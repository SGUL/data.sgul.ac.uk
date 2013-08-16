import json
import csv
import shutil
import os
import codecs
import tarfile

#read settings, load url, parse resulting text
settings_text = open(os.path.dirname(__file__) +"/config.json", "r").read()
settings = json.loads(settings_text)
output_url = settings["datadownload"]["url"]

       
all_entries = dict()

# one dictionary for each dataset
catalogue = dict()
catalogue['csv'] = output_url + "catalogue.csv"
catalogue['json'] = output_url + "catalogue.json"
catalogue['rdfdump'] = output_url + "cataloguerdf.tar"
catalogue['humanurl'] = output_url + "datacatalogue.php"
all_entries['catalogue'] = catalogue

jobs = dict()
jobs['csv'] = output_url + "jobs.csv"
jobs['json'] = output_url + "jobs.json"
jobs['rdfdump'] = output_url + "jobsrdf.tar"
jobs['humanurl'] = output_url + "vacancies.php"
all_entries['jobs'] = jobs

publications = dict()
publications['csv'] = output_url + "publications.csv"
publications['json'] = output_url + "publications.json"
publications['rdfdump'] = output_url + "publicationsrdf.tar"
publications['humanurl'] = output_url + "publications.php"
all_entries['publications'] = publications

# JSON
json_output = json.dumps(all_entries, encoding="utf8", indent=4, sort_keys=True, ensure_ascii=False)


with codecs.open(os.path.dirname(__file__) +'/datacatalogue.json', 'w', 'utf-8-sig') as f:
    f.write(json_output)
    f.close()
    shutil.copy(os.path.dirname(__file__) +'/datacatalogue.json',os.path.dirname(__file__) +"/output/datacatalogue.json")
    

j = all_entries
f = csv.writer(open(os.path.dirname(__file__) +"/datacatalogue.csv", "wb+"))
# Write CSV Header, If you dont need that, remove this line
f.writerow(["description", "csv", "json", "rdfdump", "humanurl"])

entry = j["catalogue"]
f.writerow(["catalogue",entry["csv"], entry["json"], entry["rdfdump"], entry["humanurl"]])
entry = j["publications"]
f.writerow(["publications",entry["csv"], entry["json"], entry["rdfdump"], entry["humanurl"]])
entry = j["jobs"]
f.writerow(["jobs",entry["csv"], entry["json"], entry["rdfdump"], entry["humanurl"]])


# File Write
with codecs.open(os.path.dirname(__file__) +'/datacatalogue.csv', 'w', 'utf-8-sig') as f:
    shutil.move(os.path.dirname(__file__) +'/datacatalogue.csv',os.path.dirname(__file__) +"/output/datacatalogue.csv")
    
    


# RDF
rdf_init_str = "\
<?xml version=\"1.0\" encoding=\"utf-8\"?>\n\
<rdf:RDF\n\
  xmlns:dcat='http://www.w3.org/ns/dcat#'\n\
  xmlns:dct='http://purl.org/dc/terms/'\n\
  xmlns:dctype='http://purl.org/dc/dcmitype/'\n\
  xmlns:skos='http://www.w3.org/2004/02/skos/core#'\n\
  xmlns:vcard='http://www.w3.org/2006/vcard/ns#'\n\
  xmlns:dcterms='http://purl.org/dc/terms/'\n\
  xmlns:xsd='http://www.w3.org/2001/XMLSchema#'\n\
  xmlns:foaf='http://xmlns.com/foaf/0.1/'\n\
  xmlns:void='http://rdfs.org/ns/void#'\n\
  xmlns:oo='http://purl.org/openorg/'\n\
  xmlns:rdfs='http://www.w3.org/2000/01/rdf-schema#'\n\
  xmlns:dc='http://purl.org/dc/elements/1.1/'\n\
  xmlns:vacancy='http://purl.org/openorg/vacancy/'\n\
  xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>\n\
  xmlns:bibo='http://purl.org/ontology/bibo/'\n\
  xmlns:sgul='http://data.sgul.ac.uk/ontology/lib/'\n\
  xmlns:vivo='http://vivoweb.org/ontology/core#'>\n\
"

# DATA CATALOGUE PREAMBLE
rdf_catalogue = "\n\
    <rdf:Description rdf:about='https://data.ox.ac.uk/id/dataset/catalogue'>\n\
        <dcterms:license rdf:resource='http://creativecommons.org/publicdomain/zero/1.0/'/>\n\
        <dcterms:title>Dataset catalogue for SGUL</dcterms:title>\n\
        <oo:contact rdf:resource='https://data.sgul.ac.uk/contact.php'/>\n\
        <oo:corrections rdf:resource='https://data.sgul.ac.uk/contact.php'/>\n\
        <void:dataDump rdf:resource='https://data.sgul.ac.uk/output/datacatalogue.rdf'/>\n\
        <rdf:type rdf:resource='http://www.w3.org/ns/dcat#Catalog'/>\n\
        <rdf:type rdf:resource='http://www.w3.org/ns/dcat#Dataset'/>\n\
        <dcat:dataset rdf:resource='https://data.sgul.ac.uk/ontology/datacatalogue'/>\n\
        <dcat:dataset rdf:resource='https://data.sgul.ac.uk/ontology/vacancies'/>\n\
        <dcat:dataset rdf:resource='https://data.sgul.ac.uk/ontology/publications'/>\n\
        <foaf:homepage rdf:resource='http://data.sgul.ac.uk/listdatasets.php'/>\n\
    </rdf:Description>\n\
"

