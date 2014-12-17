<?php



$string = file_get_contents("./cron/config.json");

//echo $string;
$json_a=json_decode($string,true);




$cris_url = $json_a['cris']['url'];
$cris_port = $json_a['cris']['port'];
$cris_user = $json_a['cris']['user'];
$cris_pass = $json_a['cris']['pass'];



	
$pub_list_page_1 = "$cris_url:$cris_port/publications-api/publications?detail=full&page=1";
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL,$pub_list_page_1);
curl_setopt($ch, CURLOPT_TIMEOUT, 30); //timeout after 30 seconds
curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);
curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_ANY);
curl_setopt($ch, CURLOPT_USERPWD, "$cris_user:$cris_pass");
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);   //get status code
$result=curl_exec ($ch);
curl_close ($ch);


$dom = new DOMDocument();
$dom->loadXML($result);

$xpath = new DOMXpath($dom);
$last = $xpath->query('//api:page[@position="last"]')->item(0)->getAttribute('href');
$next = $xpath->query('//api:page[@position="next"]')->item(0)->getAttribute('href');
$thispage = $xpath->query('//api:page[@position="this"]')->item(0)->getAttribute('href');

$json_output = array();
$csvfile = "./cron/output/publications.csv";
$jsonfile = "./cron/output/publications.json";

$f_csv = fopen($csvfile, 'w') or die("can't open file");
$f_json = fopen($jsonfile, 'w') or die("can't open file");
$page=0;
do
{
	$page++;
    $parsed=parse_url($last);
    $lastpage=explode("=",$parsed['query']) ;
	echo $page." of ".$lastpage[2]."\n";
	$pub_list_page = "$cris_url:$cris_port/publications-api/publications?detail=full&page=$page";
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL,$pub_list_page);
	curl_setopt($ch, CURLOPT_TIMEOUT, 30); //timeout after 30 seconds
	curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);
	curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_ANY);
	curl_setopt($ch, CURLOPT_USERPWD, "$cris_user:$cris_pass");
	$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);   //get status code
	$result=curl_exec ($ch);
	curl_close ($ch);
	

	$dom = new DOMDocument();
	$dom->loadXML($result);
	
	$xpath = new DOMXpath($dom);
	$xpath->registerNamespace("atom","http://www.w3.org/2005/Atom");
	$last = $xpath->query('//api:page[@position="last"]')->item(0)->getAttribute('href');
	$next = $xpath->query('//api:page[@position="next"]');
	
	if ($next->length > 0)
		$next = $next->item(0)->getAttribute('href');
	$thispage = $xpath->query('//api:page[@position="this"]')->item(0)->getAttribute('href');



	$entries = $xpath->query('//atom:entry');
	
	
	

	for ($i = 0; $i < $entries->length; $i++) {
		$entry = $entries->item($i);
		$pub_id = $xpath->query('api:object',$entry)->item(0)->getAttribute('id');
		$pubdict = getPublicationDetails($pub_id);

		if ($pubdict['repository'] <> "none") {
			$rdf = printRDF($pubdict);
            $rdffile = "./cron/output/pub_$pub_id.rdf";
            $f_rdf = fopen($rdffile, 'w') or die("can't open file");
            fwrite($f_rdf, $rdf);
            fclose($f_rdf);

            $csv = printCSV($pubdict);
            fwrite($f_csv, $csv);
            $json_output[] = $pubdict;
            

		}

	}
   

 
} while ($thispage <> $last);
var_dump($json_output);
fclose($f_csv);
fwrite($f_json, json_encode($json_output));
fclose($f_json);

