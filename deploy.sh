#!/bin.sh

HOST="data.sgul.ac.uk"
USER="root"
SIRSI="unicorn.sgul.ac.uk"
OPDHOST="cluster-node2.sgul.ac.uk"
OPDUSER="root"
DATE=`date`

echo $DATE > site/.datefile.txt

# JOBS
echo "Elaborating Job Vacancies"
rm -f site/output/jobs*
rm -f cron/output/jobs*
python cron/jobs.py
tar -cvf cron//output/jobsrdf.tar cron/output/jobs*.rdf 

# PUBLICATIONS
echo "Elaborating Publications"
rm -f site/output/pub*
rm -f cron/output/pub*
php cron/pubrepo.php
tar -cvf cron/output/publicationsrdf.tar cron/output/pub*.rdf  



# COURSE MODULES
echo "Elaborating Course Modules"
rm -f site/output/course*
rm -f cron/output/course*
cp datasets_local/coursemodules.csv cron/output/
php cron/localdatasets.php
tar -cvf cron/output/coursemodulesrdf.tar cron/output/course*.rdf 

# SIRSI
echo "Elaborating Library Catalogue"
rm -f site/output/lib*
rm -f cron/output/lib*
scp root@$SIRSI:/s/sirsi/Unicorn/Xfer/full_stg_primo.mrc cron/sirsi.mrc
python cron/sirsi.py
rm -f cron/sirsi.mrc
tar -cvf cron/output/libraryrdf.tar cron/output/lib*.rdf

# CATALOGUE
echo "Generating Data Catalogue"
rm -f site/output/datacatalogue*
rm -f cron/output/datacatalogue*
python cron/datacatalogue.py



# FACILITIES
echo "Writing Equipment file"
rm -f cron/equipment.csv
rm -f site/equipment.csv
php cron/equipment.php

# OPD
echo "Writing OPD file"
rm -f cron/opd.ttl
rm -f site/opd.ttl
php cron/opd.php

# Moving files
echo "Moving files to destination"
mv cron/output/*.rdf site/output/
mv cron/output/*.json site/output/
mv cron/output/*.csv site/output/
mv cron/output/*.tar site/output/
mv cron/output/*.ttl site/output/

# MYSQL
echo "Executing export into Mysql"
dos2unix site/output/jobs.json
dos2unix site/output/library.json
dos2unix site/output/datacatalogue.json
dos2unix site/output/coursemodules.json
dos2unix site/output/publications.json
php cron/sql.php



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
scp -r site/.datefile.txt $USER@$HOST:/var/www/html/

echo "Deploying OPD"
scp site/output/opd.ttl $OPDUSER@$OPDHOST:/wwwdata/cluster/www/html/.well-known/openorg

sleep 3

echo "Importing data into 4s"
ssh $USER@$HOST 4s-import data /var/www/html/output/*.rdf
echo "Starting SPARQL http endpoint"
ssh $USER@$HOST 4s-httpd -p 8282 data






echo "Open Data portal ready"



 



