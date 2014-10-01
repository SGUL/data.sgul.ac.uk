#!/usr/bin/env python
 
import csv
import json
import os
import cgi
import codecs
import shutil
from pymarc import MARCReader
from os import listdir
from re import search
 


def cleanNone(variable):
  if not variable:
      variable = ""
  return variable


#- change this line to match your folder structure
SRC_DIR = 'cron/'
 
# get a list of all .mrc files in source directory
file_list = filter(lambda x: search('.mrc', x), listdir(SRC_DIR))
i = 0
csv_out = csv.writer(open('cron/output/library.csv', 'w'), delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
csv_out.writerow([unicode(s).encode("utf-8") for s in ["title", "author", "date", "subject", "oclc", "publisher", "isbn"]])
all_books = []
for item in file_list:
  
  fd = file(SRC_DIR + '/' + item, 'r')
  reader = MARCReader(fd)
  for record in reader:
    i = i + 1
    title = author = date = subject = oclc = publisher = ''
 
    # title
    if record['245'] is not None:
      title = record['245']['a']
      if record['245']['b'] is not None:
        title = title + " " + record['245']['b']
    
    # determine author
    if record['100'] is not None:
      author = record['100']['a']
    elif record['110'] is not None:
      author = record['110']['a']
    elif record['700'] is not None:
      author = record['700']['a']
    elif record['710'] is not None:
      author = record['710']['a']
    
    # date
    if record['260'] is not None:
      date = record['260']['c']
    
    # subject
    if record['650'] is not None:
      subject = record['650']['a']
    
    # oclc number
    if record['035'] is not None:
      if len(record.get_fields('035')[0].get_subfields('a')) > 0:
        oclc = record['035']['a'].replace('(OCoLC)', '')
    
    # publisher
    if record['260'] is not None:
      publisher = record['260']['b']
    
    # isbn
    isbn = record.isbn()
    if not isbn:
          isbn = ""
    this_book = dict()
    this_book['id'] = 'lib'+str(i)

    title = cleanNone(title)
    author = cleanNone(author)
    date = cleanNone(date)
    subject = cleanNone(subject)
    oclc = cleanNone(oclc)
    publisher = cleanNone(publisher)
    isbn = cleanNone(isbn)


    this_book['title'] = title
    this_book['author'] = author
    this_book['date'] = date
    this_book['subject'] = subject
    this_book['oclc'] = oclc
    this_book['publisher'] = publisher
    this_book['isbn'] = isbn
    all_books.append(this_book)


    csv_out.writerow([unicode(s).encode("utf-8") for s in [title, author, date, subject, oclc, publisher, isbn]])



    # RDF
    rdfprint = '<?xml version="1.0" encoding="UTF-8"?>\n\
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n\
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n\
    xmlns:bibo="http://purl.org/ontology/bibo/"\n\
    xmlns:sgul="http://data.sgul.ac.uk/ontology/lib/"\n\
    xmlns:dc="http://purl.org/dc/elements/1.1/"\n\
    xmlns:vivo="http://vivoweb.org/ontology/core#">\n\
    <rdf:Description rdf:about="http://data.sgul.ac.uk/id/lib' + str(i) +'">\n\
    <rdf:type rdf:resource="http://purl.org/ontology/bibo/Book"/>\n\
    <rdf:type rdf:resource="http://purl.org/ontology/bibo/Document"/>\n\
    <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>\n\
    <rdfs:label>%s</rdfs:label>\n\
    <bibo:isbn>%s</bibo:isbn>\n\
    <dc:author>%s</dc:author>\n\
    <dc:publisher>%s</dc:publisher>\n\
    <vivo:dateTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">%s</vivo:dateTime>\n\
    <bibo:oclcnum>%s</bibo:oclcnum>\n\
    <sgul:libraryItem>true</sgul:libraryItem>\n\
    </rdf:Description>\n\
    </rdf:RDF>' % (cgi.escape(title), cgi.escape(isbn), cgi.escape(author), cgi.escape(publisher), cgi.escape(date), cgi.escape(oclc))
    with codecs.open(os.path.dirname(__file__) +'/output/lib'+str(i)+'.rdf', 'w', 'utf-8-sig') as f:
        f.write(rdfprint)
        f.close()

  fd.close()

# JSON
json_output = json.dumps(all_books, encoding="utf8", indent=4, sort_keys=True, ensure_ascii=False)
with codecs.open(os.path.dirname(__file__) +'/output/library.json', 'w', 'utf-8-sig') as f:
  f.write(json_output)
  f.close()
  #shutil.copy(os.path.dirname(__file__) +'/library.json',os.path.dirname(__file__) +"/library/jobs.json")
  #up_one_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'site/output'))
  #shutil.move("jobs.json",up_one_folder+"/jobs.json")

    



  
# JSON
# csvfile = open('marc_records.csv', 'r')
# jsonfile = open('marc_records.json', 'w')

# fieldnames = ("title","author","date","subject","oclc","publisher","isbn")
# reader = csv.DictReader( csvfile, fieldnames)
# for row in reader:
#     json.dumps(row, jsonfile)
#     jsonfile.write('\n')
  
