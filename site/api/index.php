<?php

require("Toro.php");
require("sparqllib.php");

function fixBadUnicodeForJson($str) {
    $str = preg_replace("/\\\\u00([0-9a-f]{2})\\\\u00([0-9a-f]{2})\\\\u00([0-9a-f]{2})\\\\u00([0-9a-f]{2})/e", 'chr(hexdec("$1")).chr(hexdec("$2")).chr(hexdec("$3")).chr(hexdec("$4"))', $str);
    $str = preg_replace("/\\\\u00([0-9a-f]{2})\\\\u00([0-9a-f]{2})\\\\u00([0-9a-f]{2})/e", 'chr(hexdec("$1")).chr(hexdec("$2")).chr(hexdec("$3"))', $str);
    $str = preg_replace("/\\\\u00([0-9a-f]{2})\\\\u00([0-9a-f]{2})/e", 'chr(hexdec("$1")).chr(hexdec("$2"))', $str);
    $str = preg_replace("/\\\\u00([0-9a-f]{2})/e", 'chr(hexdec("$1"))', $str);
    //$str = htmlentities($str);
    return $str;
}

class HelloHandler {
    function get() {
      echo "Hello, world";
    }
}

// Publications

class PubListHandler {
    function get() {
      $data = sparql_get( 
				"http://data.sgul.ac.uk:8282/sparql/",
				"
                
  				PREFIX bibo: <http://purl.org/ontology/bibo/>
				PREFIX sgul: <http://sgul.ac.uk/ontology/lib/>
                PREFIX vivo: <http://vivoweb.org/ontology/core#>
				PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
				PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>


				SELECT ?s ?title ?authorList ?repositoryLink ?doi  WHERE {
                	?s sgul:repositoryLink ?repositoryLink.
                	?s rdfs:label ?title.
                	?s bibo:authorList ?authorList.
                	?s bibo:doi ?doi.
				} LIMIT 2000

				" );
		if( !isset($data) )
		{
			print "<p>Error: ".sparql_errno().": ".sparql_error()."</p>";
		}

		
		$json_output = array();
		
		foreach( $data as $row )
		{
			$this_row = array();
			foreach( $data->fields() as $field )
			{
				$this_row[$field] = fixBadUnicodeForJson($row[$field]);
			}
			$json_output[] = $this_row;
		}


		print json_encode($json_output);
    }
}

class LibraryCatalogueHandler {
    function get() {
    	$json_output = array();
      	$json_output = json_encode($json_output);
      	print $json_output;
    }
}

class PubSearchHandler {
    function get() {
      echo "PubSearch";
    }
}

// Jobs

class JobListHandler {
    function get() {

      $data = sparql_get( 
				"http://data.sgul.ac.uk:8282/sparql/",
				"
                
  				PREFIX vacancy: <http://purl.org/openorg/vacancy/>
				PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>


				SELECT ?title ?employer ?ou ?salary ?url ?dateInterviewBy ?dateClosing WHERE {
					?s rdfs:label ?title.
					?s vacancy:employer ?employer.
					?s vacancy:salary ?salary.
					?s vacancy:availableOnline ?url.
					?s vacancy:organizationalUnit ?ou.
					?s vacancy:applicationInterviewNotificationByDate ?dateInterviewBy.
					?s vacancy:applicationClosingDate ?dateClosing.
				}

				" );

		if( !isset($data) )
		{
			print "<p>Error: ".sparql_errno().": ".sparql_error()."</p>";
		}

		
		$json_output = array();
		
		foreach( $data as $row )
		{
			$this_row = array();
			foreach( $data->fields() as $field )
			{
				$this_row[$field] = fixBadUnicodeForJson($row[$field]);
			}
			$json_output[] = $this_row;
		}


		print json_encode($json_output);
    }
}



class SparqlHandler {
	function post() {
      	$query = $_POST['query'];
      	

    //   	"
				// PREFIX vacancy: <http://purl.org/openorg/vacancy/>
				// PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>


				// SELECT ?title ?employer ?ou ?salary ?url ?dateInterviewBy ?dateClosing WHERE {
				// 	?s rdfs:label ?title.
				// 	?s vacancy:employer ?employer.
				// 	?s vacancy:salary ?salary.
				// 	?s vacancy:availableOnline ?url.
				// 	?s vacancy:organizationalUnit ?ou.
				// 	?s vacancy:applicationInterviewNotificationByDate ?dateInterviewBy.
				// 	?s vacancy:applicationClosingDate ?dateClosing.
				// }
				// "
      
		$data = sparql_get( 
				"http://data.sgul.ac.uk:8282/sparql/",
				$query );
		if( !isset($data) )
		{
			print "<p>Error: ".sparql_errno().": ".sparql_error()."</p>";
		}

		print "<table border=1>";
		print "<tr>";
		foreach( $data->fields() as $field )
		{
			print "<th>$field</th>";
		}
		print "</tr>";
		foreach( $data as $row )
		{
			print "<tr>";
			foreach( $data->fields() as $field )
			{
				print "<td>$row[$field]</td> ";
			}
			print "</tr>";
		}
		print "</table>";
	}
}

class CatalogueRdfHandler {
    function get() {
      echo "Catalogue";
    }
}


class CatalogueJsonHandler {
    function get() {
    	$filecontents = file_get_contents("../output/catalogue.json");
		print $filecontents;
    }
}

Toro::serve(array(
			"/" => "HelloHandler",
			"/catalogue/rdf" => "CatalogueRdfHandler",
			"/catalogue/json" => "CatalogueJsonHandler",
			"/publications/list" => "PubListHandler",
			"/jobs/list" => "JobListHandler",
			"/sparql2table" => "SparqlHandler",
			"/library/catalogue" => "LibraryCatalogueHandler",
		 ));
