#!/usr/bin/perl
use Mozilla::LDAP::Conn;                # Main "OO" layer for LDAP
use Mozilla::LDAP::Utils;               # LULU, utilities.
use WWW::Mechanize;
use JSON -support_by_pp;
use HTML::Entities;
use URI::Escape;
use CGI qw/:standard/;
use File::Copy qw(copy);
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

my $baseUrl = "http://vivo.sgul.ac.uk:8080/vivo15";
my $aboutBaseUrl= "http://vivo.symplectic.co.uk/individual";


my $PATHFULL="/usr/local/vivo15symtest/data";
my $PATHTHUMB="/usr/local/vivo15symtest/data";
my $PATHVIVORECORDS="/root/vivo/harvester/example-scripts/example-elements/data/translated-records";

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

	#Photo, profile, research interests
	my $photo = $entry->{"jpegphoto"}[0];
	my $profile = $entry->{"researcherprofile"}[0];




	$profile = decode_entities(decode_entities($profile));

	my $jpegFile1 = "$PATHFULL/$username.jpg";
	open(TMP, "+>$jpegFile1");
	binmode(TMP);
	$| = 1;
	print TMP $photo;
	close(TMP);

	my $jpegFile2 = "$PATHTHUMB/$username.thumbnail.jpg";
        open(TMP, "+>$jpegFile2");
        binmode(TMP);
        $| = 1;
        print TMP $photo;
        close(TMP);

	# check file size - fill 0-images with placeholder
 	my $filesize = -s $jpegFile2;
	if ($filesize == 0) {
		copy "/root/data.sgul.ac.uk-deploy/data.sgul.ac.uk/cron/vivo/sgulplus.jpg", $jpegFile1;
		copy "/root/data.sgul.ac.uk-deploy/data.sgul.ac.uk/cron/vivo/sgulplus.jpg", $jpegFile2;
	}

	my $resint = "cancer$username";
	if ($username eq "gsollazz") {
		$resint="cancerdbennett";
	}

	# generatee rdf
	my $rdfoutput = <<END;
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:foaf="http://xmlns.com/foaf/0.1/"
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
	 xmlns:rdfsyn="http://www.w3.org/1999/02/22-rdf-syntax-ns#"         
	 xmlns:vocab="http://purl.org/vocab/vann/"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:swvocab="http://www.w3.org/2003/06/sw-vocab-status/ns#"
         xmlns:core="http://vivoweb.org/ontology/core#"
         xmlns:dc="http://purl.org/dc/elements/1.1/">
   <rdf:Description rdf:about="$aboutBaseUrl/$username">
      <vitro-public:mainImage rdf:resource="http://vivo.sgul.ac.uk:8080/vivo15/individual/$username-image"/>
      <core:hasResearchArea rdf:resource="$baseUrl/individual/$resint"/>
      <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
      <rdf:type rdf:resource="http://vivoweb.org/harvester/excludeEntity"/>
      <rdf:type rdf:resource="http://vitro.mannlib.cornell.edu/ns/vitro/0.7#Flag1Value1Thing"/>
      <rdf:type rdf:resource="http://www.symplectic.co.uk/vivo/User"/>
      <core:overview>
	<![CDATA[$profile]]>
      </core:overview>
   </rdf:Description>
   <rdf:Description rdf:about="http://vivo.sgul.ac.uk:8080/vivo15/individual/$username-image">
      <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>
      <rdf:type rdf:resource="http://vitro.mannlib.cornell.edu/ns/vitro/public#File"/>
      <vitro-public:downloadLocation rdf:resource="http://vivo.sgul.ac.uk:8080/vivo15/individual/$username-imageDownload"/>
      <vitro-public:thumbnailImage rdf:resource="http://vivo.sgul.ac.uk:8080/vivo15/individual/$username-imageThumbnail"/>
      <vitro-public:filename>$username.jpg</vitro-public:filename>
      <vitro-public:mimeType>image/jpg</vitro-public:mimeType>
   </rdf:Description>
   <rdf:Description rdf:about="http://vivo.sgul.ac.uk:8080/vivo15/individual/$username-imageDownload">
      <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>
      <rdf:type rdf:resource="http://vitro.mannlib.cornell.edu/ns/vitro/public#FileByteStream"/>
      <vitro-public:directDownloadUrl>/harvestedImages/$username.jpg</vitro-public:directDownloadUrl>
   </rdf:Description>
   <rdf:Description rdf:about="http://vivo.sgul.ac.uk:8080/vivo15/individual/$username-imageThumbnail">
      <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>
      <rdf:type rdf:resource="http://vitro.mannlib.cornell.edu/ns/vitro/public#File"/>
      <vitro-public:downloadLocation rdf:resource="http://vivo.sgul.ac.uk:8080/vivo15/individual/$username-imageThumbnailDownload"/>
      <vitro-public:filename>$username.thumbnail.jpg</vitro-public:filename>
      <vitro-public:mimeType>image/jpeg</vitro-public:mimeType>
   </rdf:Description>
   <rdf:Description rdf:about="http://vivo.sgul.ac.uk:8080/vivo15/individual/$username-imageThumbnailDownload">
      <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>
      <rdf:type rdf:resource="http://vitro.mannlib.cornell.edu/ns/vitro/public#FileByteStream"/>
      <vitro-public:directDownloadUrl>/harvestedImages/$username.thumbnail.jpg</vitro-public:directDownloadUrl>
   </rdf:Description>
