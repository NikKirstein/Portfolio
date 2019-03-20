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
from mitmproxy.utils import strutils
from mitmproxy import http

header_list = []
header_dict = {}

def request(flow: http.HTTPFlow) -> None:
    ctx.log.info("NEW REQUEST")
    #ctx.log.info("HEADERS FOR REQUEST: GOING OUT\n")
    ctx.log.info("URL| " + flow.request.url)
    for header in flow.request.headers:
        if header not in header_list:
            header_list.append(header)
        if header not in header_dict:
            header_dict.setdefault(header, [])
            if flow.request.headers[header] not in header_dict[header]:
                header_dict[header].append(flow.request.headers[header])

        value = flow.request.headers[header]
        ctx.log.info("HEADER| " + header +"| "+ value)
        #ctx.log.info("HEADER: " + header + ": " + flow.request.headers[header])
        #print("Header list: ", header_list)
        #print("\nHeader Dict: ", header_dict)
        #for raw bytes of the response
        '''
        ctx.log.info("String representation of bytes from rawcontent\n")
        ctx.log.info(str(flow.request.raw_content))
        ctx.log.info("Decoded raw content using utf-8\n")
        ctx.log.info((flow.request.raw_content).decode("utf-8"))
        '''
    ctx.log.info("REQUEST END")
