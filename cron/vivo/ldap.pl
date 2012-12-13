#!/usr/bin/perl
use Mozilla::LDAP::Conn;                # Main "OO" layer for LDAP
use Mozilla::LDAP::Utils;               # LULU, utilities.
use WWW::Mechanize;
use JSON -support_by_pp;
use HTML::Entities;
use URI::Escape;
use CGI qw/:standard/;
use strict;

# read config file
my $json;
{
  local $/; 
  open my $fh, "<", "/root/data.sgul.ac.uk-deploy/data.sgul.ac.uk/cron/config.json";
  $json = <$fh>;
} 
my $JSONPARSER = new JSON;
my $json_text = $JSONPARSER->allow_nonref->utf8->relaxed->escape_slash->loose->allow_singlequote->allow_barekey->decode($json);

my $ldap_host = $json_text->{ldap}->{host};
my $ldap_port = $json_text->{ldap}->{port};
my $bind_user = $json_text->{ldap}->{binduser};
my $bind_pass = $json_text->{ldap}->{bindpass};
my $search_base = $json_text->{ldap}->{searchbase};

my $PATHFULL="/usr/local/vivo15test/data";
my $PATHTHUMB="/usr/local/vivo15test/data/thumbnails";
my $PATHVIVORECORDS="/root/vivo-15-test-ieb/symplectic-harvester/example-scripts/full-harvest-examples/example-symplectic/data/translated-records";

# connect to LDAP host
my $conn = new Mozilla::LDAP::Conn($ldap_host, $ldap_port, $bind_user, $bind_pass,"") || die "Can't connect to $ldap_host.\n";



# read the ldap entries and generate the foaf extract
my $entry = $conn->search($search_base, "subtree", "(uid=*)");
while ($entry) {
	# download data
	my $username=$entry->{"uid"}[0];
        my $mail=$entry->{"mail"}[0];
	my $cn=uri_escape($entry->{"cn"}[0]);
	my $sn=uri_escape($entry->{"sn"}[0]);
	my $givenname=uri_escape($entry->{"givenname"}[0]);
	my $initials=uri_escape($entry->{"initials"}[0]);
   	my $title=$entry->{"title"}[0];
	my $researchinterests=$entry->{"researchinterests"}[0];

	#Photo, profile, research interests
	my $photo = $entry->{"jpegphoto"}[0];
	my $profile = $entry->{"researcherprofile"}[0];




	$profile = decode_entities(decode_entities($profile));

	my $jpegFile = "$PATHFULL/$username.jpg";
	open(TMP, "+>$jpegFile");
	binmode(TMP);
	$| = 1;
	print TMP $photo;
	close(TMP);

	my $jpegFile = "$PATHTHUMB/$username.thumbnail.jpg";
        open(TMP, "+>$jpegFile");
        binmode(TMP);
        $| = 1;
        print TMP $photo;
        close(TMP);

	# generatee rdf
	my $rdfoutput = <<END;
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:foaf="http://xmlns.com/foaf/0.1/"
         xmlns:vivo="http://vivoweb.org/ontology/core#"
         xmlns:vitro="http://vitro.mannlib.cornell.edu/ns/vitro/0.7#"
         xmlns:xs="http://www.w3.org/2001/XMLSchema#"
         xmlns:score="http://vivoweb.org/ontology/score#"
         xmlns:bibo="http://purl.org/ontology/bibo/"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:ufVivo="http://vivo.ufl.edu/ontology/vivo-ufl/"
         xmlns:owlPlus="http://www.w3.org/2006/12/owl2-xml#"
         xmlns:skos="http://www.w3.org/2008/05/skos#"
         xmlns:svo="http://www.symplectic.co.uk/vivo/"
         xmlns:owl="http://www.w3.org/2002/07/owl#"
         xmlns:api="http://www.symplectic.co.uk/publications/api"
         xmlns:vitro-public="http://vitro.mannlib.cornell.edu/ns/vitro/public#"
         xmlns:vocab="http://purl.org/vocab/vann/"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:swvocab="http://www.w3.org/2003/06/sw-vocab-status/ns#"
         xmlns:core="http://vivoweb.org/ontology/core#"
         xmlns:dc="http://purl.org/dc/elements/1.1/">
   <rdf:Description rdf:about="http://vivo.sgul.ac.uk:8080/vivo15test/individual/$username">
      <ufVivo:harvestedBy>Symplectic-Harvester</ufVivo:harvestedBy>
      <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
      <rdfs:label>$sn, $givenname</rdfs:label>
      <core:preferredTitle>$title</core:preferredTitle>
      <core:primaryEmail>$mail</core:primaryEmail>
      <foaf:lastName>$sn</foaf:lastName>
      <foaf:firstName>$givenname</foaf:firstName>
      <score:initials>$initials</score:initials>
      <rdf:type rdf:resource="http://vivoweb.org/harvester/excludeEntity"/>
      <rdf:type rdf:resource="http://vitro.mannlib.cornell.edu/ns/vitro/0.7#Flag1Value1Thing"/>
      <rdf:type rdf:resource="http://www.symplectic.co.uk/vivo/User"/>
      <vitro-public:mainImage rdf:resource="http://vivo.sgul.ac.uk:8080/vivo15test/individual/$username-image"/>
      <ufVivo:harvestedBy>Symplectic-Harvester</ufVivo:harvestedBy>
      <vivo:overview>
	<![CDATA[$profile]]>
      </vivo:overview>
   </rdf:Description>
</rdf:RDF>
END

	# write rdf file
	my $vivoFile = "$PATHVIVORECORDS/user$username";
	open(TMP, "+>$vivoFile");
	print TMP "$rdfoutput";
	close(TMP);


        $entry = $conn->nextEntry();
}

