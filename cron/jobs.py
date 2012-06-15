import json
from StringIO import StringIO

import urllib2
from BeautifulSoup import BeautifulSoup


def downloadJobDetails(url):
    jobs_detail_url = settings["jobs"]["url"]  + "/" + url
    job = (urllib2.urlopen(jobs_url)).read()
    soup = BeautifulSoup(job)
    maincontent_element = soup.findAll(attrs={'id': 'maincontent'})[0]

    reference = ""
    closing = ""
    interview = ""
    salary = ""
    description = ""

    msonormal_elements = soup.findAll(attrs={'class': 'staffprofilequote'})
    i=0
    for desc_elem in msonormal_elements:
        i = i + 1
        description = description + str(desc_elem.contents)

    doc_file_url = ""
   
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