</rdf:RDF>
END



	# write rdf file
	my $vivoFile = "$PATHVIVORECORDS/user/phone$username";
	open(TMP, "+>$vivoFile");
	print TMP "$rdfoutput";
	close(TMP);


	# TODO just debug, then move these away
	# write research area rdf file
	my $resrdfoutput = <<END;
<rdf:RDF
    xmlns:hr="http://vivo.cornell.edu/ns/hr/0.9/hr.owl#"
    xmlns:c4o="http://purl.org/spar/c4o/"
    xmlns:vitro-public="http://vitro.mannlib.cornell.edu/ns/vitro/public#"
    xmlns:ero="http://purl.obolibrary.org/obo/"
    xmlns:pvs="http://vivoweb.org/ontology/provenance-support#"
    xmlns:vivo="http://vivoweb.org/ontology/core#"
    xmlns:stars="http://vitro.mannlib.cornell.edu/ns/cornell/stars/classes#"
    xmlns:aka="http://vivoweb.org/ontology/aka#"
    xmlns:rdfsyn="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:far="http://vitro.mannlib.cornell.edu/ns/reporting#"
    xmlns:bibo="http://purl.org/ontology/bibo/"
    xmlns:foaf="http://xmlns.com/foaf/0.1/"
    xmlns:local="http://vivo.cornell.edu/ontology/local#"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:scires="http://vivoweb.org/ontology/scientific-research#"
    xmlns:acti="http://vivoweb.org/ontology/activity-insight#"
    xmlns:aktp="http://www.aktors.org/ontology/portal#"
    xmlns:geo="http://aims.fao.org/aos/geopolitical.owl#"
    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns:event="http://purl.org/NET/c4dm/event.owl#"
    xmlns:socsci="http://vivo.library.cornell.edu/ns/vivo/socsci/0.1#"
    xmlns:dcelem="http://purl.org/dc/elements/1.1/"
    xmlns:ospcu="http://vivoweb.org/ontology/cu-vivo-osp#"
    xmlns:vitro="http://vitro.mannlib.cornell.edu/ns/vitro/0.7#"
    xmlns:vivoc="http://vivo.library.cornell.edu/ns/0.1#"
    xmlns:pubmed="http://vitro.mannlib.cornell.edu/ns/pubmed#"
    xmlns:cce="http://vivoweb.org/ontology/cornell-cooperative-extension#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:mann="http://vivo.cornell.edu/ns/mannadditions/0.1#"
    xmlns:owl="http://www.w3.org/2002/07/owl#"
    xmlns:fabio="http://purl.org/spar/fabio/"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" > 
 <rdf:Description about="$baseUrl/individual/cancer$username">
    <rdf:type rdf:resource="http://vivoweb.org/ontology/core#SubjectArea"/>
    <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#Concept"/>
    <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>
    <rdfs:label>cancer$username</rdfs:label>
  </rdf:Description>
</rdf:RDF>
END

	
my $vivoFile = "$PATHVIVORECORDS/user/researchcancer$username";
open(TMP, "+>$vivoFile");
print TMP "$resrdfoutput";
close(TMP);



        $entry = $conn->nextEntry();
}

