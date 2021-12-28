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
Authors: Nik Kirstein, Gabe

The program might eventually expand to gather all kinds of traffic and then
using that gathered traffic that has been saved, hide all kinds of traffic
as another user's.  Basically, browsing the web and having all our traffic
look like it's someone else.
'''

import mitmproxy
from mitmproxy import ctx
from mitmproxy import http
from pathlib import Path
import sqlite3
import random
from TOBI import parseDumpBuildLogToHeaders, getHeaderValues


logs = parseDumpBuildLogToHeaders()
master_list_header_options = getHeaderValues(logs)


def checkForDatabase():
    '''
    This function takes checks for database and returns a connection
    Parameters:
    return: A sqlite3 database connection
    '''
    my_file = Path("net_logs.db")
    if(my_file.is_file()):
        db = sqlite3.connect('net_logs.db')
        db.row_factory = sqlite3.Row
        print("Found database.")
        return db

    else:
        print("Database not found. Run TOBI with log traffic option.")
        return

database = checkForDatabase()
def getAHeaderForLikeURL(url,database):
    '''
    This function querys a like url ad returns a query results from the database
    Parameters:
    url: A url to search the database for
    db_connection: A connection object to a traffic db
    return: A cursor to the query result
    '''
    start_ind = 0
    end_ind = 0
    for i in range(len(url)):
      if(url[i] == '.' and start_ind == 0):
        start_ind = i
      if(url[i] == '.' and start_ind != 0):
        end_ind = i
        if(end_ind == 0):
          print("Didn't catch.")
    query_String = "SELECT * FROM netlogs WHERE url like '%"+url[start_ind:end_ind]+"%';"
    cursor = database.execute(query_String)

    return cursor

def request(flow: http.HTTPFlow) -> None:

    # ctx.log.info("HEADERS FOR REQUEST: GOING OUT")
    cursor = getAHeaderForLikeURL(flow.request.url,database)
    picked_header = int(random.randint(1,len(master_list_header_options)-1))
    #Manually set this for demo
    #flow.request.headers['user-agent'] = "BlackBerry8520/5.0.0.681 Profile/MIDP-2.1 Configuration/CLDC-1.1 VendorID/114"
    for header in flow.request.headers:
        #if(header.lstrip().strip().lower() == "user-agent"):
        #     ctx.log.info("Check fired")
        #     cc =  "BlackBerry8520/5.0.0.681 Profile/MIDP-2.1 Configuration/CLDC-1.1 VendorID/114"
        #     continue
        if(header.lstrip().strip().lower() in master_list_header_options[picked_header]):
          for col in enumerate(cursor):
            flow.request.headers[header] =  col[1][picked_header]
            print(header)
            print("replaced")
            break
