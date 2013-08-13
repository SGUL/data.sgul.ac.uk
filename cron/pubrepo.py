import cris
from lxml import etree
import json
import tarfile

#read settings, load url, parse resulting text
settings_text = open("config.json", "r").read()
settings = json.loads(settings_text)
cris_url = settings["cris"]["url"]
cris_port = settings["cris"]["port"]


# Publications management 
def parsePublicationList(xmlFile,url): 
    mynext = xmlFile 
    tree = etree.parse(xmlFile) 
    root = tree.getroot()
    last = root.xpath('//api:page[@position="last"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].get('href')


    while mynext <> last:
        pub_return, mynext = cris.parsePublicationListPage(mynext)
        do_inCites_publications(pub_return,url)



# takes a list of publications, prints incites extract
def do_inCites_publications(list,url):
    #[employeeID,lastName,firstName,other-authors,title,source-title,starting-page]
    members = []
    jsonprint = ""
    csvprint = "URLTitle,DOI,AuthorList,Year,RepositoryURL"

    # Generate CSV
    csvname = "output/publications.csv"
    c = open(csvname, 'w')
    
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
        try:
            year = winningrecord['date']['{http://www.symplectic.co.uk/publications/api}year']
        except Exception, err:
            year = ""

        if repo <> "NONE" and repo <> None and len(repo)>0:
            filename = "output/pub_" + id + ".rdf"
            members.append(filename)
            f = open(filename, 'w')
    	    rdfprint = ""
     	    # Preamble
    	    rdfprint = rdfprint + """<?xml version="1.0" encoding="UTF-8"?>
                         <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                                  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
                                  xmlns:bibo="http://purl.org/ontology/bibo/"
    			      xmlns:sgul="http://data.sgul.ac.uk/ontology/lib/"
                                  xmlns:vivo="http://vivoweb.org/ontology/core#">"""

            #DEBUG
            # print "puburl "
            # print puburl
            # print "title " 
            # print winningrecord['title'].encode('utf-8').replace('\n', '').replace('\r', '')
            # print "abstract "
            # print winningrecord['abstract'].encode('utf-8').replace('\n', '').replace('\r', '')
            # print "doi"
            # print winningrecord['doi']
            # print "authors"
            # print lastName+","+firstName+";"+otherAuthors
            # print "date" 
            # print year
            # print "repo"
            # print repo

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

            csvprint = puburl + "," + winningrecord['title'].encode('utf-8').replace('\n', '').replace('\r', '') + "," + winningrecord['doi'] + "," + lastName+","+firstName+";"+otherAuthors+ "," + year + "," + repo + "\n"
            c.write(csvprint)
            #jsonprint 
    	    # Closing and writing RDF
            rdfprint = rdfprint + """</rdf:RDF>"""
    	    f.write(rdfprint)
    	    f.close()

    
    # Close CSV
    c.close()
    
    # Generate JSON TODO
    jsonname = "output/publications.json"
    j = open(jsonname, 'w')
    j.write(jsonprint)
    j.close()

    # Generate RDF-XML archive
    tar = tarfile.open("output/publicationsrdf.tar", "w")
    for name in members:
        path = name
        tar.add(path)
    tar.close()


parsePublicationList(cris_url + ":" + cris_port +"/publications-api/objects?categories=publications", cris_url + ":" + cris_port)

