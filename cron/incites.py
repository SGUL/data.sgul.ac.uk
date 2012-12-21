import cris
from lxml import etree
import json

#read settings, load url, parse resulting text
settings_text = open("config.json", "r").read()
settings = json.loads(settings_text)
cris_url = settings["cris"]["url"]
cris_port = settings["cris"]["port"]

# Users management
def parseUserList(xmlFile,url):
    mynext = xmlFile
    tree = etree.parse(xmlFile)
    root = tree.getroot()
    last = root.xpath('//api:page[@position="last"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].get('href')


    while mynext <> last:
        user_return, mynext = cris.parseUserListPage(mynext,url)
        do_inCites_users(user_return)

# Publications management 
def parsePublicationList(xmlFile): 
    mynext = xmlFile 
    tree = etree.parse(xmlFile) 
    root = tree.getroot()
    last = root.xpath('//api:page[@position="last"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].get('href')


    while mynext <> last:
        pub_return, mynext = cris.parsePublicationListPage(mynext)
        do_inCites_publications(pub_return)

# takes a list of users, prints incites extract
def do_inCites_users(list):
    for user in list:
        symp_id = user['user-data']['symp-id']
        prop_id = user['user-data']['prop-id']
        lastname = user['user-data']['last-name']
        firstname = user['user-data']['first-name']
        email = user['user-data']['email-address']
	try:
            primarygroup = user['user-feed-data']['primarygroup']
            arrive_date = user['user-feed-data']['arrive-date']
            leave_date = user['user-feed-data']['leave-date']
            ou_1 = user['user-feed-data']['ou-1']
            ou_2 = user['user-feed-data']['ou-2']
    
    
            if leave_date == '':
                print symp_id + "," + lastname + "," + firstname + "," + email + ',"St. George\'s, University of London",' + primarygroup + "," + "Cranmer Terrace" + "," + "London" + "," + "United Kingdom" + "," + "SW17 0RE" + "," + ou_1 + "," + arrive_date[0:4] + "," + leave_date[0:4]
                print symp_id + "," + lastname + "," + firstname + "," + email + ',"St. George\'s, University of London",' + primarygroup + "," + "Cranmer Terrace" + "," + "London" + "," + "United Kingdom" + "," + "SW17 0RE" + "," + ou_2 + "," + arrive_date[0:4] + "," + leave_date[0:4]
        except Exception, err:
            print "User " + symp_id + " does not have feed data"



# takes a list of publications, prints incites extract
def do_inCites_publications(list):
    #[employeeID,lastName,firstName,other-authors,title,source-title,starting-page]
    for pub in list:
        item = pub['pub']

        # procedure to get the authors
        rel = pub['rel']
        users = rel['users']
        authors = []


        employeeID = ""
        lastName = ""
        firstName = ""
        otherAuthors = ""
        i = 0
        
        for author in users:
            proprietaryId = author['proprietary-id']
            username = author['username']
            href = author['href']
            authorinfo = cris.parseUser(href)
            if i == 0:
                employeeID = author['id']
                lastName = authorinfo['last-name']
                firstName = authorinfo['first-name']
            else:
                otherAuthors = authorinfo['last-name'] + ", " + authorinfo['first-name'] + ";" + otherAuthors
            i = i + 1

        if otherAuthors <> "":
            otherAuthors = otherAuthors[:-1]
        # end of procedure to get the authors

        records = item['records']
        puburl = item['puburl']
        # select best available record (manual, pubmed, wos, woslite)
        recordindex = 100
        winningrecord = dict()

        for record in records:
            if int(record['source-id']) < recordindex:
                recordindex = int(record['source-id'])
                winningrecord = record

        #     pub contains the whole publication        
        #     winningrecord contains the record we're meant to work on
        #     rel contains the relationships
        #     users contain user info from the relationships
        #     authors contains all the authors
        #print winningrecord
        try:
            year = winningrecord['date']['{http://www.symplectic.co.uk/publications/api}year']
        except Exception, err:
            year = ""


        #print employeeID+","+lastName+","+firstName+",,"+otherAuthors+",,"+winningrecord['title'].encode('utf-8').replace('\n', '').replace('\r', '')+","+winningrecord['journal'].encode('utf-8').replace('\n', '').replace('\r', '')+","+winningrecord['volume']+","+winningrecord['issue']+","+winningrecord['begin-page']+","+winningrecord['issn']+",,,"+year+","+winningrecord['doi'].encode('utf-8')+",,,"

#        print "\""+employeeID+"\""+","+"\""+lastName+"\""+","+"\""+firstName+"\""+",,"+"\""+otherAuthors+"\""+",,"+"\""+winningrecord['title'].encode('utf-8').replace('\n', '').replace('\r', '')+"\""+","+"\""+winningrecord['journal'].encode('utf-8').replace('\n', '').replace('\r', '')+","+"\""+winningrecord['volume']+"\""+","+"\""+winningrecord['issue']+"\""+","+"\""+winningrecord['begin-page']+"\""+","+"\""+winningrecord['issn']+"\""+",,,"+"\""+year+"\""+","+"\""+winningrecord['doi'].encode('utf-8')+"\""+",,,"
        print str(len(records))+","+winningrecord['source-id']+","+puburl+","+employeeID+","+lastName+","+firstName+","+winningrecord['title'].encode('utf-8').replace('\n', '').replace('\r', '')+","+winningrecord['journal'].encode('utf-8').replace('\n', '').replace('\r', '')+","+winningrecord['begin-page']+","+year

parseUserList(cris_url + ":" + cris_port +"/publications-api/objects?categories=users",cris_url + ":" + cris_port)
#parsePublicationList(cris_url + ":" + cris_port +"/publications-api/objects?categories=publications")

