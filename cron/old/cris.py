import lxml
import urllib2
import libxml2
from lxml import etree
from StringIO import StringIO
from xml.dom.minidom import parse, parseString

# takes a user list page as input
# returns data about all publications in that page and next page
def parseUserListPage(xmlFile,url):
    tree = etree.parse(xmlFile) 
    root = tree.getroot()
    entries = root.xpath('//def:entry',namespaces={'def':'http://www.w3.org/2005/Atom',})

    next = root.xpath('//api:page[@position="next"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].get('href')
    last = root.xpath('//api:page[@position="last"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].get('href')

    user_return = []

    for entry in entries:
        user_uri = entry.xpath('def:link[@rel="alternate"]',namespaces={'def':'http://www.w3.org/2005/Atom',})[0].get('href')
        this_user = dict()
        this_user['uri'] = user_uri
        user_data = parseUser(user_uri,url)
	user_feed_data = dict()
	if user_data['prop-id'] is not None:
  	    feed_uri = url+ "/publications-api/user-feed/users/" + user_data['prop-id']
	    user_feed_data = parseUserFeed(feed_uri)
	this_user['user-data'] = user_data
	this_user['user-feed-data'] = user_feed_data
        user_return.append(this_user)

    return user_return, next

# parses http://cris.sgul.ac.uk:8090/publications-api/users/1001
def parseUser(xmlFile,url):
    tree = etree.parse(xmlFile)
    root = tree.getroot()
    entries = root.xpath('//def:entry',namespaces={'def':'http://www.w3.org/2005/Atom',})
    out = dict()
    for entry in entries:
        link = entry.xpath('def:link[@rel="alternate"]',namespaces={'def':'http://www.w3.org/2005/Atom',})[0].get('href')
        lastname = entry.xpath('api:object/api:last-name',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
        firstname = entry.xpath('api:object/api:first-name',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
        email = entry.xpath('api:object/api:email-address',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
 	user = entry.xpath('api:object[@category="user"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0]
	prop_id = user.get('proprietary-id')
 	symp_id = user.get('id')
        link = entry.xpath('def:link[@rel="alternate"]',namespaces={'def':'http://www.w3.org/2005/Atom',})[0].get('href')
        relationships = entry.xpath('api:object/api:relationships',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0]
	out['prop-id'] = prop_id
        out['symp-id'] = symp_id
	out['last-name'] = lastname
	out['first-name'] = firstname
	out['email-address'] = email
    return out

# parses http://cris.sgul.ac.uk:8090/publications-api/user-feed/users/E107130
def parseUserFeed(xmlFile):
    returnlist = []
    tree = etree.parse(xmlFile)
    e = etree.XPathEvaluator(tree)
    e.register_namespace('api', 'http://www.symplectic.co.uk/publications/api')
    out = dict()
    try:
        primarygroup = e('//api:primary-group-descriptor')[0].text
    except Exception, err:
        primarygroup = ""
    out['primarygroup'] = primarygroup
    try:
        isacademic = e('//api:is-academic')[0].text
    except Exception, err:
        isacademic = ""
    out['isacademic'] = isacademic
    try:
        arrive_date = e('//api:arrive-date')[0].text
    except Exception, err:
        arrive_date = ""
    out['arrive-date'] = arrive_date
    try:
        leave_date = e('//api:leave-date')[0].text
    except Exception, err:
        leave_date = ""
    out['leave-date'] = leave_date
    try:
        dateofbirth = e('//api:generic-field-03')[0].text
    except Exception, err:
        dateofbirth = ""
    out['dateofbirth'] = dateofbirth
    try:
        ou_1 = e('//api:generic-field-04')[0].text
    except Exception, err:
        ou_1 = ""
    out['ou-1'] = ou_1
    try:
        ou_2 = e('//api:generic-field-05')[0].text
    except Exception, err:
        ou_2 = ""
    out['ou-2'] = ou_2
    try:
        jobtitle = e('//api:generic-field-06')[0].text
    except Exception, err:
        jobtitle = ""
    out['jobtitle'] = jobtitle
    try:
        ft = e('//api:generic-field-07')[0].text
    except Exception, err:
        ft = ""
    out['ft'] = ft
    try:
        perm_ft_text = e('//api:generic-field-15')[0].text
    except Exception, err:
        perm_ft_text = ""
    out['perm_ft_text'] = perm_ft_text
    return out

#a publication list page as input
# returns data about all publications in that page and next page
def parsePublicationListPage(xmlFile):
    tree = etree.parse(xmlFile)
    root = tree.getroot()
    entries = root.xpath('//def:entry',namespaces={'def':'http://www.w3.org/2005/Atom',})
 
    next = root.xpath('//api:page[@position="next"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].get('href')
    last = root.xpath('//api:page[@position="last"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].get('href')


    pub_return = []

    for entry in entries:
        title = entry.xpath('def:title',namespaces={'def':'http://www.w3.org/2005/Atom',})[0].text
        pub_uri = entry.xpath('def:link[@rel="alternate"]',namespaces={'def':'http://www.w3.org/2005/Atom',})[0].get('href')
        pub_rel_uri = entry.xpath('def:link[@rel="related"]',namespaces={'def':'http://www.w3.org/2005/Atom',})[0].get('href')
        pub_data = parsePublication(pub_uri)
        pub_rel = parsePublicationRel(pub_rel_uri)

        this_pub = dict()
        this_pub['pub'] = pub_data
        this_pub['rel'] = pub_rel
        pub_return.append(this_pub)

    return pub_return, next


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
        out['id'] = entry.xpath('api:object[@category="publication"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].get('id')
        records = entry.xpath('api:object/api:records',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0]
	type = entry.xpath('api:object[@category="publication"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].get('type-id')
        relationships = entry.xpath('api:object/api:relationships',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0]
	out['type'] = type
        out['relationships'] = relationships.get('href')
	

	# TODO this way I only get the first - I guess it's good enough but you could do an aggregation of all the working copies
	repo = "NONE"
	try:
		repositoryitem = entry.xpath('api:object/api:repository-items/api:repository-item',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0]
		repo = repositoryitem.xpath('api:public-url',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})
		repo = repo[0].text
		# TODO go to repo and get item. There are multiple links. Probably the unique one is in
		# <meta name="DC.identifier" content="http://openaccess.sgul.ac.uk/101167/7/licence.txt" />
	except Exception, err:
		pass

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
                parent_title = record.xpath('api:native/api:field[@name="parent-title"]/api:text',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                if parent_title is None:
                    parent_title = ""
            except Exception, err:
                parent_title = ""
            recorddict['parent_title'] = parent_title

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
            recorddict['begin-page'] = beginpage

            try:
                endpage = record.xpath('api:native/api:field[@name="pagination"]/api:pagination/api:end-page',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0].text
                if endpage is None:
                    endpage = ""
            except Exception, err:
                endpage = ""
            recorddict['end-page'] = endpage

            try:
                subtypes = record.xpath('api:native/api:field[@name="types"]/api:items/api:item',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})
	        itemslist = []
                for item in subtypes:
                    i_text = item.text
                    itemslist.append(i_text)
            except Exception, err:
                itemslist = []

            recorddict['subtypes'] = itemslist

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
    out['puburl'] = xmlFile
    out['repo'] = repo

    return out

def parsePublicationRel(xmlFile):
    tree = etree.parse(xmlFile)
    root = tree.getroot()
    entries = root.xpath('//def:entry',namespaces={'def':'http://www.w3.org/2005/Atom',})
    out = dict()

    
    # TODO will need completion, now just getting the essential for inCites
    authorslist = []
    for entry in entries:
        user = entry.xpath('api:relationship/api:related/api:object[@category="user"]',namespaces={'api':'http://www.symplectic.co.uk/publications/api'})[0]
        author = dict()
        author['id'] = user.get('id')
        author['proprietary-id'] = user.get('proprietary-id')
        author['username'] = user.get('username')
        author['href'] = user.get('href')
        authorslist.append(author)

    out['pubrel'] = xmlFile
    out['users'] = authorslist

    return out


