import json
from StringIO import StringIO

import urllib2
from BeautifulSoup import BeautifulSoup

import csv
import shutil

import codecs

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
	    reference = str(sib).rstrip().lstrip()
        elif 'Closing Date' in contents:
            closing = str(sib).rstrip().lstrip()
        elif 'Interview Date' in contents:
            interview = str(sib).rstrip().lstrip()
        elif 'Salary' in contents:
            salary = str(sib).rstrip().lstrip()
        #elif 'font style' in contents:
        #    soup_contents = BeautifulSoup(str(contents))
        #    title = str(soup_contents.text)
        #    job_dict['Title'] = title
        #else:
        #    unit = str(contents)
        #    job_dict['Unit'] = unit
    #description = soup.findAll(attrs={'name': 'j748'})
    job_dict['reference'] = reference
    job_dict['closing_date'] = closing
    job_dict['interview_date'] = interview
    job_dict['salary'] = salary
            
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

# navigate in each element of the page
all_jobs = []
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
	jobs_data["url"] = settings["jobs"]["url"]  + "/" + href
	jobs_data["title"] = title
	jobs_data["type"] = type
	jobs_data["topic"] = topic
	all_jobs.append(jobs_data)
       

# JSON
json_output = json.dumps(all_jobs, encoding="utf8", indent=4, sort_keys=True, ensure_ascii=False)

# CSV
i=0
csv_output = "Index,Url,Title,Type,Topic,Reference,Interview Date,Closing Date,Salary\n"
for job in all_jobs:
    url = job['url']
    title = job['title']
    type = job['type']
    topic = job['topic']
    salary = job['salary'].decode('utf8')
    reference = job['reference']
    interview = job['interview_date']
    closing = job['closing_date']
    csv_output = csv_output + str(i)+","+url+","+title+","+type+","+topic+","+reference+","+interview+","+closing+","+ salary +"\n"
    i = i + 1


# RDF
rdf_init_str = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n\
<rdf:RDF\n\
  xmlns:foaf='http://xmlns.com/foaf/0.1/'\n\
  xmlns:oo='http://purl.org/openorg/'\n\
  xmlns:rdfs='http://www.w3.org/2000/01/rdf-schema#'\n\
  xmlns:dc='http://purl.org/dc/elements/1.1/'\n\
  xmlns:vacancy='http://purl.org/openorg/vacancy/'\n\
  xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\n\
  xmlns:dcterms='http://purl.org/dc/terms/'\n\
  xmlns:skos='http://www.w3.org/2004/02/skos/core#'>\n\
    <rdf:Description rdf:about=\"http://www.w3.org/2000/01/rdf-schema#comment\">\n\
        <rdfs:label>comment</rdfs:label>\n\
    </rdf:Description>\n\
    <rdf:Description rdf:about=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#type\">\n\
        <rdfs:label>type</rdfs:label>\n\
    </rdf:Description>\n\
    <rdf:Description rdf:about=\"http://xmlns.com/foaf/0.1/page\">\n\
        <rdfs:label>page</rdfs:label>\n\
    </rdf:Description>\n\
    <rdf:Description rdf:about=\"http://xmlns.com/foaf/0.1/homepage\">\n\
        <rdfs:label>homepage</rdfs:label>\n\
    </rdf:Description>\n\
    <rdf:Description rdf:about=\"http://www.w3.org/2000/01/rdf-schema#label\">\n\
        <rdfs:label>label</rdfs:label>\n\
    </rdf:Description>\n"

i = 0
for job in all_jobs:
    url = job['url']
    title = job['title']
    type = job['type']
    topic = job['topic']
    salary = job['salary']
    reference = job['reference']
    interview = job['interview_date']
    closing = job['closing_date']
    rdf_content_str =  '<foaf:Document rdf:about="http://jobs.sgul.ac.uk">\n\
        <foaf:primaryTopic>\n\
            <vacancy:Vacancy rdf:about="' + url + '">\n\
                <rdfs:label>' + title + '</rdfs:label>\n\
                <vacancy:employer>St. George\'s University of London</vacancy:employer>\n\
                <vacancy:organizationalUnit rdf:resource="' + topic + '"/>\n\
                <vacancy:availableOnline>' + url +  '</vacancy:availableOnline>\n\
                <vacancy:applicationInterviewNotificationByDate>' + interview + '</vacancy:applicationInterviewNotificationByDate>\n\
                <vacancy:applicationClosingDate>' + closing +' </vacancy:applicationClosingDate>\n\
                <rdfs:comment>' + " " + '</rdfs:comment>\n\
                <vacancy:salary>'+ salary.decode("utf8")  +'</vacancy:salary>\n\
            </vacancy:Vacancy>\n\
        </foaf:primaryTopic>\n\
    </foaf:Document>\n'

    rdf_output = rdf_init_str + rdf_content_str + '</rdf:RDF>'
    filename = "jobs_" + str(i) + ".rdf"
    i = i + 1
    with codecs.open(filename, 'w', 'utf-8-sig') as f:
        f.write(rdf_output)
        f.close()
        shutil.copy(filename,'output/'+filename)
        shutil.move(filename,'../static-site/output/'+filename)



# File Write
with codecs.open('jobs.csv', 'w', 'utf-8-sig') as f:
    f.write(csv_output)
    f.close()
    shutil.copy('jobs.csv','output/jobs.csv')
    shutil.move('jobs.csv','../static-site/output/jobs.csv')

with codecs.open('jobs.json', 'w', 'utf-8-sig') as f:
    f.write(json_output)
    f.close()
    shutil.copy('jobs.json','output/jobs.json')
    shutil.move('jobs.json','../static-site/output/jobs.json')


