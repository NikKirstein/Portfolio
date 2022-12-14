from datetime import datetime  # used for timing the script
from elasticsearch6 import Elasticsearch  # Used for Elasticsearch operations
import csv_output  # the script that handles recursively grabbing columns and outputting them
import json  # processing JSON
import re  # regex for input checking
import os  # os for creating and checking directories


def get_all_hits_from_search(es, index_to_search, query_body, hit_size, scroll_size):
    """
    Searches an Index in Elasticsearch and gets all the documents in that index.
    Each document is a python dictionary.  This function appends them to a list.
    So what is returned is a list of Elasticsearch documents that are in python dictionary form.
    :param es: Elasticsearch instance
    :param index_to_search: the index to search documents from
    :param query_body: the query body used in the search
    :param hit_size: number of documents to get back in a search
    :param scroll_size: scroll to use in the elasticsearch search.  Can be maximum of 10000.
    :return: all_returned_documents: a list of all the hits from a search
    """
    # Hit elastic and search using parameters
    print("Using Index:", index_to_search)
    response = es.search(index=index_to_search, body=query_body, size=hit_size, scroll=scroll_size)
    # Pull scroll ID for next step of documents
    search_scroll_id = response['_scroll_id']
    # How many documents were returned. This matters because if you finish your search, scroll size can be 0.
    scroll_size = len(response['hits']['hits'])
    all_returned_documents = []

    # If documents still present.
    while scroll_size > 0:
        # print(response)
        print("Scrolling...", " Hit length:", scroll_size)
        all_returned_documents = all_returned_documents + response['hits']['hits']
        # This is es.scroll not es.search, so all we need to do is provide the ID.
        response = es.scroll(scroll_id=search_scroll_id, scroll='2m')
        # Get next scroll ID and next size.  If scroll_size is 0, loop will finish, otherwise, loop goes again.
        search_scroll_id = response['_scroll_id']
        scroll_size = len(response['hits']['hits'])

    return all_returned_documents


def change_dates(new_date, list_of_objects):
    """
    Note: This is dead code and is no longer used.
    Takes a list of Elasticsearch documents in Python dictionary form.  This list is built
    from the get_all_hits_from_search function.
    Loops through every document and changes the timestamp to a new date: new_date parameter.
    The format of that date is "yyyy-mm-dd" for the timestamp field.  Note that indexes for Elastic
    Don't follow that format, they use "yyyy.mm.dd" so don't get confused.  Use the dashes.
    Doesn't return anything, Modifies the dictionary place so it's often best to feed a copied dictionary
    to this function to preserve the original for later use.
    :param new_date: a string in the format "yyyy-mm-dd"
    :param list_of_objects: A list of Elastic documents, where each document is in python dictionary format.
    :return: None
    """
    for hit in list_of_objects:
        doc_body = hit['_source']
        # print(doc_body)
        timestamp = doc_body['@timestamp']
        date_only = timestamp.split('T')[0]
        time_only = timestamp.split('T')[1]
        new_timestamp = new_date + 'T' + time_only
        # print(new_timestamp)
        doc_body['@timestamp'] = new_timestamp
        # print(doc_body)
    return None


def add_to_index(es_connection, index_to_add_to, list_of_objects):
    """
    # This is dead code and is no longer used.
    Takes an Elasticsearch connection, an index, and a list of Elasticsearch documents where each document
    is in python dictionary format.  This will loop through each document and add it to the Index specified.
    The index does not need to exist already but the Index should follow a pattern so that an index pattern
    can be matched on it later.
    :param es_connection: An Elasticsearch connection instance.
    :param index_to_add_to: a string of the index to add the documents to.  Does not need to exist.
    :param list_of_objects: A list of Elastic documents, where each document is in python dictionary format.
    :return: None, should create an index and add documents to it though.  Check Kibana or Elasticsearch
    directly once the script has finished running to see results.
    """
    for hit in list_of_objects:
        doc_body = hit["_source"]
        es_connection.index(index_to_add_to, 'doc', doc_body)
    return None


