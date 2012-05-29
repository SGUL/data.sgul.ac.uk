import lxml
from lxml import etree
from StringIO import StringIO

#<api:pagination results-count="1059" items-per-page="25">
#    <api:page position="this" number="1" href="http://cris.sgul.ac.uk:8090/publications-api/objects?categories=users"/>
#    <api:page position="first" number="1" href="http://cris.sgul.ac.uk:8090/publications-api/objects?categories=users"/>
#    <api:page position="next" number="2" href="http://cris.sgul.ac.uk:8090/publications-api/objects?categories=users&amp;page=2"/>
#    <api:page position="last" number="43" href="http://cris.sgul.ac.uk:8090/publications-api/objects?categories=users&amp;page=43"/>
#</api:pagination>


#<api:object category="user" id="314" proprietary-id="E114886" authenticating-authority="ORG" username="cowen" last-modified-when="2012-05-24T13:25:48.26+01:00" is-deleted="false" href="http://cris.sgul.ac.uk:8090/publications-api/users/314" created-when="2010-02-14T11:10:57.37+00:00" type-id="1">

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

    # get next/last - also available: first, this
    next = e('//api:page[@position="next"]')[0].get("href")
    last = e('//api:page[@position="last"]')[0].get("href")
    if next <> last:
        parseXML(next)

parseXML("http://cris.sgul.ac.uk:8090/publications-api/objects?categories=users")

