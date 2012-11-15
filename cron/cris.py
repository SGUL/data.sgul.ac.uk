import lxml, json
import urllib2
import libxml2
from lxml import etree
from StringIO import StringIO
from xml.dom.minidom import parse, parseString

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
    if next <> last:
        parseUserList(next)

def parseUser(xmlFile):
    tree = etree.parse(xmlFile)
    e = etree.XPathEvaluator(tree)
    e.register_namespace('api', 'http://www.symplectic.co.uk/publications/api')
    # get all users in this page
    users = e('//api:object[@category="user"]')
    for user in users:
        prop_id = user.get("proprietary-id")
        symp_id = user.get("id")
        username = user.get("username")

        href = user.get("href")
        type = user.get("type-id")
        current = e('//api:is-current-staff')[0].text
       
        try:
            title = e('//api:title')[0].text
        except Exception, err:
            title = ""

        lastname = e('//api:last-name')[0].text
        firstname = e('//api:first-name')[0].text
        email = e('//api:email-address')[0].text
        result = []
        if prop_id <> None:
            hr_feed_url = (cris_url + ":" + cris_port +"/publications-api/user-feed/users/"+prop_id)
            result = parseUserFeed(hr_feed_url)
            finalres = [symp_id, prop_id, lastname, firstname, email, result.pop(0), result.pop(0), result.pop(0), result.pop(0), result.pop(0), result.pop(0), result.pop(0), result.pop(0), result.pop(0), result.pop(0)]
            # TODO move this to the caller - make it a function over the set, rather than over the single entry
            do_inCites_authors(finalres)


def parseUserFeed(xmlFile):
    returnlist = []
    tree = etree.parse(xmlFile)
    e = etree.XPathEvaluator(tree)
    e.register_namespace('api', 'http://www.symplectic.co.uk/publications/api')
    # get all users in this page
    try:
        primarygroup = e('//api:primary-group-descriptor')[0].text
    except Exception, err:
        primarygroup = ""
    try:
        isacademic = e('//api:is-academic')[0].text
    except Exception, err:
        isacademic = ""
    try:
        arrive_date = e('//api:arrive-date')[0].text
    except Exception, err:
        arrive_date = ""
    try:
        leave_date = e('//api:leave-date')[0].text
    except Exception, err:
        leave_date = ""
    try:
        dateofbirth = e('//api:generic-field-03')[0].text
    except Exception, err:
        dateofbirth = ""
    try:
        ou_1 = e('//api:generic-field-04')[0].text
    except Exception, err:
        ou_1 = ""
    try:
        ou_2 = e('//api:generic-field-05')[0].text
    except Exception, err:
        ou_2 = ""
    try:
        jobtitle = e('//api:generic-field-06')[0].text
    except Exception, err:
        jobtitle = ""
    try:
        ft = e('//api:generic-field-07')[0].text
    except Exception, err:
        ft = ""
    try:
        perm_ft_text = e('//api:generic-field-15')[0].text
    except Exception, err:
        perm_ft_text = ""
    returnlist = [primarygroup, isacademic, arrive_date, leave_date, dateofbirth, ou_1, ou_2, jobtitle, ft, perm_ft_text]
    return returnlist

# prints author export for in_cites
def do_inCites_authors(list):
    #[symp_id, prop_id, lastname, firstname, email,primarygroup, isacademic, arrive_date, leave_date, dateofbirth, ou_1, ou_2, jobtitle, ft, perm_ft_text]
    symp_id = list.pop(0)
    prop_id = list.pop(0)
    lastname = list.pop(0)
    firstname = list.pop(0)
    email = list.pop(0)
    primarygroup = list.pop(0)
    isacademic = list.pop(0)
    arrive_date = list.pop(0)
    leave_date = list.pop(0)
    dateofbirth = list.pop(0)
    ou_1 = list.pop(0)
    ou_2 = list.pop(0)
    jobtitle = list.pop(0)
    ft = list.pop(0)
    perm_ft_text = list.pop(0)
    
    if leave_date == '':
        print symp_id + "," + lastname + "," + firstname + "," + email + ',"St. George\'s, University of London",' + primarygroup + "," + "Cranmer Terrace" + "," + "London" + "," + "United Kingdom" + "," + "SW17 0RE" + "," + ou_1 + "," + arrive_date[0:4] + "," + leave_date[0:4]
        print symp_id + "," + lastname + "," + firstname + "," + email + ',"St. George\'s, University of London",' + primarygroup + "," + "Cranmer Terrace" + "," + "London" + "," + "United Kingdom" + "," + "SW17 0RE" + "," + ou_2 + "," + arrive_date[0:4] + "," + leave_date[0:4]