def ip_validator(ip_list):
    """
    Takes a list of IPs in string form and uses a regex expression to check if they are valid.
    Returns true or false if all the ips in the list are valid.
    :param ip_list: a list of IPs as strings
    :return: True or False if all IPs are valid or not.
    """
    ip_regex_expression = ('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}'
                           '([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
    for ip in ip_list:
        # print(re.match(ip_regex_expression, ip))
        if re.match(ip_regex_expression, ip) is None:
            return False
    return True


def query_validator(query):
    """
    Takes a string which should be a string representation of a JSON document/python dictionary
    If the string is in fact in the above format, it will return it as a python dictionary.
    If not, it will return False
    :param query: a string form of a python dictionary (or any string)
    :return: query_dict, a python form of the input string or False if it couldn't be converted.
    """
    if query == "":
        # If no query was input, we assume default match all and return this
        query = '{"query": {"match_all": {}}}'
    try:
        # Try to turn the string into a python dictionary
        query_dict = json.loads(query)
    except json.JSONDecodeError:
        # if it fails, it wasn't in a format that python could turn into a dictionary
        print("Invalid query, try again")
        # return False for invalid query
        return False
    # If it makes it through the above try, except, it's valid. We print what we are using.
    print("Using query:", query_dict)
    # return the valid query in dictionary format.
    return query_dict


def indices_found(es, index_input):
    """
    Takes an elasticsearch instance and a string and uses it to populate a list
    of indices in elastic that match the string.  It should accept wildcards attached.
    :param es: Elasticsearch instance object
    :param index_input: string to search indexes for.  Can contain * to wildcard match
    :return: index_list: A list of strings of indices elastic found using the input.
    """
    alias_response = es.indices.get_alias(index_input)
    index_list = sorted(list(alias_response.keys()))
    return index_list


def generate_indice_report(es, index_search="*"):
    """
    This function differs from indices_found because it serves as a search function as well.
    It will always search using a wildcard even if none are specified and the default/blank input is
    a wildcard as well, which will match all indices.  This function uses that input to
    print a report of all the indices it finds based on the search and prints out their size in Elastic as well.
    :param es: An elasticsearch instance object
    :param index_search: a string to search indices in Elasticsearch
    :return: None, prints a report to the console.
    """
    alias_response = es.indices.get_alias(index_search + '*')
    populated_index_list = sorted(list(alias_response.keys()))

    print("Indices".center(100, "="))
    for index_item in populated_index_list:
        individual_index_response = es.indices.stats(index_item)
        # print(individual_index_response)
        index_doc_count = individual_index_response['_all']['primaries']['docs']['count']
        index_size = individual_index_response['_all']['total']['store']['size_in_bytes']
        # print(index_item, index_doc_count, index_size)
        # print("==" + index_item.center(76) + "==")
        print(("==  " + (str(index_item)).ljust(40) +
               " " * 3 +
               ("Doc Count: " + str(index_doc_count)).ljust(28) +
               " " * 3 +
               ("Size: " + (str(round(index_size / (1024 * 1024), 1)) + "mb")).ljust(18) + "  =="))
    if len(populated_index_list) == 0:
        print("No indices found.")
    print("=" * 100)


def generate_node_report(es):
    """
    Takes an Elasticsearch instance object and prints some information out about the nodes in the cluster.
    :param es: an elasticsearch instance object
    :return: None, prints node information out to console
    """
    node_info_dictionary = es.nodes.info()
    # print(node_info_dictionary)
    for individual_node in node_info_dictionary["nodes"]:
        node_name = node_info_dictionary["nodes"][individual_node]["name"]
        node_roles = ', '.join(node_info_dictionary["nodes"][individual_node]["roles"])
        # Unused for now but potentially useful to keep
        # transport_address = node_info_dictionary["nodes"][individual_node]["transport_address"]
        # Unused for now since host is often node_name but potentially use to keep
        # host = node_info_dictionary["nodes"][individual_node]["host"]
        node_ip = node_info_dictionary["nodes"][individual_node]["ip"]

        print(("==      " + "Node: " + str(node_name)).ljust(28) + (" " * 10) +
              ("Node IP: " + str(node_ip)).rjust(34) + "      ==")
        print(("==      " + "Node Roles: ").ljust(28) + (" " * 10) +
              (str(node_roles)).rjust(34) + "      ==")
        print("==" + "---".center(76) + "==")
    return None


def print_cluster_report(es):
    """
    Takes an Elasticsearch instance object and prints some information out about cluster.
    :param es: an elasticsearch instance object
    :return: None, prints cluster information out to the console.
    """
    cluster_stats_dictionary = es.cluster.stats()
    # print(cluster_stats_dictionary)

    cluster_name = cluster_stats_dictionary['cluster_name']
    node_count = cluster_stats_dictionary["_nodes"]["total"]
    indice_count = cluster_stats_dictionary["indices"]['count']
    shard_total_count = cluster_stats_dictionary['indices']['shards']['total']
    shard_primary_count = cluster_stats_dictionary['indices']['shards']['primaries']
    shard_replication_count = cluster_stats_dictionary['indices']['shards']['replication']
    doc_count = cluster_stats_dictionary['indices']['docs']['count']

    print((str(cluster_name) + " Report").center(80, '='))
    print("==  " + "Number of Nodes:".ljust(35) + str(node_count).ljust(37) + "  ==")
    generate_node_report(es)
    print(("==  " + ("Total Shards: " + str(shard_total_count)).ljust(17) +
           " " * 5 +
           ("Primary Shards: " + str(shard_primary_count)).center(22) +
           " " * 5 +
           ("Replication active: " + str(round(shard_replication_count, 3))).rjust(22) + "  =="))
    print("==  " + "Number of Indices:".ljust(35) + str(indice_count).ljust(37) + "  ==")

    print("==  " + "Number of Docs:".ljust(35) + str(doc_count).ljust(37) + "  ==")
    return None


def display_menu(es):
    """
    Displays a menu of this program.  What the options are for using it.
    :param es: an elasticsearch instance object
    :return: None, prints information to console
    """

    print("PyElastic-Client ".center(80, '='))

    cluster_health_response = es.cluster.health()
    cluster_name = str(cluster_health_response['cluster_name'])
    health_status = str(cluster_health_response['status'])

    print(((("Cluster: " + cluster_name) +
            " " * 10 +
            ("Health Status: " + health_status)).center(76)).center(80, "="))
    print("=" * 80)
    print("    Menu Options:".ljust(76).center(80, "="))
    print("    1) Print Cluster Information Report".ljust(76).center(80, "="))
    print("    2) Search and Display Indices".ljust(76).center(80, "="))
    print("    3) Print Top 10 Documents from Index".ljust(76).center(80, "="))
    print("    4) Save Documents to CSV File".ljust(76).center(80, "="))
    print("    5) Exit".ljust(76).center(80, "="))
    print("=" * 80)
    return None


def response_handler(es, user_input):
    """
    Takes user input and an elasticsearch input and handles what actions and functions to
    execute for the user, either displaying information out outputting documents in a format.
    :param es: an elasticsearch instance object
    :param user_input: a number that corresponds to a menu item on what actions/functions to execute
    :return: None
    """
    if user_input == 1:
        print_cluster_report(es)
        return None
    elif user_input == 2:
        indice_search = input("Search for Indices. Leave blank to search all: ").lower()
        generate_indice_report(es, indice_search)
        return None
    elif user_input == 3:
        indice_to_search = input("Indices to retrieve docs from; must be valid Index or Index Pattern: ").lower()
        print("Matched indices")
        list_of_indices = indices_found(es, indice_to_search)
        print([index_found for index_found in list_of_indices])
        query_to_use = query_validator(input("Insert query to use. Must be a valid JSON (blank input matches all): "))
        while not query_to_use:
            print("Query invalid, try again")
            query_to_use = query_validator(
                input("Insert query to use. Must be a valid JSON (blank input matches all): "))
        top_ten = [hits for hits in
                   es.search(index=indice_to_search, body=query_to_use, size=10, scroll="5m")['hits']['hits']]
        for doc_return in top_ten:
            print(doc_return)
        return None
    elif user_input == 4:
        indice_to_search = input("Indices to retrieve docs from; must be valid Index or Index Pattern: ").lower()
        print("Matched indices")
        list_of_indices = indices_found(es, indice_to_search)
        print([index_found for index_found in list_of_indices])
        query_to_use = query_validator(input("Insert query to use. Must be a valid JSON (blank input matches all): "))
        while not query_to_use:
            print("Query invalid, try again")
            query_to_use = query_validator(
                input("Insert query to use. Must be a valid JSON (blank input matches all): "))
        how_to_save = input("Save each index in separate CSV [Insert 1] "
                            "or as one large CSV (Resource intensive) [Insert 2]: ")
        if int(how_to_save) == 1:
            for index_retrieved in list_of_indices:
                if not os.path.exists("output"):
                    os.makedirs("output")
                filename = "output/" + str(index_retrieved) + '.csv'
                csv_output.write_to_csv(es, index_retrieved, query_to_use, filename)
        if int(how_to_save) == 2:
            filename = input("Insert output path and filename of output csv: ")
            csv_output.write_to_csv(es, indice_to_search, query_to_use, filename)
        else:
            return None
        return None
    elif user_input == 5:
        return None
    else:
        print("Number input did not match an option, try again.")
        return


def main():
    """
    This function serves as a wrapper for this client.  It asks for an IP to connect to
    of an elasticsearch instance and if it connects properly, will display a menu giving some options
    regarding how to interact with the cluster such as displaying information about it or exporting documents.
    Runs a loop and continues executing functions and actions until the user inputs the number 6 which
    is the quit option.
    :return: None
    """
    start_time = datetime.now()

    print("PyElastic-Client".center(80, '='))
    elastic_instance_host_list = input(
        "Insert IP(s) of Elasticsearch instances (space separated if more than one IP): ").split(' ')
    if not ip_validator(elastic_instance_host_list):
        print("One or more of the IPs entered was not valid.")
    es = Elasticsearch(elastic_instance_host_list, sniff_on_start=True, timeout=12000)
    if not (es.ping()):
        print("Connection to Elasticsearch cluster failed. Exiting.")
        return
    connected_ips = [es.nodes.info()['nodes'][node]['ip'] for node in es.nodes.info()['nodes']]
    print("Connection status:", es.ping(), '||| Found nodes at:', connected_ips)

    user_input = ""
    first_time_flag = True
    while user_input != 6:
        if first_time_flag:
            display_menu(es)
            user_input = input("Please input a number to select an option: ")
            first_time_flag = False
        else:
            input("Press Enter to Display Menu ")
            display_menu(es)
            user_input = input("Please input a number to select an option: ")
        try:
            user_input = int(user_input)
            response_handler(es, user_input)
        except ValueError:
            print("Input was not valid, try again")

    print("Goodbye.")
    print("Script ran for", (datetime.now() - start_time).seconds, "seconds")
    return None


if __name__ == '__main__':
    main()
