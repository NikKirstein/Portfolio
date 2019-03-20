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
'''

import mitmproxy
from mitmproxy import ctx
from mitmproxy import http
from bs4 import BeautifulSoup


def request(flow: http.HTTPFlow) -> None:
    ctx.log.info("OUTGOING REQUEST")

def response(flow: http.HTTPFlow) -> None:
    #ctx.log.info(str(flow.response.status_code))

    #Get headers so we can compare for a specific one
    header_list = []
    for header in flow.response.headers:
        header_list.append(header)
        #ctx.log.info(header +" : " + flow.response.headers[header])
    #print(header_list)

    #If the header content-type exists, check so we only inject
    #javascript in html files
    if "Content-Type" in header_list or "content-type" in header_list:
        #text/html; charset=UTF-8
        if "text/html" in flow.response.headers["content-type"] or "text/html" in flow.response.headers["Content-Type"]:
            #html = (flow.response.content).decode('utf-8', 'replace')
            html = (flow.response.content).decode()
            #ctx.log.info(html)
            Beautiful_html = BeautifulSoup(html)

            #Docstrings for the javascript function used to overwrite and
            #give new properties to existing objects that are read-only
            '''
            /**
             * Creates or replaces a read-write-property in a given scope object, especially for non-writable properties.
             * This also works for built-in host objects (non-DOM objects), e.g. navigator.
             * Optional an initial value can be passed, otherwise the current value of the object-property will be set.
             *
             * @param {Object} objBase  e.g. window
             * @param {String} objScopeName    e.g. "navigator"
             * @param {String} propName    e.g. "userAgent"
             * @param {Any} initValue (optional)   e.g. window.navigator.userAgent
             */
             '''

             '''
             This code will eventually be updated to either share JavaScript values from others users 
             with a database.  Or, automatically fill in with whatever values are taken from the header database.
             
             Coordinating two databases to have the same values whenever possible sounds annoying, but possible.
             '''

             #Actually do the javascript code changing properties
             # All values below are placeholders for now, and also must be expanded.


            user_agent_string = ("Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) "
                                 "AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4")
            platform = "Mac68K"

            screen_height = '400'
            screen_width = '650'

            avail_screen_height = '395'
            avail_screen_width = '645'


            Javascript_Code = (
                'function createProperty(value) { var _value = value; function _get() { return _value; } '
                'function _set(v) { _value = v; } return { "get": _get, "set": _set };}; '
                'function makePropertyWritable(objBase, objScopeName, propName, initValue) '
                '{ var newProp, initObj; if (objBase && objScopeName in objBase && propName in objBase[objScopeName]) '
                '{ if(typeof initValue === "undefined") { initValue = objBase[objScopeName][propName]; } '
                'newProp = createProperty(initValue); '
                'try { Object.defineProperty(objBase[objScopeName], propName, newProp); } catch (e) { initObj = {}; '
                'initObj[propName] = newProp; '
                'try { objBase[objScopeName] = Object.create(objBase[objScopeName], initObj); } catch(e) { } } } }; '
                'makePropertyWritable(window, "navigator", "userAgent"); '
                'window.navigator.userAgent = "' + user_agent_string + '"; '
                'makePropertyWritable(window, "navigator", platform"); '
                'window.navigator.platform = "' + platform + '"; '
                'makePropertyWritable(window, "screen", "height"); window.screen.height = "' + screen_height + '"; '
                'makePropertyWritable(window, "screen", "width"); window.screen.width = "' + screen_width + '"; '
                'makePropertyWritable(window, "screen", "availHeight"); '
                'window.screen.availWidth = "' + avail_screen_height + '"; '
                'makePropertyWritable(window, "screen", "availWidth"); '
                'window.screen.availHeight = "' + avail_screen_width + '"; '
            )

            #Make a new script tag and put the javascript in it
            if Beautiful_html.body:
                    script = Beautiful_html.new_tag(
                        "script",
                        type='application/javascript',)
                    script.string = (Javascript_Code)
                    #to insert into head (gives errors for things that dont have a head)
                    #Beautiful_html.head.insert(0, script)
                    #to insert into body
                    Beautiful_html.body.insert(0, script)
                    #print(Beautiful_html)
                    #print(type(Beautiful_html.encode('utf-8')))

                    #remake flow object for mitmdump
                    flow.response.content = Beautiful_html.encode('utf-8')
