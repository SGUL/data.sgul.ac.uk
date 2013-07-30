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
def parsePublicationList(xmlFile,url): 
    mynext = xmlFile 
    tree = etree.parse(xmlFile) 
    root = tree.getroot()
    last = root.xpath('//api:page[@position="last"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].get('href')


    while mynext <> last:
        pub_return, mynext = cris.parsePublicationListPage(mynext)
        do_inCites_publications(pub_return,url)

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
def do_inCites_publications(list,url):
    #[employeeID,lastName,firstName,other-authors,title,source-title,starting-page]
    for pub in list:
        item = pub['pub']

        # procedure to get the authors
        rel = pub['rel']
        users = rel['users']
	type = item['type']
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
            authorinfo = cris.parseUser(href,url)
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
	repo = item['repo']
	id = item['id']
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

	
	if repo <> "NONE" and repo <> None and len(repo)>0:
	    filename = "output/pub_" + id + ".rdf"
	    f = open(filename, 'w')
	    rdfprint = ""
 	    # Preamble
	    rdfprint = rdfprint + """<?xml version="1.0" encoding="UTF-8"?>
                     <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                              xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
                              xmlns:bibo="http://purl.org/ontology/bibo/"
			      xmlns:sgul="http://sgul.ac.uk/ontology/lib/"
                              xmlns:vivo="http://vivoweb.org/ontology/core#">"""
	    # General info
	    rdfprint = rdfprint +  """<rdf:Description rdf:about=\""""+puburl+"""\">
      			<rdf:type rdf:resource="http://purl.org/ontology/bibo/AcademicArticle"/>
		        <rdf:type rdf:resource="http://purl.org/ontology/bibo/Article"/>
		        <rdf:type rdf:resource="http://purl.org/ontology/bibo/Document"/>
		        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>
		        <rdfs:label>"""+winningrecord['title'].encode('utf-8').replace('\n', '').replace('\r', '')+"""</rdfs:label>
		        <bibo:abstract>"""+winningrecord['abstract'].encode('utf-8').replace('\n', '').replace('\r', '')+"""</bibo:abstract>
		        <bibo:doi>"""+winningrecord['doi']+"""</bibo:doi>
      			<bibo:authorList>"""+lastName+","+firstName+";"+otherAuthors+"""</bibo:authorList>
         	        <vivo:dateTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">"""+year+"""</vivo:dateTime>
			<sgul:repositoryLink rdf:resource=\""""+repo+"""\"/>
		     </rdf:Description>"""


	    # Closing 
            rdfprint = rdfprint + """</rdf:RDF>"""
	    f.write(rdfprint)
	    f.close()

	   # Generate CSV TODO
	   # Generate JSON TODO


#parseUserList(cris_url + ":" + cris_port +"/publications-api/objects?categories=users",cris_url + ":" + cris_port)
parsePublicationList(cris_url + ":" + cris_port +"/publications-api/objects?categories=publications", cris_url + ":" + cris_port)

