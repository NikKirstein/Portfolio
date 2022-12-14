from datetime import datetime
from elasticsearch6 import Elasticsearch
import re
import clientresponse
import pandas as pd
import numpy as np
import json
import textwrap  # this library handles printing only to a certain column.
# Keeping it in for now but should be moved to clientresponse.py eventually


def get_all_hits_from_search(main_dict, counter, es, index_to_search, query_body, hit_size, scroll_size):
    """
    Searches an Index in Elasticsearch and gets all the documents in that index.
    Each document is a python dictionary.  This function loops through every single document in a response and parses
    them for nested columns and values and then appends this built dictionary to a main_dict
    assigns them a number index as it's key.  It looks something like:
    { 0: {"_index": "metricbeat", "doc_id": "ejfj223ddkk"}, 1: {"_index": "metricbeat", "doc_id": "fkkkeiii32"} }
    The main dictionary is populated using this function and contains indexes (as numers) mapped to individual documents.
    Nothing is returned, this function modifies and populates main_dict and counter in place.
    :param main_dict: an externally fed dictionary to be populated with documents that are parsed to column: values
    :param counter: an external counter used to keep track of the total number of documents seen.
    :param es: Elasticsearch instance
    :param index_to_search: the index to search documents from
    :param query_body: the query body used in the search
    :param hit_size: number of documents to get back in a search
    :param scroll_size: scroll to use in the elasticsearch search.  Can be maximum of 10000.
    :return: None: Populates main_dict in place.
    """
    # Hit elastic and search using parameters
    print("Using Index:", index_to_search)
    docs_expected = es.count(index=index_to_search, body=query_body)
    print("Expecting:", str(docs_expected), "documents returned.")
    response = es.search(index=index_to_search, body=query_body, size=hit_size, scroll=scroll_size)
    # print(response)
    # Pull scroll ID for next step of documents
    search_scroll_id = response['_scroll_id']
    # How many documents were returned. This matters because if you finish your search, scroll size can be 0.
    scroll_size = len(response['hits']['hits'])
    # all_returned_documents = []

    # If documents still present.
    while scroll_size > 0:
        # print(response)
        print("Scrolling...", " Hit length:", scroll_size)
        # print(type(response))
        # print("going into function")
        counter = loop_through_response_and_append_dict(main_dict, counter, response['hits']['hits'])
        print("total documents so far:", str(counter))
        # all_returned_documents = all_returned_documents + response['hits']['hits']
        # This is es.scroll not es.search, so all we need to do is provide the ID.
        response = es.scroll(scroll_id=search_scroll_id, scroll='5m')
        # Get next scroll ID and next size.  If scroll_size is 0, loop will finish, otherwise, loop goes again.
        search_scroll_id = response['_scroll_id']
        scroll_size = len(response['hits']['hits'])
        print("New scroll size is:", str(scroll_size))


def pull_column_value_dict_from_json(json_obj):
    """
    Takes a list of column values from get_columns_from_json and tosses
    some extra nested and un-needed key/value pairs.  We only care about
    un-nested and properly extracted columns, so we toss ones that we didn't parse earlier.
    :param json_obj: a dictionary/json object of keys (document columns) and values as actual document values.
    :return: total_scrubbed_dict, the same as json_obj but without keys and values in which those values were dictionaries.
    """
    total_value_list = []
    total_scrubbed_dict = {}
    get_columns_from_json(json_obj, total_value_list)
    # print(total_value_list)
    for item in total_value_list:
        # print(item.values())
        for key, value in item.items():
            if type(value) is not dict:
                total_scrubbed_dict.update(item)
            # print(key, value)
            # print(type(key), type(value))
        # print(item)

    return total_scrubbed_dict


def get_columns_from_json(json_obj, value_list, previous_key=None, key_list=[]):
    """
    This is a recursive function.  It looks through an Elasticsearch document and looks at the nested fields.
    Every time it finds a nested field in the JSON, it uses recursion to keep track of that field name and the
    nested field names and creates a single field name that is a nested representation of the json document.
    Example: {source: memory: {bytes: 100283, pct: 0.2} }
    becomes
    source.memory.bytes: 100283
    source.memory.pct: 0.2
    This is we can export all nested fields as individual columns for a csv.
    :param json_obj: An elasticsearch document in json format.
    :param value_list: an externally fed list (usually empty) to populate with un-nested columns as shown above and their values.
    :param previous_key: used for the recursion, the last key it saw in the JSON document
    :param key_list: used in recursion. An ongoing list of all the keys so far seen.
    :return: found_keys, all the keys so far seen in the JSON object.  Really, the main meat and functionality
    is the function populating the value_list.
    """
    if type(json_obj) is not dict:
        key_list.append(previous_key)
        # print("Top Level found", key_list)
        # print(previous_key)
        # print(key_list)
        return key_list
    found_keys = []
    for current_key, current_value in json_obj.items():
        if previous_key is not None:
            new_key = str(previous_key) + "." + str(current_key)
            # print("Not None", new_key)
        else:
            new_key = current_key
        # print(found_keys)
        if previous_key is None and current_value is not dict:
            value_list.append({current_key: current_value})
        elif previous_key is not None and current_value is not dict:
            value_list.append({str(previous_key) + '.' + str(current_key): current_value})
        # print(current_key, previous_key, current_value)
        found_keys.extend(get_columns_from_json(current_value, value_list, new_key, []))
    # print(found_keys)
    # print(value_list)
    return found_keys