# JOB VACANCIES
rdf_jobs = "\n\
<dcat:Dataset rdf:about='http://data.sgul.ac.uk/ontology/vacancies'>\n\
  <dct:description>Job vacancies at SGUL</dct:description>\n\
  <dcat:keyword>sgul</dcat:keyword>\n\
  <dcat:keyword>jobs</dcat:keyword>\n\
  <dcat:keyword>vacancies</dcat:keyword>\n\
  <foaf:homepage rdf:resource='http://data.sgul.ac.uk/vacancies.php'></foaf:homepage>\n\
  <rdfs:label>Job vacancies at SGUL</rdfs:label>\n\
  <dct:identifier>sgul-job-vacancies</dct:identifier>\n\
  <dct:title>Job Vacancies at SGUL</dct:title>\n\
  <dcat:distribution>\n\
      <dcat:Distribution>\n\
          <dcat:accessURL rdf:resource='http://data.sgul.ac.uk/output/jobs.json'></dcat:accessURL>\n\
          <rdfs:label>JSON</rdfs:label>\n\
      </dcat:Distribution>\n\
  </dcat:distribution>\n\
  <dcat:distribution>\n\
      <dcat:Distribution>\n\
          <dcat:accessURL rdf:resource='http://data.sgul.ac.uk/output/jobs.csv'></dcat:accessURL>\n\
          <rdfs:label>CSV</rdfs:label>\n\
      </dcat:Distribution>\n\
  </dcat:distribution>\n\
  <dcat:distribution>\n\
      <dcat:Distribution>\n\
          <dcat:accessURL rdf:resource='http://data.sgul.ac.uk/output/jobsrdf.tar'></dcat:accessURL>\n\
          <rdfs:label>RDF Dump</rdfs:label>\n\
      </dcat:Distribution>\n\
  </dcat:distribution>\n\
  <dcat:distribution>\n\
      <dcat:Distribution>\n\
          <dcat:accessURL rdf:resource='http://data.sgul.ac.uk/sparql'></dcat:accessURL>\n\
          <rdfs:label>SPARQL Endpoint</rdfs:label>\n\
      </dcat:Distribution>\n\
  </dcat:distribution>\n\
  <dct:creator>\n\
    <rdf:Description>\n\
      <foaf:name>Giuseppe Sollazzo</foaf:name>\n\
      <foaf:mbox rdf:resource='mailto:opendata@sgul.ac.uk'></foaf:mbox>\n\
    </rdf:Description>\n\
  </dct:creator>\n\
  <dct:contributor>\n\
    <rdf:Description>\n\
      <foaf:name>Giuseppe Sollazzo</foaf:name>\n\
      <foaf:mbox rdf:resource='mailto:opendata@sgul.ac.uk'></foaf:mbox>\n\
    </rdf:Description>\n\
  </dct:contributor>\n\
  <dct:rights rdf:resource='http://www.nationalarchives.gov.uk/doc/open-government-licence/'></dct:rights>\n\
  </dcat:Dataset>\n\
    "

# PUBLICATIONS
rdf_pubs ="\n\
<dcat:Dataset rdf:about='http://data.sgul.ac.uk/ontology/publications'>\n\
  <dct:description>Publications at SGUL</dct:description>\n\
  <dcat:keyword>sgul</dcat:keyword>\n\
  <dcat:keyword>academic</dcat:keyword>\n\
  <dcat:keyword>publications</dcat:keyword>\n\
  <foaf:homepage rdf:resource='http://data.sgul.ac.uk/publications.php'></foaf:homepage>\n\
  <rdfs:label>Publications at SGUL</rdfs:label>\n\
  <dct:identifier>sgul-academic-publications</dct:identifier>\n\
  <dct:title>Publications at SGUL</dct:title>\n\
  <dcat:distribution>\n\
      <dcat:Distribution>\n\
          <dcat:accessURL rdf:resource='http://data.sgul.ac.uk/output/publications.json'></dcat:accessURL>\n\
          <rdfs:label>JSON</rdfs:label>\n\
      </dcat:Distribution>\n\
  </dcat:distribution>\n\
  <dcat:distribution>\n\
      <dcat:Distribution>\n\
          <dcat:accessURL rdf:resource='http://data.sgul.ac.uk/output/publications.csv'></dcat:accessURL>\n\
          <rdfs:label>CSV</rdfs:label>\n\
      </dcat:Distribution>\n\
  </dcat:distribution>\n\
  <dcat:distribution>\n\
      <dcat:Distribution>\n\
          <dcat:accessURL rdf:resource='http://data.sgul.ac.uk/output/publicationsrdf.tar'></dcat:accessURL>\n\
          <rdfs:label>RDF Dump</rdfs:label>\n\
      </dcat:Distribution>\n\
  </dcat:distribution>\n\
  <dcat:distribution>\n\
      <dcat:Distribution>\n\
          <dcat:accessURL rdf:resource='http://data.sgul.ac.uk/sparql'></dcat:accessURL>\n\
          <rdfs:label>SPARQL Endpoint</rdfs:label>\n\
      </dcat:Distribution>\n\
  </dcat:distribution>\n\
  <dct:creator>\n\
    <rdf:Description>\n\
      <foaf:name>Giuseppe Sollazzo</foaf:name>\n\
      <foaf:mbox rdf:resource='mailto:opendata@sgul.ac.uk'></foaf:mbox>\n\
    </rdf:Description>\n\
  </dct:creator>\n\
  <dct:contributor>\n\
    <rdf:Description>\n\
      <foaf:name>Giuseppe Sollazzo</foaf:name>\n\
      <foaf:mbox rdf:resource='mailto:opendata@sgul.ac.uk'></foaf:mbox>\n\
    </rdf:Description>\n\
  </dct:contributor>\n\
  <dct:rights rdf:resource='http://www.nationalarchives.gov.uk/doc/open-government-licence/'></dct:rights>\n\
  </dcat:Dataset>\n\
    "
