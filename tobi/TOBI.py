'''
ooooooooooooo   .oooooo.   oooooooooo.  ooooo
8'   888   `8  d8P'  `Y8b  `888'   `Y8b `888'
     888      888      888  888     888  888
     888      888      888  888oooo888'  888
     888      888      888  888    `88b  888
     888      `88b    d88'  888    .88P  888
    o888o      `Y8bood8P'  o888bood8P'  o888o
          Traffic Obfuscated Internet

The goal of TOBI is to obfuscate one users http traffic with a
victim's harvested http traffic. We pose our traffic as theirs.
Authors: Nik Kirstein, Gabe Lemon

The program might eventually expand to gather all kinds of traffic and then
using that gathered traffic that has been saved, hide all kinds of traffic
as another user's.  Basically, browsing the web and having all our traffic
look like it's someone else.
'''
import mitmproxy
from mitmproxy import ctx
from mitmproxy import http
from open_str import *
import subprocess
import os
import time
import sqlite3
from pathlib import Path

# def sanitizeLogHeaders(list_of_logs, master_list_header_options):
#     for log in list_of_logs:
#         for key in log.keys():
#             for header in log[key]:
#                 print(header)

def buildInsertStatmentPerLog(indLog):
    url = "".join(list(indLog.keys()))
    list_of_heads = ['url']
    match_indx_values_head_values = []
    for key in indLog.keys():
        match_indx_values_head_values.append("'"+key+"'")
        for header in indLog[key]:
            if(list(header.keys())[0].lstrip().strip().lower() == ":authority"):
                #print("yes")
                list_of_heads.append("authority")
                match_indx_values_head_values.append("'"+header[list(header.keys())[0]]+"'")
                continue
            list_of_heads.append("'"+list(header.keys())[0].lstrip().strip().lower()+"'")
            match_indx_values_head_values.append("'"+header[list(header.keys())[0]]+"'")
    return (list_of_heads, tuple(match_indx_values_head_values,))

def getHeaderValues(list_of_logs):
    master_list_header_options = []
    for log in list_of_logs:
        for url_key in log.keys():
            for header in log[url_key]:
                if(list(header.keys())[0].lstrip().strip().lower() == ':authority'):
                    if('authority' not in master_list_header_options):
                        master_list_header_options.append('authority')
                        continue
                else:
                    if "'"+list(header.keys())[0].lstrip().strip().lower()+"'" not in master_list_header_options:
                        master_list_header_options.append("'"+list(header.keys())[0].lstrip().strip().lower()+"'")
    return master_list_header_options

def parseDumpBuildLogToHeaders():
    build_log_list = []
    my_file = Path("out_dump")
    if my_file.is_file():
        print("Your output log has been found. Building database.")
    else:
        print("Dump file out_dump wans't found. Would you like to create a dump file of traffic?")
        print("Press 1 for yes, 0 to exit program.")
        run_mitmdump()
        return
    header_dict = {}
    opened_log = open("out_dump",'r')
    log_name = ""
    log_entry = {}
    for line in opened_log:
        if(line.strip().lstrip() == "REQUEST END"):
            build_log_list.append(log_entry)
            log_entry = {}
            log_name = ""
            continue
        elif(line == "NEW REQUEST"):
            continue
        elif(line.split("|")[0] == "URL"):
            log_name = "".join(line.split("|")[1]).strip().lstrip()
            log_entry[log_name] = []
            # print(log_name)
            continue
        elif(line.split("|")[0] == "HEADER"):
            log_entry[log_name].append({line.split("|")[1].lstrip().strip().lower():line.split("|")[2].strip().lower()})
            continue
    return build_log_list