# Publications management
def parsePublicationList(xmlFile):
    mynext = xmlFile
    tree = etree.parse(xmlFile)
    root = tree.getroot()
    last = root.xpath('//api:page[@position="last"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].get('href')

    all_pubs = []

    while mynext <> last:
        pub_data_list, pub_rel_list, mynext = parsePublicationListPage(mynext) 
        all_pubs = all_pubs + pub_data_list

# takes a publication list page as input
# returns data about all publications in that page and next page
def parsePublicationListPage(xmlFile):
    tree = etree.parse(xmlFile)
    root = tree.getroot()
    entries = root.xpath('//def:entry',namespaces={'def':'http://www.w3.org/2005/Atom',})
 
    next = root.xpath('//api:page[@position="next"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].get('href')
    last = root.xpath('//api:page[@position="last"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].get('href')
    pub_data_list = []
    pub_rel_list = []
    for entry in entries:
        title = entry.xpath('def:title',namespaces={'def':'http://www.w3.org/2005/Atom',})[0].text
        pub_uri = entry.xpath('def:link[@rel="alternate"]',namespaces={'def':'http://www.w3.org/2005/Atom',})[0].get('href')
        pub_rel_uri = entry.xpath('def:link[@rel="related"]',namespaces={'def':'http://www.w3.org/2005/Atom',})[0].get('href')
        pub_data = parsePublication(pub_uri)
        pub_rel = parsePublicationRel(pub_rel_uri)
        pub_data_list.append(pub_data)
        pub_rel_list.append(pub_rel)
    return pub_data_list, pub_rel_list, next


# this parses the main publication url
# e.g. http://my.symplectic.instance:8090/publications-api/publications/78823
def parsePublication(xmlFile):
    tree = etree.parse(xmlFile)
    root = tree.getroot()
    entries = root.xpath('//def:entry',namespaces={'def':'http://www.w3.org/2005/Atom',})
    out = dict()
    for entry in entries:
        link = entry.xpath('def:link[@rel="alternate"]',namespaces={'def':'http://www.w3.org/2005/Atom',})[0].get('href')
        out['link'] = link
        records = entry.xpath('api:object/api:records',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0]
        # there can be multiple records for each publication (web of science, pub med, etc...)
        recordslist = []
        for record in records:
            recorddict = dict()
            sourcename = record.get('source-name')
            recorddict['source-name'] = sourcename
            sourceid = record.get('source-id')
            recorddict['source-id'] = sourceid
            sourcedisplayname = record.get('source-display-name')
            recorddict['source-display-name'] = sourcedisplayname
            idatsource = record.get('id-at-source')
            recorddict['id-at-source'] = idatsource
            # gathering available fields
            try: 
                abstract = record.xpath('api:native/api:field[@name="abstract"]/api:text',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
		if abstract is None:
                    abstract = ""
            except Exception, err:
                abstract = ""
            
            recorddict['abstract'] = abstract

            authors = record.xpath('api:native/api:field[@name="authors"]/api:people/api:person',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})
            authorslist = []
            for author in authors:
                try:
                    lastname = author.xpath('api:last-name',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                    if lastname is None:
                        lastname = ""
                except Exception, err:
                    lastname = ""
                
                try:
                    initials = author.xpath('api:initials',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                    if initials is None:
                        initials = ""
                except Exception, err:
                    initials = ""

                formattedname = lastname + ", " + initials
                authorslist.append(formattedname)

            recorddict['authors'] = authorslist

            try:
                doi = record.xpath('api:native/api:field[@name="doi"]/api:text',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                if doi is None:
                    doi = ""
            except Exception, err:
                doi = ""       
            recorddict['doi'] = doi 
         
            try:
                issn = record.xpath('api:native/api:field[@name="issn"]/api:text',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                if issn is None:
                    issn = ""
            except Exception, err:
                issn = ""          
            recorddict['issn'] = issn
      
            try:
                issue = record.xpath('api:native/api:field[@name="issue"]/api:text',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                if issue is None:
                    issue = ""
            except Exception, err:
                issue = ""           
            recorddict['issue'] = issue
     
            try:
                journal = record.xpath('api:native/api:field[@name="journal"]/api:text',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text 
                if journal is None:
                    journal = ""
            except Exception, err:
                journal = ""           
            recorddict['journal'] = journal
              

            
            try:
                keywords = record.xpath('api:native/api:field[@name="keywords"]/api:keywords/api:keyword',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})
	        keywordslist = []
                for keyword in keywords:
                    k_text = keyword.text
                    keywordslist.append(k_text)
            except Exception, err:
                keywordslist = []
            recorddict['keywords'] = keywordslist

            try:
                language = record.xpath('api:native/api:field[@name="language"]/api:text',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                if language is None:
                    language = ""
            except Exception, err:
                language = ""                
            recorddict['language'] = language

            try:
                location = record.xpath('api:native/api:field[@name="location"]/api:text',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                if location is None:
                    location = ""
            except Exception, err:
                location = ""                
            recorddict['location'] = location

            try:
                title = record.xpath('api:native/api:field[@name="title"]/api:text',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                if title is None:
                    title = ""
            except Exception, err:
                title = ""
            recorddict['title'] = title

            try:
                volume = record.xpath('api:native/api:field[@name="volume"]/api:text',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                if volume is None:
                    volume = ""
            except Exception, err:
                volume = ""
            recorddict['volume'] = volume

            try:
                pii = record.xpath('api:native/api:field[@name="pii"]/api:text',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                if pii is None:
                    pii = ""
            except Exception, err:
                pii = ""
            recorddict['pii'] = pii

            try:
                beginpage = record.xpath('api:native/api:field[@name="pagination"]/api:pagination/api:begin-page',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                if beginpage is None:
                    beginpage = ""
            except Exception, err:
                beginpage = ""
            recorddict['beginpage'] = beginpage

            try:
                endpage = record.xpath('api:native/api:field[@name="pagination"]/api:pagination/api:end-page',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                if endpage is None:
                    endpage = ""
            except Exception, err:
                endpage = ""
            recorddict['endpage'] = endpage


            try:
                subtypes = record.xpath('api:native/api:field[@name="types"]/api:items/api:item',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})
	        imtemslist = []
                for item in subtypes:
                    i_text = item.text
                    itemslist.append(i_text)
            except Exception, err:
                itemslist = []

#            recorddict['subtypes'] = itemslist TODO

            try:
                addresses = record.xpath('api:native/api:field[@name="addresses"]/api:addresses/api:address',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})
                addresslist = []
                for address in addresses:
                    lineslist = []
                    lines = address.xpath('api:line',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})
                    for line in lines:
                        l_text = line.text
                        lineslist.append(l_text)
                    addresslist.append(lineslist)

            except Exception, err:
                addresslist = []

            recorddict['addresses'] = addresslist

            try:
                date = record.xpath('api:native/api:field[@name="publication-date"]/api:date/api:*',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})
                datelist = dict()
                for item in date:
                    i_tag = item.tag
                    i_text = item.text
                    datelist[i_tag] = i_text
            except Exception, err:
                datelist = []
            recorddict['date'] = datelist

                
            recordslist.append(recorddict)

    out['records'] = recordslist

    return out

def parsePublicationRel(xmlFile):
    tree = etree.parse(xmlFile)
    root = tree.getroot()
    entries = root.xpath('//def:entry',namespaces={'def':'http://www.w3.org/2005/Atom',})
    out = []

    return out




def do_inCites_publications():
    #[employeeID,lastName,firstName,middleName,other-authors,ref-type,title,source-title,volume,number,starting-page,ISSN,date-day,date-month,date-year,electronic-resource-num,accession-num,pub-url]
    pubdictlist = parsePublicationList(cris_url + ":" + cris_port +"/publications-api/objects?categories=publications")
  
    for pubdict in pubdictlist:
        title = pubdict['list']
        print title

    

#    employeeID = 'TODO'
#    lastName = pubdict
#    firstName = 
#    middleName = 
#    otherauthors = 
#    reftype = 
#    title = 
#    sourcetitle = 
#    volume = 
#    number = 
#    startingpage = 
#    ISSN = 
#    dateday = 
#    datemonth = 
#    dateyear = 
#    electronicresourcenum = 
#    accessionnum = 
#    puburl = 

    
#    print employeeID + "," + lastName + "," + firstName + "," + middleName + "," + otherauthors + "," + reftype + "," + title + "," + sourcetitle + "," + volume + "," + startingpage + "," + ISSN + "," + dateday + "," + datemonth + "," + dateyear + "," + electronicresourcenum

#read settings, load url, parse resulting text
settings_text = open("config.json", "r").read()
settings = json.loads(settings_text)
cris_url = settings["cris"]["url"]
cris_port = settings["cris"]["port"]

#parseUserList(cris_url + ":" + cris_port +"/publications-api/objects?categories=users")
do_inCites_publications()