# CATALOGUE
rdf_catalogue_data ="\n\
<dcat:Dataset rdf:about='http://data.sgul.ac.uk/ontology/datacatalogue'>\n\
  <dct:description>Data Catalogue at SGUL</dct:description>\n\
  <dcat:keyword>sgul</dcat:keyword>\n\
  <dcat:keyword>data</dcat:keyword>\n\
  <dcat:keyword>catalogue</dcat:keyword>\n\
  <foaf:homepage rdf:resource='http://data.sgul.ac.uk/datacatalogue.php'></foaf:homepage>\n\
  <rdfs:label>Data Catalogue at SGUL</rdfs:label>\n\
  <dct:identifier>sgul-data-catalogue</dct:identifier>\n\
  <dct:title>Data Catalogue at SGUL</dct:title>\n\
  <dcat:distribution>\n\
      <dcat:Distribution>\n\
          <dcat:accessURL rdf:resource='http://data.sgul.ac.uk/output/datacatalogue.json'></dcat:accessURL>\n\
          <rdfs:label>JSON</rdfs:label>\n\
      </dcat:Distribution>\n\
  </dcat:distribution>\n\
  <dcat:distribution>\n\
      <dcat:Distribution>\n\
          <dcat:accessURL rdf:resource='http://data.sgul.ac.uk/output/datacatalogue.csv'></dcat:accessURL>\n\
          <rdfs:label>CSV</rdfs:label>\n\
      </dcat:Distribution>\n\
  </dcat:distribution>\n\
  <dcat:distribution>\n\
      <dcat:Distribution>\n\
          <dcat:accessURL rdf:resource='http://data.sgul.ac.uk/output/datacataloguerdf.tar'></dcat:accessURL>\n\
          <rdfs:label>RDF Dump</rdfs:label>\n\
      </dcat:Distribution>\n\
  </dcat:distribution>\n\
  <dcat:distribution>\n\
      <dcat:Distribution>\n\
          <dcat:accessURL rdf:resource='http://data.sgul.ac.uk/sparql'></dcat:accessURL>\n\
          <rdfs:label>SPARQL Endpoint</rdfs:label>\n\
      </dcat:Distribution>\n\
  </dcat:distribution>\n\
  <dct:creator>\n\
    <rdf:Description>\n\
      <foaf:name>Giuseppe Sollazzo</foaf:name>\n\
      <foaf:mbox rdf:resource='mailto:opendata@sgul.ac.uk'></foaf:mbox>\n\
    </rdf:Description>\n\
  </dct:creator>\n\
  <dct:contributor>\n\
    <rdf:Description>\n\
      <foaf:name>Giuseppe Sollazzo</foaf:name>\n\
      <foaf:mbox rdf:resource='mailto:opendata@sgul.ac.uk'></foaf:mbox>\n\
    </rdf:Description>\n\
  </dct:contributor>\n\
  <dct:rights rdf:resource='http://www.nationalarchives.gov.uk/doc/open-government-licence/'></dct:rights>\n\
  </dcat:Dataset>\n\
    "

filename = "datacatalogue.rdf"
rdf_output = rdf_init_str + rdf_catalogue + rdf_catalogue_data + rdf_jobs + rdf_pubs + "\n</rdf:RDF>"
with codecs.open(filename, 'w', 'utf-8-sig') as f:
    f.write(rdf_output)
    f.close()
    shutil.move(filename,os.path.dirname(__file__) +"/output/"+filename)


members = ['datacatalogue.rdf']
tar = tarfile.open(os.path.dirname(__file__) +"/output/datacataloguerdf.tar", "w")
for name in members:
    path = os.path.dirname(__file__) +'/output/'+name
    tar.add(path)
tar.close()
