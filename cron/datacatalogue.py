import json
from StringIO import StringIO

import urllib, urllib2
from BeautifulSoup import BeautifulSoup

import csv
import shutil
import os
import codecs
import tarfile

#read settings, load url, parse resulting text
settings_text = open(os.path.dirname(__file__) +"/config.json", "r").read()
settings = json.loads(settings_text)
# jobs_url = settings["jobs"]["url"] + "/" + settings["jobs"]["list"]
output_url = settings["datadownload"]["url"]

       
all_entries = dict()

# one dictionary for each dataset
catalogue = dict()
catalogue['csv'] = output_url + "catalogue.csv"
catalogue['json'] = output_url + "catalogue.json"
catalogue['rdfdump'] = output_url + "catalogue.rdf"
all_entries['catalogue'] = catalogue

jobs = dict()
jobs['csv'] = output_url + "jobs.csv"
jobs['json'] = output_url + "jobs.json"
jobs['rdfdump'] = output_url + "jobsrdf.tar"
all_entries['jobs'] = jobs

publications = dict()
publications['csv'] = output_url + "publications.csv"
publications['json'] = output_url + "publications.json"
publications['rdfdump'] = output_url + "publicationsrdf.tar"
all_entries['publications'] = publications

# JSON
json_output = json.dumps(all_entries, encoding="utf8", indent=4, sort_keys=True, ensure_ascii=False)


print json_output
# # CSV
# i=0
# csv_output = "Index,Url,Title,Type,Topic,Reference,Interview Date,Closing Date,Salary\n"
# for job in all_jobs:
#     url = job['url']
#     title = job['title']
#     type = job['type']
#     topic = job['topic']
#     salary = job['salary'].decode('utf8')
#     reference = job['reference']
#     interview = job['interview_date']
#     closing = job['closing_date']
#     csv_output = csv_output + str(i)+","+url+","+title+","+type+","+topic+","+reference+","+interview+","+closing+","+ salary +"\n"
#     i = i + 1


# # RDF
# rdf_init_str = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n\
# <rdf:RDF\n\
#   xmlns:foaf='http://xmlns.com/foaf/0.1/'\n\
#   xmlns:oo='http://purl.org/openorg/'\n\
#   xmlns:rdfs='http://www.w3.org/2000/01/rdf-schema#'\n\
#   xmlns:dc='http://purl.org/dc/elements/1.1/'\n\
#   xmlns:vacancy='http://purl.org/openorg/vacancy/'\n\
#   xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>\n\
#     <rdf:Description rdf:about=\"http://www.w3.org/2000/01/rdf-schema#comment\">\n\
#         <rdfs:label>comment</rdfs:label>\n\
#     </rdf:Description>\n\
#     <rdf:Description rdf:about=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#type\">\n\
#         <rdfs:label>type</rdfs:label>\n\
#     </rdf:Description>\n\
#     <rdf:Description rdf:about=\"http://xmlns.com/foaf/0.1/page\">\n\
#         <rdfs:label>page</rdfs:label>\n\
#     </rdf:Description>\n\
#     <rdf:Description rdf:about=\"http://xmlns.com/foaf/0.1/homepage\">\n\
#         <rdfs:label>homepage</rdfs:label>\n\
#     </rdf:Description>\n\
#     <rdf:Description rdf:about=\"http://www.w3.org/2000/01/rdf-schema#label\">\n\
#         <rdfs:label>label</rdfs:label>\n\
#     </rdf:Description>\n"

# i = 0
# members = []
# for job in all_jobs:
#     url = job['url']
#     title = job['title']
#     type = job['type']
#     topic = job['topic']
#     salary = job['salary']
#     reference = job['reference']
#     interview = job['interview_date']
#     closing = job['closing_date']
#     # REDO according to https://data.ox.ac.uk/feeds/vacancies/31337175.rdf
#     rdf_content_str =  '<foaf:Document rdf:about="http://jobs.sgul.ac.uk">\n\
#         <foaf:primaryTopic>\n\
#             <vacancy:Vacancy rdf:about="' + url + '">\n\
#                 <rdfs:label>' + title + '</rdfs:label>\n\
#                 <vacancy:employer>St. George\'s University of London</vacancy:employer>\n\
#                 <vacancy:organizationalUnit>' + topic + '</vacancy:organizationalUnit>\n\
#                 <vacancy:availableOnline>' + url +  '</vacancy:availableOnline>\n\
#                 <vacancy:applicationInterviewNotificationByDate>' + interview + '</vacancy:applicationInterviewNotificationByDate>\n\
#                 <vacancy:applicationClosingDate>' + closing +' </vacancy:applicationClosingDate>\n\
#                 <rdfs:comment>' + " None " + '</rdfs:comment>\n\
#                 <vacancy:salary>'+ salary.decode("utf8")  +'</vacancy:salary>\n\
#             </vacancy:Vacancy>\n\
#         </foaf:primaryTopic>\n\
#     </foaf:Document>\n'

#     rdf_output = rdf_init_str + rdf_content_str + '</rdf:RDF>'
#     filename = "jobs_" + str(i) + ".rdf"
#     i = i + 1
#     members.append(filename)
#     with codecs.open(filename, 'w', 'utf-8-sig') as f:
#         f.write(rdf_output)
#         f.close()
#         shutil.move(filename,os.path.dirname(__file__) +"/output/"+filename)
#         #up_one_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'site/output'))
#         #shutil.move(filename,up_one_folder+"/"+filename)



# # File Write
# with codecs.open(os.path.dirname(__file__) +'/jobs.csv', 'w', 'utf-8-sig') as f:
#     f.write(csv_output)
#     f.close()
#     shutil.move(os.path.dirname(__file__) +'/jobs.csv',os.path.dirname(__file__) +"/output/jobs.csv")
#     #up_one_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'site/output'))
#     #shutil.move("jobs.csv",up_one_folder+"/jobs.csv")
    

# with codecs.open(os.path.dirname(__file__) +'/jobs.json', 'w', 'utf-8-sig') as f:
#     f.write(json_output)
#     f.close()
#     shutil.copy(os.path.dirname(__file__) +'/jobs.json',os.path.dirname(__file__) +"/output/jobs.json")
#     #up_one_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'site/output'))
#     #shutil.move("jobs.json",up_one_folder+"/jobs.json")

# tar = tarfile.open(os.path.dirname(__file__) +"/output/jobsrdf.tar", "w")
# for name in members:
#     path = os.path.dirname(__file__) +'/output/'+name
#     tar.add(path)
# tar.close()
