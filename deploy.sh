#!/bin.sh
cp static-site/* -r /var/www/html

# TODO regenerate TTL

# TODO make service
/etc/init.d/fuseki stop
/etc/init.d/fuseki start
