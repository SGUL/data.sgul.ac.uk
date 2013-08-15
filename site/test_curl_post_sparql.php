<?php
extract($_POST);

//set POST variables
$url = 'http://data.sgul.ac.uk/api/sparql2table';

$sparql = "
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX sgul: <http://sgul.ac.uk/ontology/lib/>
PREFIX vivo: <http://vivoweb.org/ontology/core#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?publication ?title ?doi ?authors WHERE {
        ?publication bibo:doi ?doi.
        ?publication rdfs:label ?title.
        ?publication bibo:authorList ?authors.
}";

$fields = array(
						'query' => $sparql,
				);

//url-ify the data for the POST
$fields_string = "";
foreach($fields as $key=>$value) { $fields_string .= $key.'='.$value.'&'; }
rtrim($fields_string, '&');

//open connection
$ch = curl_init();

//set the url, number of POST vars, POST data
curl_setopt($ch,CURLOPT_URL, $url);
curl_setopt($ch,CURLOPT_POST, count($fields));
curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);

//execute post
$result = curl_exec($ch);

//close connection
curl_close($ch);
?>
