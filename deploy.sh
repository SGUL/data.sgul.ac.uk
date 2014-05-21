#!/bin.sh

HOST="data.sgul.ac.uk"
USER="root"

# JOBS
echo "Elaborating Job Vacancies"
rm -f site/output/jobs*
rm -f cron/output/jobs*
python cron/jobs.py

# PUBLICATIONS
echo "Elaborating Publications"
rm -f site/output/pub*
rm -f cron/output/pub*
php cron/pubrepo.php

# COURSE MODULES

# SIRSI

# CATALOGUE
echo "Generating Data Catalogue"
rm -f site/output/datacatalogue*
rm -f cron/output/datacatalogue*
python cron/datacatalogue.py

echo "Moving files to destination"
mv cron/output/*.rdf site/output/
mv cron/output/*.json site/output/
mv cron/output/*.csv site/output/
mv cron/output/*.tar site/output/



# RDF Data store
echo "Killing 4s daemons"
ssh $USER@$HOST pkill -f \'^4s-httpd -p 8282 data\$\'
ssh $USER@$HOST pkill -f \'^4s-backend data$\'

echo "Destroying 4s backend"
ssh $USER@$HOST 4s-backend-destroy data

echo "[Paranoid] Deleting 4s files"
ssh $USER@$HOST rm -rf /var/lib/4store/data/*

echo "Deleting web files"
ssh $USER@$HOST rm -rf /var/www/html/*

sleep 3

echo "Setting up 4s instance"
ssh $USER@$HOST 4s-backend-setup data
echo "Starting 4s instance"
ssh $USER@$HOST 4s-backend data

echo "Deploying web site"
scp -r site/* $USER@$HOST:/var/www/html/

sleep 3

echo "Importing data into 4s"
ssh $USER@$HOST 4s-import data /var/www/html/output/*.rdf
echo "Starting SPARQL http endpoint"
ssh $USER@$HOST 4s-httpd -p 8282 data
echo "Open Data portal ready"



 



