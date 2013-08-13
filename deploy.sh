#!/bin.sh
#cp site/* -r /var/www/html
# JOBS
rm -f site/output/jobs*
#python cron/jobs.py


scp -r site/* root@data:/var/www/html/