function getPublicationDetails($pub_id) {
	global $cris_url, $cris_port, $cris_user, $cris_pass;
	$pubdet = array();
	$url = "$cris_url:$cris_port/publications-api/publications/$pub_id";


	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL,$url);
	curl_setopt($ch, CURLOPT_TIMEOUT, 30); //timeout after 30 seconds
	curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);
	curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_ANY);
	curl_setopt($ch, CURLOPT_USERPWD, "$cris_user:$cris_pass");
	$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);   //get status code
	$result=curl_exec ($ch);
	curl_close ($ch);

	$dom = new DOMDocument();
	$dom->loadXML($result);
	$xpath = new DOMXpath($dom);
	$xpath->registerNamespace("atom","http://www.w3.org/2005/Atom");

	$title = $xpath->query("//atom:title")->item(0)->nodeValue;
	$pubdet['title'] = $title;


	//  get records with source-id
	$recordindex = 100;
    $winningrecord = array();
    $records = $xpath->query("//api:record");



    // choose the preferred record
	for ($i = 0; $i < $records->length; $i++) {
		$record = $records->item($i);

		


		$sourceId = $record->getAttribute('source-id');
		if (is_numeric($sourceId)) {
			if ($sourceId < $recordindex) {
				$recordindex = $sourceId;
				$winningrecord = $record;
				}
		}
	}


	

	$abstract=$xpath->query('api:native/api:field[@name="abstract"]',$winningrecord);

	// $newdoc = new DOMDocument;
	// $node = $newdoc->importNode($abstract->item(0), true);
	// $newdoc->appendChild($node);
	// $html = $newdoc->saveXML();
	//echo $html;


	if ($abstract->length > 0) {
		$abstract = $abstract->item(0)->nodeValue;
		//$pubdet['abstract'] = htmlentities($abstract, ENT_QUOTES, 'utf-8', FALSE); // TODO for XML
        $pubdet['abstract'] = $abstract;
	} else {
		$pubdet['abstract'] = "";	
	}

	
	
	$doi=$xpath->query('api:native/api:field[@name="doi"]',$winningrecord);
	if ($doi->length > 0) {
		$doi = $doi->item(0)->nodeValue;
		$pubdet['doi'] = $doi;
	} else {
		$pubdet['doi'] = "";	
	}


	$authors=array();
	$people=$xpath->query('api:native/api:field[@name="authors"]/api:people/api:person',$winningrecord);
	if ($people->length > 0) {

		for ($j = 0; $j < $people->length; $j++) {
			$author = $people->item($j);
			$lastName = $xpath->query('api:last-name',$author)->item(0)->nodeValue;
			$initials = $xpath->query('api:initials',$author)->item(0)->nodeValue;
			$authors[] = "$lastName, $initials";
		}
		
		$pubdet['authors'] = $authors;
	} else {
		$pubdet['authors'] = "";	
	}

	
	$year = $xpath->query('//api:field[@name="publication-date"]/api:date/api:year');
	$pubdet['year'] = "";
	if ($year->length > 0) {
		$pubdet['year']=$year->item(0)->nodeValue;
	} 
	

	$repositoryitem_list = $xpath->query('//api:object/api:repository-items/api:repository-item');
    
	
    $pubdet['repository'] = "none";
    
	if ($repositoryitem_list->length > 0) {
		$repositoryitem = $repositoryitem_list->item(0);

		
        $repositorycount = $xpath->query('api:licence-file-count', $repositoryitem)->item(0)->nodeValue;

        if ($repositorycount > 0) {
            
            $repositoryurl = $xpath->query('api:public-url', $repositoryitem);
            if ($repositoryurl->length > 0) {

                $repositoryurl = $repositoryurl->item(0)->nodeValue;
                echo "$pub_id : $repositoryurl\n";
                $repositorypdflist = $xpath->query('api:repository-files',$repositoryitem);
                if ($repositorypdflist ->length > 0) {
                    // $repositorypdf = $repositorypdflist->item(0);
                    // $repositorypdfurl = $xpath->query('api:repository-file',$repositorypdf)->item(0)->nodeValue;
                    $pubdet['repository']=$repositoryurl;
                    
                }
            }
            
        } 
    } 	
	
	


	$pubdet['url'] = $url;
	return $pubdet;
}

function xmlentities($string) { 
   return str_replace ( array ( '&', '"', "'", '<', '>', '�' ), array ( '&amp;' , '&quot;', '&apos;' , '&lt;' , '&gt;', '&apos;' ), $string ); 
} 

function printRDF($pubdic) {

    $puburl = $pubdic['url'];
    $authorsList = "";
    foreach ($pubdic['authors'] as $author) {
        $thisauthor = "<dc:author>".xmlentities($author)."</dc:author>";
        $authorsList = $authorsList.$thisauthor;
    }
    
    
    $title = $pubdic['title'];
    $abstract = $pubdic['abstract'];
    $doi = $pubdic['doi'];
    $year = $pubdic['year'];
    $repository = $pubdic['repository'];

    $rdfprint = '<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:bibo="http://purl.org/ontology/bibo/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:sgul="http://data.sgul.ac.uk/ontology/lib/"
    xmlns:vivo="http://vivoweb.org/ontology/core#">

<rdf:Description rdf:about="'.$puburl.'">
    <rdf:type rdf:resource="http://purl.org/ontology/bibo/AcademicArticle"/>
    <rdf:type rdf:resource="http://purl.org/ontology/bibo/Article"/>
    <rdf:type rdf:resource="http://purl.org/ontology/bibo/Document"/>
    <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Thing"/>
    <rdfs:label>'.xmlentities($title).'</rdfs:label>
    <bibo:abstract>'.xmlentities($abstract).'</bibo:abstract>
    <bibo:doi>'.$doi.'</bibo:doi>'.$authorsList.'
    <vivo:dateTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">'.$year.'</vivo:dateTime>
    <sgul:repositoryLink>'.$repository.'</sgul:repositoryLink>
</rdf:Description>
</rdf:RDF>';
    return $rdfprint;

}

function printCSV($pubdic) {
    $puburl = $pubdic['url'];
    $authorsList = "";
    foreach ($pubdic['authors'] as $author) {
        $authorsList = "$authorsList;$author";
    }
    $authorsList = substr($authorsList, 1);
    $title = $pubdic['title'];
    $doi = $pubdic['doi'];
    $year = $pubdic['year'];
    $repository = $pubdic['repository'];

    $csvprint = "$puburl|$title|$doi|$authorsList|$year|$repository\n";
    return $csvprint;
}



?>
