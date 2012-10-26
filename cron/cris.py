import lxml, json
import urllib2
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
    tree = etree.parse(xmlFile)
    e = etree.XPathEvaluator(tree, namespaces={'def':'http://www.w3.org/2005/Atom'})
    #e.register_namespace('def','http://www.w3.org/2005/Atom')
    e.register_namespace('api', 'http://www.symplectic.co.uk/publications/api')


   # file = urllib2.urlopen(xmlFile)
   # data = file.read()
   # file.close()
   # dom = parseString(data)

    #entries = dom.getElementsByTagName('entry')

    #for entry in entries:
     #   pub_id = (entry.getElementsByTagName('id'))[0].childNodes[0].data
     #   title = (entry.getElementsByTagName('title'))[0].childNodes[0].data
     #   links = (entry.getElementsByTagName('link'))
    #   for link in links:
    #        rel = link.getAttribute('rel')
    #        if rel == 'alternate':
    #            pub_url = link.getAttribute('href')
    #        elif rel == 'related' and link.getAttribute('title') == 'Relationships':
    #            pub_rel_url = link.getAttribute('href')

    #    print pub_url
    #publicationData = parsePublicationUrl(pub_url) #).encode('ascii','xmlcharrefreplace')

    entries = e('//def:entry')
    for entry in entries:
        #print (entry.findall('*'))[0].text
        mypath = tree.getpath(entry) + "/category"
	print mypath
	category = e(mypath)
        #print category
        
    #cate = e('//def:entry[1]/def:category[1]')[0].get('scheme')
    #print '/def:feed/def:entry[1]/def:category[1]'

    # get next/last     
    next = e('//api:page[@position="next"]')[0].get('href')
    last = e('//api:page[@position="last"]')[0].get('href')
    #if next <> last:
    #    parsePublicationList(next)

def parsePublicationUrl(xmlFile):

    file = urllib2.urlopen(xmlFile)
    data = file.read()
    file.close()
    dom = parseString(data)


    return []


def parsePublicationUrlXslt(xmlFile):
    xml_input = etree.parse(xmlFile)
    xslt_root = etree.parse("symplectic-to-vivo.datamap.xsl")
    transform = etree.XSLT(xslt_root)
    rdf_xml = transform(xml_input)
    
    dom = parseString(str(rdf_xml))

    employeeID = ""
    lastName = ""
    firstName = ""
    middleName = ""
    otherauthors = ""
    reftype = ""
    title = getValue(dom,'core:Title')
    sourcetitle = ""
    volume = getValue(dom,'bibo:volume')
    number = ""
    startingpage = getValue(dom,'bibo:pageStart')
    ISSN = getValue(dom,'bibo:ISSN')
    dateday = ""
    datemonth = ""
    dateyear = ""
    electronicresourcenum = getValue(dom,'bibo:doi')
    accessionnum = ""
    puburl = ""

    list = [employeeID,lastName,firstName,middleName,otherauthors,reftype,title,sourcetitle,volume,number,startingpage,ISSN,dateday,datemonth,dateyear,electronicresourcenum,accessionnum,puburl]
    do_inCites_publications(list)
 
    return ""

def getValue(dom,name):
    try:
        return dom.getElementsByTagName(name)[0].childNodes[0].nodeValue
    except:
        return ""


def do_inCites_publications(list):
    #[employeeID,lastName,firstName,middleName,other-authors,ref-type,title,source-title,volume,number,starting-page,ISSN,date-day,date-month,date-year,electronic-resource-num,accession-num,pub-url]

    employeeID = list.pop(0)
    lastName = list.pop(0)
    firstName = list.pop(0)
    middleName = list.pop(0)
    otherauthors = list.pop(0)
    reftype = list.pop(0)
    title = list.pop(0)
    sourcetitle = list.pop(0)
    volume = list.pop(0)
    number =  list.pop(0)
    startingpage = list.pop(0)
    ISSN =  list.pop(0)
    dateday = list.pop(0)
    datemonth = list.pop(0)
    dateyear = list.pop(0)
    electronicresourcenum = list.pop(0)
    accessionnum = list.pop(0)
    puburl = list.pop(0)

    
    print employeeID + "," + lastName + "," + firstName + "," + middleName + "," + otherauthors + "," + reftype + "," + title + "," + sourcetitle + "," + volume + "," + startingpage + "," + ISSN + "," + dateday + "," + datemonth + "," + dateyear + "," + electronicresourcenum

#read settings, load url, parse resulting text
settings_text = open("config.json", "r").read()
settings = json.loads(settings_text)
cris_url = settings["cris"]["url"]
cris_port = settings["cris"]["port"]

#parseUserList(cris_url + ":" + cris_port +"/publications-api/objects?categories=users")
parsePublicationList(cris_url + ":" + cris_port +"/publications-api/objects?categories=publications")
