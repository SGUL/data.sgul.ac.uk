<?php

$opd = <<<OPD
@prefix foaf:    <http://xmlns.com/foaf/0.1/>.
@prefix oo:      <http://purl.org/openorg/>.
@prefix dcterms: <http://purl.org/dc/terms/>.
@prefix geo:     <http://www.w3.org/2003/01/geo/wgs84_pos#>.
@prefix skos:    <http://www.w3.org/2004/02/skos/core#>.
@prefix org:     <http://www.w3.org/ns/org#>.
@prefix xtypes:  <http://purl.org/xtypes/>.
@prefix lyou:    <http://purl.org/linkingyou/>.
@prefix vcard:   <http://www.w3.org/2006/vcard/ns#>.
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .


<> a oo:OrganizationProfileDocument ;
        dcterms:license <http://creativecommons.org/publicdomain/zero/1.0/> ;
        foaf:primaryTopic <http://id.sgul.ac.uk/> .

<http://id.sgul.ac.uk/>
        a org:FormalOrganization ;
        skos:prefLabel "St George's, University of London" ;
        foaf:homepage <http://www.sgul.ac.uk/> ;
		foaf:account <https://twitter.com/StGeorgesUni> ;
        <http://purl.org/linkingyou/open-data> <http://data.sgul.ac.uk/> ;
		foaf:account <https://twitter.com/sgulit> .


<https://twitter.com/StGeorgesUni> a foaf:OnlineAccount ;
	foaf:accountName "SGUL" ;
	foaf:accountServiceHomepage <https://twitter.com/> .


<https://twitter.com/sgulit> a foaf:OnlineAccount ;
	foaf:accountName "SGUL Computing Services" ;
	foaf:accountServiceHomepage <https://twitter.com/> .


# Contact for open data service
<http://id.sgul.ac.uk/ukprn/10007782#ods-contact>
     a foaf:Person ;
     foaf:name "Giuseppe Sollazzo" ;
     foaf:mbox <mailto:gsollazz@sgul.ac.uk> .

# Equipment
<http://data.sgul.ac.uk/output/equipment.csv>
    <http://purl.org/dc/terms/conformsTo> <http://equipment.data.ac.uk/uniquip> ;
    <http://purl.org/dc/terms/license> <http://www.nationalarchives.gov.uk/doc/open-government-licence/> ;
    <http://purl.org/dc/terms/subject> <http://purl.org/openorg/theme/equipment>, <http://purl.org/openorg/theme/facilities> ;
    <http://purl.org/openorg/contact> <mailto:gsollazz@sgul.ac.uk> ;
    <http://purl.org/openorg/corrections> <mailto:gsollazz@sgul.ac.uk> ;
    <http://purl.org/openorg/organization> <http://id.sgul.ac.uk/> .
OPD;

$opdfile = "./cron/output/opd.ttl";
$f_opd = fopen($opdfile, 'w') or die("can't open file");
fwrite($f_opd, $opd);
fclose($f_opd);
?>