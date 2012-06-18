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
        elif 'font style' in contents:
            title = "" #str(sib.children[0])
        else:
            unit = str(sib)
            
    print "Reference: " + reference +", Title: " + title + ", Unit: "+ unit + ", Closing: " + closing + ", Interview: " + interview + ", Salary: " + salary
    return description





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
        print jobs_data
