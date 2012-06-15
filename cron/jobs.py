import json
from StringIO import StringIO

import urllib2
from BeautifulSoup import BeautifulSoup



#read settings, load url, parse resulting text
settings_text = open("config.json", "r").read()
settings = json.loads(settings_text)
jobs_url = settings["jobs"]["url"]


# get page and soupify
jobs = (urllib2.urlopen(jobs_url)).read()
soup = BeautifulSoup(jobs)

for i in soup.findAll(attrs={'class': 'printHide'}):
    print i.extract()

