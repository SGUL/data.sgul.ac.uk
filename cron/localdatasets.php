<?php


	
	# Course modules
	$filename="./datasets_local/coursemodules.csv";
	$csv = array_map("str_getcsv", file("$filename",FILE_SKIP_EMPTY_LINES));
	$keys = array_shift($csv);
	foreach ($csv as $i=>$row) {
		$csv[$i] = array_combine($keys, $row);
	}
	$jsonfile = "./cron/output/coursemodules.json";
	$f_json = fopen($jsonfile, 'w') or die("can't open file");
	fwrite($f_json, json_encode($csv));
	fclose($f_json);



	foreach ($csv as $line=>$arrvalue) {
		$code = $arrvalue["Module code"];
		$name = $arrvalue["Full name"];
		


		$rdf = printCoursesRDF($code, $name);
        $rdffile = "./cron/output/course_$code.rdf";
        $f_rdf = fopen($rdffile, 'w') or die("can't open file");
        fwrite($f_rdf, $rdf);
        fclose($f_rdf);

	}

	
function printCoursesRDF($code, $name) {

    echo "$code, $name\n";

     $rdfprint = '<?xml version="1.0" encoding="UTF-8"?>
 <rdf:RDF 
 	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
 	xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:sgul="http://data.sgul.ac.uk/ontology/courses/">
    
<rdf:Description rdf:about="sgulmodule:'.$code.'">
     <rdf:type rdf:resource="http://xcri.org/profiles/1.2/course"/>
     <rdfs:label>'.xmlentities($name).'</rdfs:label>
 </rdf:Description>
 </rdf:RDF>';
     return $rdfprint;

}
function xmlentities($string) { 
   return str_replace ( array ( '&', '"', "'", '<', '>', '�' ), array ( '&amp;' , '&quot;', '&apos;' , '&lt;' , '&gt;', '&apos;' ), $string ); 
} 
?>