def loop_through_response_and_append_dict(main_dict, counter, es_response_obj):
    """
    The main function that's using the previous two functions to populate one main dictionary.
    This is used because we have to build a dictionary before turning it into a pandas dataframe
    as pandas dataframe functions are too expensive to build from.  It uses a counter to keep track
    of all documents seen so far and uses that to assign an index to each and every json_obj in order
    to build the pandas DataFrame.
    :param main_dict: The main dictionary to populate.
    :param counter: a counter object to keep track of the pandas index to assign to json_objects of un-nested columns
    :param es_response_obj: a response object from elasticsearch.  This function loops through this and
    un-nests the json keys into columns and assigns them their values and then assigns an index to that dictionary
    and adds it to the main top level dictionary main_dict
    :return: counter: in order to keep track of all the documents and use this counter over again.  main_dict
    isn't returned because it's populated in place.
    """
    # print("looping through response")
    # print(main_df)
    for json_obj in es_response_obj:
        # print(json_obj)
        individual_json_dict = pull_column_value_dict_from_json(json_obj)
        # print(individual_json_dict)
        main_dict[counter] = individual_json_dict
        counter += 1
    return counter


# noinspection PyBroadException
def write_to_csv(es, search_index, execute_query, filename):
    """
    takes an elasticsearch instance, an index or index pattern,
    a query, and a filename to write all the documents under this index and query
    and convert them into a DataFrame and write that DataFrame to a csv file.
    :param es: an elasticsearch instance object
    :param search_index: an index or index pattern, must be valid
    :param execute_query: an elasticsearch query, should be valid or errors will occur.
    :param filename: the filename/path to output the csv file under
    :return: None, outputs a file.
    """
    doc_process_time_start = datetime.now()
    total_dict = {}
    counter = 0
    get_all_hits_from_search(total_dict, counter, es, search_index, execute_query, 10000, '5m')
    main_dataframe = pd.DataFrame.from_dict(total_dict, "index")
    # print(main_dataframe)
    possible_cols = ""
    for col in main_dataframe.columns:
        possible_cols += (col + ", ")
    print("It took", (datetime.now() - doc_process_time_start).seconds, "seconds", "to pull documents for export.")
    print("Columns found:")
    cols_found = textwrap.wrap(possible_cols, 80)
    for line in cols_found:
        print(line)

    user_response = input("Insert columns to write separated by a space (leave blank for all): ")
    csv_write_time_start = datetime.now()

    if user_response == "":
        main_dataframe.to_csv(filename, index=False)
    else:
        columns_to_write = user_response.split(" ")
        main_dataframe.to_csv(filename, index=False, columns=columns_to_write)

    print("Writing to file:", str(filename))
    print("Done!")
    print("It took", (datetime.now() - csv_write_time_start).seconds, "seconds", "to write your csv.")
    return None


def main():
    """
    Note: This version if main does not include lots of input checking.
    clientresponse.py has more input checking and should be used over this main function.
    Only used if this is run by itself and not used in the main client script.
    It's less robust and doesn't do as much input checking/validation.
    This will break if the IPs aren't valid, the indices aren't valid and/or the query isn't valid.
    Otherwise if everything is valid, it will take all the given input and output a csv file.
    :return: None
    """

    start_time = datetime.now()

    pd.set_option("display.max_columns", None, "display.max_rows", None, "display.width", None, "display.max_colwidth", 1)

    elastic_instance = input("Insert IP of Elasticsearch instance: ")
    es = Elasticsearch(elastic_instance, sniff_on_start=True)
    index_to_search = input("Insert Index to search (leave blank for *): ")
    if index_to_search == "":
        index_to_search = "*"
    query_to_execute = input("Insert Query, must be valid JSON (leave blank for match_all): ")
    if query_to_execute == "":
        query_to_execute = {"query": {"match_all": {}}}
    output_filename = input("Insert output filename: ")

    write_to_csv(es, index_to_search, query_to_execute, output_filename)

    print("Script ran for", (datetime.now() - start_time).seconds, "seconds")


if __name__ == '__main__':
    main()