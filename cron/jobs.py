import json
from StringIO import StringIO

import urllib2
from BeautifulSoup import BeautifulSoup


def downloadJobDetails(url):
    jobs_detail_url = settings["jobs"]["url"]  + "/" + url
    job = (urllib2.urlopen(jobs_detail_url)).read()
    soup = BeautifulSoup(job)
    maincontent_element = soup.findAll(attrs={'id': 'leftpanel'})[0]

    title = ""
    unit = ""
    reference = ""
    closing = ""
    interview = ""
    salary = ""
    description = ""
    doc_file_url = ""

    job_dict = dict()
    

    soup_2 = BeautifulSoup(str(maincontent_element))
    msonormal_elements = soup_2.findAll('strong')
    for desc_elem in msonormal_elements:
        contents = str(desc_elem.contents)
        sib = desc_elem.nextSibling
        if 'Reference' in contents:
	    reference = str(sib)
        elif 'Closing Date' in contents:
            closing = str(sib)
        elif 'Interview Date' in contents:
            interview = str(sib)
        elif 'Salary' in contents:
            salary = str(sib)
        #TODO this needs cleaning from unicode, but it's not really needed
        #elif 'font style' in contents:
        #    soup_contents = BeautifulSoup(str(contents))
        #    title = str(soup_contents.text)
        #    job_dict['Title'] = title
        #else:
        #    unit = str(contents)
        #    job_dict['Unit'] = unit
    description = soup.findAll(attrs={'name': 'j748'})
    job_dict['Reference'] = reference
    job_dict['Closing'] = closing
    job_dict['Interview'] = interview
    job_dict['Salary'] = salary
            
    return job_dict





#read settings, load url, parse resulting text
settings_text = open("config.json", "r").read()
settings = json.loads(settings_text)
jobs_url = settings["jobs"]["url"] + "/" + settings["jobs"]["list"]


# get page and soupify
jobs = (urllib2.urlopen(jobs_url)).read()
soup = BeautifulSoup(jobs)
printHide_element = soup.findAll(attrs={'class': 'printHide'})[0]
soup_div = BeautifulSoup(str(printHide_element))

type = ""
topic = ""

# output RDF
print '<?xml version="1.0"?>'
print ' '
print '<vacancy:RDF'
print '<rdfs:RDF<http://www.w3.org/2000/01/rdf-schema#> '
print '  xmlns:vacancy http://purl.org/openorg/vacancy/'

# navigate in each element of the page
for elem in soup_div.findAll():
    tagname = elem.name

    if tagname == "h2":
        type = elem.contents[0]
    elif tagname == "strong":
        topic = elem.contents[0]
    elif tagname == "li":
        href = elem.a['href']
        title = elem.a['title']
        # Now (type,topic,href,title) is a description of the job
	# ready to download further information
        jobs_data = downloadJobDetails(href)
       

        #print "Title: " + title
        #print "Area: " + topic
        #print "Unit: " + type
        #print "Ref.: " + jobs_data['Reference']
        #print "Closing: " + jobs_data['Closing']
        #print "Interview: " + jobs_data['Interview']
        #print "Salary: " + jobs_data['Salary']
        #print "Href: " + settings["jobs"]["url"]  + "/" + href
        #print " "

	#Production of the RDF
        print '  <rdfs:label>' + title + '</rdfs:label>'
	print '  <vacancy:employer>St. George\'s, University of London</vacancy:employer>'
        print '  <vacancy:applicationOpeningDate>01/01/1970</vacancy:applicationOpeningDate>'
        print '  <vacancy:applicationClosingDate>' + jobs_data['Closing'] + '</vacancy:applicationClosingDate>'
        print '  <vacancy:applicationInterviewNotificationByDate>' + jobs_data['Interview'] + 'vacancy:applicationInterviewNotificationByDate>'
        print '  <vacancy:organizationPart>' + topic + '</vacancy:organizationPart>'
        print '  <vacancy:availableOnline>' + href + '</vacancy:availableOnline>'
        print '  <vacancy:open>True</vacancy:open>'
        
