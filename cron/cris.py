import lxml, json
from lxml import etree
from StringIO import StringIO


def parseUser(xmlFile):
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
        type = user.get("type-id")
        current = e('//api:is-current-staff')[0].text
        currents = e('//api:is-current-staff')
        # TODO this is all wrong - it needs to search in the current node
        for c in currents:
            print c.text
        #try:
        #    title = e('//api:title')[0].text
        #except Exception, err:
        #    title = ""
        #lastname = e('//api:last-name')[0].text
        #firstname = e('//api:first-name')[0].text
        #email = e('//api:email-address')[0].text
        #print prop_id, ",", id, ",", username, ",", href, ",", type, ",", current, ",", title, ",", lastname, ",", firstname, ",", email

def parseUserFeed(xmlFile):
    pass

def parseUserFeedList(xmlFile):
    tree = etree.parse(xmlFile)
    e = etree.XPathEvaluator(tree)
    e.register_namespace('api', 'http://www.symplectic.co.uk/publications/api')
    # get all users in this page
    users = e('//api:user-feed-entry')
    for user in users:
        enew = etree.XPathEvaluator(user)
        enew.register_namespace('api', 'http://www.symplectic.co.uk/publications/api')
        last = enew('api:last-name')
        for l in last:
            print l.text
            # TODO Wrong: it's got all the users
        #user.e('//api:last-name')
        #prop_id = user.get("proprietary-id")
        #id = user.get("id")
        #username = user.get("username")
        #href = user.get("href")

    # get next/last     
    next = e('//api:page[@position="next"]')[0].get("href")
    last = e('//api:page[@position="last"]')[0].get("href")
    #if next <> last:
        #parseUserFeedList(next)
    

def parseUserList(xmlFile):
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
        parseUser(href)

    # get next/last     
    next = e('//api:page[@position="next"]')[0].get("href")
    last = e('//api:page[@position="last"]')[0].get("href")
    #if next <> last:
    #    parseUserList(next)


def parsePublicationList(xmlFile):
    pass

#read settings, load url, parse resulting text
settings_text = open("config.json", "r").read()
settings = json.loads(settings_text)
cris_url = settings["cris"]["url"]
cris_port = settings["cris"]["port"]

#parseUserList(cris_url + ":" + cris_port +"/publications-api/objects?categories=users")
parseUserFeedList(cris_url + ":" + cris_port +"/publications-api/user-feeds/STAFF")
