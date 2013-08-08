<?php

require("Toro.php");
require("sparqllib.php");

function fixBadUnicodeForJson($str) {
    $str = preg_replace("/\\\\u00([0-9a-f]{2})\\\\u00([0-9a-f]{2})\\\\u00([0-9a-f]{2})\\\\u00([0-9a-f]{2})/e", 'chr(hexdec("$1")).chr(hexdec("$2")).chr(hexdec("$3")).chr(hexdec("$4"))', $str);
    $str = preg_replace("/\\\\u00([0-9a-f]{2})\\\\u00([0-9a-f]{2})\\\\u00([0-9a-f]{2})/e", 'chr(hexdec("$1")).chr(hexdec("$2")).chr(hexdec("$3"))', $str);
    $str = preg_replace("/\\\\u00([0-9a-f]{2})\\\\u00([0-9a-f]{2})/e", 'chr(hexdec("$1")).chr(hexdec("$2"))', $str);
    $str = preg_replace("/\\\\u00([0-9a-f]{2})/e", 'chr(hexdec("$1"))', $str);
    $str = htmlentities($str);
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

class PubGetHandler {
    function get() {
      echo "PubGet";
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

class JobGetHandler {
    function get() {
      echo "JobGet";
    }
}

class JobSearchHandler {
    function get() {
      echo "JobSearch";
    }
}

class SparqlHandler {
	function get() {
		$data = sparql_get( 
				"http://data.sgul.ac.uk:8282/sparql/",
				"
				PREFIX bibo: <http://purl.org/ontology/bibo/>
				PREFIX sgul: <http://sgul.ac.uk/ontology/lib/>
                PREFIX vivo: <http://vivoweb.org/ontology/core#>
				PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
				PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>


				SELECT ?s ?title ?o WHERE {
                                     ?s sgul:repositoryLink ?o.
                                     ?s rdfs:label ?title.

				} LIMIT 2000

				" );
		if( !isset($data) )
		{
			print "<p>Error: ".sparql_errno().": ".sparql_error()."</p>";
		}

		print "<table class='example_table'>";
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
				print "<td>$row[$field] |</td> ";
			}
			print "</tr>";
		}
		print "</table>";
	}
}


Toro::serve(array(
			"/" => "HelloHandler",
			"/abc" => "HelloHandler",
			"/publications/list" => "PubListHandler",
			"/publications/get/:number" => "PubGetHandler",
			"/publications/search/:alpha" => "PubSearchHandler",
			"/jobs/list" => "JobListHandler",
			"/jobs/get/:alpha" => "JobGetHandler",
			"/jobs/search/:alpha" => "JobSearchHandler",
			"/sparql" => "SparqlHandler",
		 ));
