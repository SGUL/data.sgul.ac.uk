<?php

require("Toro.php");
require("sparqllib.php");

class HelloHandler {
    function get() {
      echo "Hello, world";
    }
}

// Publications

class PubListHandler {
    function get() {
      echo "PubList";
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
      echo "JobList";
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

				SELECT * WHERE {
					 ?s ?p ?o
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
			"/publications/list/:string" => "PubListHandler",
			"/publications/get/:number" => "PubGetHandler",
			"/publications/search/:alpha" => "PubSearchHandler",
			"/jobs/list/:string" => "JobListHandler",
			"/jobs/get/:alpha" => "JobGetHandler",
			"/jobs/search/:alpha" => "JobSearchHandler",
			"/sparql" => "SparqlHandler",
		 ));
