#!/usr/bin/perl
use Mozilla::LDAP::Conn;                # Main "OO" layer for LDAP
use Mozilla::LDAP::Utils;               # LULU, utilities.
use URI::Escape;
use WWW::Mechanize;
use JSON -support_by_pp;
use strict;

# read config file
my $json;
{
  local $/; 
  open my $fh, "<", "config.json";
  $json = <$fh>;
} 
print $json;
my $JSONPARSER = new JSON;
my $json_text = $JSONPARSER->allow_nonref->utf8->relaxed->escape_slash->loose->allow_singlequote->allow_barekey->decode($json);

my $ldap_host = $json_text->{ldap}->{host};
my $ldap_port = $json_text->{ldap}->{port};
my $bind_user = $json_text->{ldap}->{binduser};
my $bind_pass = $json_text->{ldap}->{bindpass};
my $search_base = $json_text->{ldap}->{searchbase};
 
# connect to LDAP host
my $conn = new Mozilla::LDAP::Conn($ldap_host, $ldap_port, $bind_user, $bind_pass,"") || die "Can't connect to $ldap_host.\n";


# create general 
print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
print "<rdf:RDF\n";
print "  xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n";
print "  xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n";
print "  xmlns:foaf=\"http://xmlns.com/foaf/0.1/\"\n";
print "  xmlns:con=\"http://www.w3.org/2000/10/swap/pim/contact#\"\n";
print "  xmlns:geo=\"htp://www.w3.org/2003/01/geo/wgs84_pos#\">";

# read the ldap entries and generate the foaf extract
my $entry = $conn->search($search_base, "subtree", "(uid=*)");
while ($entry) {

	# download data
        my $mail=$entry->{"mail"}[0];
	my $cn=uri_escape($entry->{"cn"}[0]);
	my $sn=uri_escape($entry->{"sn"}[0]);
	my $givenname=uri_escape($entry->{"givenname"}[0]);
    	my $title=$entry->{"title"}[0];
    	my $telephonenumber=$entry->{"telephonenumber"}[0];
	my $researchinterests=$entry->{"researchinterests"}[0];
	my @resint = split(/,/, $researchinterests);
	my $lat = "51.427518";
	my $lon = "-0.175449";
	my $city = "London";
	my $country = "England";
	my $postalcode = "SW17 0RE";
	my $street = "Cranmer Terrace";

	# create extracts
	print "    <foaf:Person>\n";
        print "        <foaf:title>$title</foaf:title>\n";
        print "        <foaf:name>$cn</foaf:name>\n";
        print "        <foaf:family_name>$sn</foaf:family_name>\n";
        print "        <foaf:givenname>$givenname</foaf:givenname>\n";
	print "        <foaf:mbox rdf:resource=\"mailto:$mail\"/>\n";
        foreach (@resint) {
		my $interest = uri_escape($_);
	        print "        <foaf:interest>$interest</foaf:interest>\n";
        }
	print "        <foaf:workplaceHomapage rdf:resource=\"http://www.sgul.ac.uk\"/>\n";
	print "        <foaf:phone rdf:resource=\"tel:$telephonenumber\"/>\n";
	print "        <foaf:based_near rdf:parseType=\"Resource\">\n";
	print "            <geo:lat>$lat</geo:lat>\n";
	print "            <geo:long>$lon</geo:long>\n";
	print "        </foaf:based_near>\n";
	print "        <con:office rdf:parseType=\"Resource\">\n";
	print "            <con:address rdf:parseType=\"Resource\">\n";
	print "                <con:city>$city</con:city>\n";
	print "                <con:country>$country</con:country>\n";
	print "                <con:postalCode>$postalcode</con:postalCode>\n";
	print "                <con:street>$street</con:street>\n";
	print "            </con:address>\n";
	print "            <con:phone rdf:resource=\"tel:$telephonenumber\"/>\n";
	print "            <geo:location rdf:parseType=\"Resource\">\n";
	print "                <geo:lat>$lat</geo:lat>\n";
	print "                <geo:long>$lon</geo:long>\n";
	print "            </geo:location>\n";
	print "        </con:office>\n";
        print "    </foaf:Person>\n";
        $entry = $conn->nextEntry();
}

print "</rdf:RDF>";
exit 1;
