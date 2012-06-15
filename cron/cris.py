import lxml, json
from lxml import etree
from StringIO import StringIO




def parseXML(xmlFile):
    tree = etree.parse(xmlFile)
    e = etree.XPathEvaluator(tree)
    e.register_namespace('api', 'http://www.symplectic.co.uk/publications/api')
    # get all users in this page
    users = e('//api:object[@category="user"]')
    for user in users:
        prop_id = user.get("proprietary-id")
        id = user.get("id")
        username = user.get("username")
        href = user.get("href")
        print prop_id, ",", id, ",", username, ",", href

    # get next/last     
    next = e('//api:page[@position="next"]')[0].get("href")
    last = e('//api:page[@position="last"]')[0].get("href")
    if next <> last:
        parseXML(next)

#read settings, load url, parse resulting text
settings_text = open("config.json", "r").read()
settings = json.loads(settings_text)
cris_url = settings["cris"]["url"]
cris_port = settings["cris"]["port"]

parseXML(cris_url + ":" + cris_port +"/publications-api/objects?categories=users")
