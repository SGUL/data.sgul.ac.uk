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
#use warnings;
# read config file
my $json;
{
  local $/; 
  open my $fh, "<", "/root/data.sgul.ac.uk/cron/config.json";
  $json = <$fh>;
} 
my $JSONPARSER = new JSON;
my $json_text = $JSONPARSER->allow_nonref->utf8->relaxed->escape_slash->loose->allow_singlequote->allow_barekey->decode($json);

my $ldap_host = $json_text->{ldap}->{host};
my $ldap_port = $json_text->{ldap}->{port};
my $bind_user = $json_text->{ldap}->{binduser};
my $bind_pass = $json_text->{ldap}->{bindpass};
my $search_base = $json_text->{ldap}->{searchbase};

my $baseUrl = "http://vivo.sgul.ac.uk:8080/vivo15_43_test";
my $aboutBaseUrl= "http://vivo.symplectic.co.uk/individual";


my $PATHFULL="/usr/local/vivo15_43_test/data";
my $PATHTHUMB="/usr/local/vivo15_43_test/data";
my $PATHVIVORECORDS="/root/vivo_test/harvester/example-scripts/example-elements/data/translated-records";

# connect to LDAP host
my $conn = new Mozilla::LDAP::Conn($ldap_host, $ldap_port, $bind_user, $bind_pass,"") || die "Can't connect to $ldap_host.\n";
my $rescount = 0;

# read the ldap entries and generate the vivo extracts
my %researchDictionary = ();

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
	my @interests = $entry->getValues("researchinterests");
	
	my $resnamenospace="";
	my $resstring="";
	foreach (@interests) {
		if ($_) { 
		my $avoiderror = $_;
		$avoiderror =~ s/&/&amp;/g;
		$avoiderror =~ tr/\015//d;
		$avoiderror =~ s/\<//g;
		

		if (exists $researchDictionary{ $avoiderror }) {
			$resnamenospace = $researchDictionary { $avoiderror };		
		} else {
			$rescount++;
			$resnamenospace="res$rescount";
			%researchDictionary->{ $avoiderror } = $resnamenospace;

			
		}
		# Create research string for profile
		$resstring = <<END;
$resstring<core:hasResearchArea rdf:resource="$baseUrl/individual/$resnamenospace"/>
END

	
		# Create research area own file
		my $resrdfoutput = <<END;
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
xmlns:vitro-public="http://vitro.mannlib.cornell.edu/ns/vitro/public#"
xmlns:vivo="http://vivoweb.org/ontology/core#"
xmlns:rdfsyn="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:bibo="http://purl.org/ontology/bibo/"
xmlns:foaf="http://xmlns.com/foaf/0.1/"
xmlns:vitro="http://vitro.mannlib.cornell.edu/ns/vitro/0.7#"
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:owl="http://www.w3.org/2002/07/owl#"
xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" >
<rdf:Description rdf:about="$baseUrl/individual/$resnamenospace">
<rdf:type rdf:resource="http://vivoweb.org/ontology/core#SubjectArea"/>
<rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#Concept"/>
<rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>
<rdfs:label>$avoiderror</rdfs:label>
<vivo:researchAreaOf rdf:resource="$aboutBaseUrl/$username"/>
</rdf:Description>
</rdf:RDF>
END


my $vivoFile = "$PATHVIVORECORDS/user/$resnamenospace.$username";
open(TMP, "+>$vivoFile");
print TMP "$resrdfoutput";
close(TMP);	

} 
}


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
		copy "/root/data.sgul.ac.uk/cron/vivo/sgulplus.jpg", $jpegFile1;
		copy "/root/data.sgul.ac.uk/cron/vivo/sgulplus.jpg", $jpegFile2;
	}

	
	# generatee rdf for researcher
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
      <vitro-public:mainImage rdf:resource="$baseUrl/individual/$username-image"/>
	$resstring
      <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
      <rdf:type rdf:resource="http://vivoweb.org/harvester/excludeEntity"/>
      <rdf:type rdf:resource="http://vitro.mannlib.cornell.edu/ns/vitro/0.7#Flag1Value1Thing"/>
      <rdf:type rdf:resource="http://www.symplectic.co.uk/vivo/User"/>
      <core:overview>
	<![CDATA[$profile]]>
      </core:overview>
   </rdf:Description>
   <rdf:Description rdf:about="$baseUrl/individual/$username-image">
      <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>
      <rdf:type rdf:resource="http://vitro.mannlib.cornell.edu/ns/vitro/public#File"/>
      <vitro-public:downloadLocation rdf:resource="$baseUrl/individual/$username-imageDownload"/>
      <vitro-public:thumbnailImage rdf:resource="$baseUrl/individual/$username-imageThumbnail"/>
      <vitro-public:filename>$username.jpg</vitro-public:filename>
      <vitro-public:mimeType>image/jpg</vitro-public:mimeType>
   </rdf:Description>
   <rdf:Description rdf:about="$baseUrl/individual/$username-imageDownload">
      <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>
      <rdf:type rdf:resource="http://vitro.mannlib.cornell.edu/ns/vitro/public#FileByteStream"/>
      <vitro-public:directDownloadUrl>/harvestedImages/$username.jpg</vitro-public:directDownloadUrl>
   </rdf:Description>
   <rdf:Description rdf:about="$baseUrl/individual/$username-imageThumbnail">
      <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>
      <rdf:type rdf:resource="http://vitro.mannlib.cornell.edu/ns/vitro/public#File"/>
      <vitro-public:downloadLocation rdf:resource="$baseUrl/individual/$username-imageThumbnailDownload"/>
      <vitro-public:filename>$username.thumbnail.jpg</vitro-public:filename>
      <vitro-public:mimeType>image/jpeg</vitro-public:mimeType>
   </rdf:Description>
   <rdf:Description rdf:about="$baseUrl/individual/$username-imageThumbnailDownload">
      <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>
      <rdf:type rdf:resource="http://vitro.mannlib.cornell.edu/ns/vitro/public#FileByteStream"/>
      <vitro-public:directDownloadUrl>/harvestedImages/$username.thumbnail.jpg</vitro-public:directDownloadUrl>
   </rdf:Description>
</rdf:RDF>
END


	# generate reverse rdf for research interest
	

	my $vivoFile = "$PATHVIVORECORDS/user/phone$username";
	open(TMP, "+>$vivoFile");
	print TMP "$rdfoutput";
	close(TMP);

        $entry = $conn->nextEntry();
}

