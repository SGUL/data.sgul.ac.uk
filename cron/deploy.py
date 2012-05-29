import simplejson 
import os, sys
from pprint import pprint

json_data = open(file_directory).read()
data = simplejson.loads(json_data)
pprint(data)