#Remane to linkingDatabase
def createDatabase(master_list_header_options):
    my_file = Path("net_logs.db")
    if(my_file.is_file()):
        db = sqlite3.connect('net_logs.db')
        db.row_factory = sqlite3.Row
        print("Already here")
        return db

    else:
        print("Database not found. Creating table.")
        db = sqlite3.connect('net_logs.db')
        create_string = "CREATE TABLE netlogs (url TEXT,"
        for index in range(len(master_list_header_options)-1):
            create_string += master_list_header_options[index]+" TEXT,"
        create_string += master_list_header_options[len(master_list_header_options)-1] + " TEXT);"
        # print(create_string)
        db.execute(create_string)
        db.commit()
        return db

    # from urllib.request import pathname2url
    # try:
    #     dburi = 'file:{}?mode=rw'.format(pathname2url("net_logs.db"))
    #     conn = lite.connect(dburi, uri=True)
    #     c = conn.cursor()
    #     print("Database connected.")
    # except lite.OperationalError:

    #     print("\"net_logs.db\" could not be found in the diretory.\nCreating connection in directory to connet_logs.db")
    #     conn = lite.connect('net_logs.db')
    #     c = conn.cursor()
    #     create_string = "CREATE TABLE netlogs (url TEXT,"
    #     for index in range(len(master_list_header_options)-1):
    #         create_string += master_list_header_options[index]+" TEXT,"
    #     create_string += master_list_header_options[len(master_list_header_options)-1] + " TEXT);"
    #     print(create_string)
        # c.execute(create_string)
        # conn.commit()
    print("Table created, ready for log entries.")
    # return c

def fill_table(list_of_logs, dbConnection,header_list):
    match_count = 0
    for log in list_of_logs:
        (list_of_heads, match_indx_values_head_values) = buildInsertStatmentPerLog(log)
        print(type(match_indx_values_head_values))
        if(len(list_of_heads) == len(match_indx_values_head_values)):
            match_count += 1
        insert_statement = "INSERT INTO netlogs ("
        for i in range(len(list_of_heads)-1):
            insert_statement += list_of_heads[i]+", "

        insert_statement += list_of_heads[len(list_of_heads)-1]+") VALUES("
        #insert_statement += list_of_heads[len(match_indx_values_head_values)-1]+") VALUES("
        for i in range(len(list_of_heads)-1):
            insert_statement += "?,"
        insert_statement += "?)"
        print(insert_statement)
        dbConnection.execute(insert_statement, match_indx_values_head_values)
        dbConnection.commit()
        #print(insert_statement)
        # if(match_count == len(list_of_logs)):
        #     print("All good.")

def generateLogs():
    #dump_out = subprocess.Popen(['mitm/mitmdump','-s','flowTests.py','>','out_dump'],shell=True)
    print("Running mitmdump and logging traffic. Press q to exit.")
    time.sleep(2)
    os.system("bash -c \"mitmdump -s logger.py >> out_dump\"")
    # user_input = input()
    # if(user_input == 1):
    #     print("Quit")
    return 1

def repalaceHeaders():
    #dump_out = subprocess.Popen(['mitm/mitmdump','-s','flowTests.py','>','out_dump'],shell=True)
    print("Randomly changing request header properties")
    time.sleep(2)
    os.system("bash -c \"mitmdump -s re_flow.py\"")
    # user_input = input()
    # if(user_input == 1):
    #     print("Quit")
    return 1

def injectJavascript():
    print("Injecting javascript to mask fingerprint values")
    time.sleep(2)
    os.system("bash -c \"mitmdump -s javascript_inject.py\"")
    return 1

def injectandflow():
    print("Injecting javascript and changing headersb")
    time.sleep(2)
    os.system("bash -c \"mitmdump -s injectAndFlow.py\"")
    return 1

def main():
    print(opening_string)
    quit = False
    while(quit == False):
        print("What task would you like to perform")
        print("\nLog traffic: Press: 1\nCreate database: 2\nReplace headers: 3\nInject Javascript: 4\nReplace Heads and Inject: 5")
        user_input = input()
        if(user_input == "1"):
            generateLogs()
            continue
        elif(user_input == "2"):
            logs = parseDumpBuildLogToHeaders()
            master_list_header_options = getHeaderValues(logs)
            dbConnection = createDatabase(master_list_header_options)
            fill_table(logs, dbConnection,master_list_header_options)
            continue
        elif(user_input == "3"):
            repalaceHeaders()
            continue
        elif(user_input == "4"):
            injectJavascript()
            continue

        elif(user_input == "5"):
            injectandflow()
            continue
        else:
            print("You need to press 1 through 5")





if __name__ == '__main__':
    main()
