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
my $JSONPARSER = new JSON;
my $json_text = $JSONPARSER->allow_nonref->utf8->relaxed->escape_slash->loose->allow_singlequote->allow_barekey->decode($json);

my $ldap_host = $json_text->{ldap}->{host};
my $ldap_port = $json_text->{ldap}->{port};
my $bind_user = $json_text->{ldap}->{binduser};
my $bind_pass = $json_text->{ldap}->{bindpass};
my $search_base = $json_text->{ldap}->{searchbase};

my $PATHFULL="/usr/local/vivo15test/data";
my $PATHTHUMB="/usr/local/vivo15test/data/thumbnails/";

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
	my $photo = $entry->{"jpegphoto"}[0];


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

        $entry = $conn->nextEntry();
}

exit 1;
