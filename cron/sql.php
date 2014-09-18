<?php

# Get config data

$string = file_get_contents("./cron/config.json");
$json_a=json_decode($string,true);

$mysql_host = $json_a['mysql']['host'];
$mysql_db = $json_a['mysql']['host'];
$mysql_user = $json_a['mysql']['user'];
$mysql_pass = $json_a['mysql']['pass'];


# Connect to mysql
$con=mysqli_connect($mysql_host,$mysql_user,$mysql_pass,$mysql_db);

if (mysqli_connect_errno()) {
  die("Failed to connect to MySQL: " . mysqli_connect_error());
}

# DATA CATALOGUE
$string = file_get_contents("./site/output/datacatalogue.json");
$json_cat=json_decode($string,true);
// NB it assumes dos2unix has happened

# Delete
$sql1 = <<<SQL
DELETE FROM datacatalogue WHERE 1;
SQL;

if(!$result = mysqli_query($con,$sql1)){
    die('There was an error running the query [' . $con->error . ']');
}
foreach ($json_cat as $index=>$contents) {
	$csv = $json_cat[$index]['csv'];
	$json = $json_cat[$index]['json'];
	$rdfdump = $json_cat[$index]['rdfdump'];
	$humanurl = $json_cat[$index]['humanurl'];
		


	$sql2 = <<<SQL
INSERT INTO datacatalogue (name, humanurl, csv, json, rdfdump)
VALUES ("$index", "$humanurl", "$csv", "$json", "$rdfdump");
SQL;

	if(!$result = mysqli_query($con,$sql2)){
	    die('There was an error running the query [' . $con->error . ']');
	}
		
}

# COURSEMODULES
$string = file_get_contents("./site/output/coursemodules.json");
$json_cat=json_decode($string,true);
// NB it assumes dos2unix has happened
	
# Delete
$sql1 = <<<SQL
DELETE FROM coursemodules WHERE 1;
SQL;

if(!$result = mysqli_query($con,$sql1)){
    die('There was an error running the query [' . $con->error . ']');
}
foreach ($json_cat as $element) {
	$code = $element["Module code"];
	$name = $element["Full name"];
	
	$sql2 = <<<SQL
INSERT INTO coursemodules (modulecode, fullname)
VALUES ("$code", "$name");
SQL;

	if(!$result = mysqli_query($con,$sql2)){
	    die('There was an error running the query [' . $con->error . ']');
	}	
}

# JOBS
$string = file_get_contents("./site/output/jobs.json");
// NB it assumes dos2unix has happened
$json_cat=json_decode($string,true);




# Delete
$sql1 = <<<SQL
DELETE FROM jobs WHERE 1;
SQL;

if(!$result = mysqli_query($con,$sql1)){
    die('There was an error running the query [' . $con->error . ']');
}

foreach ($json_cat as $element) {


    $closing_date = $element["closing_date"];
    $interview_date = $element["interview_date"];
    $reference = $element["reference"];
    $salary = $element["salary"];
    $title = $element["title"];
    $topic = $element["topic"];
    $type = $element["type"];
    $url = $element["url"];
	
	$sql2 = <<<SQL
INSERT INTO jobs (reference, closing_date, interview_date, salary, title, topic, type, url)
VALUES ("$reference", "$closing_date", "$interview_date", "$salary", "$title", "$topic", "$type", "$url");
SQL;

	if(!$result = mysqli_query($con,$sql2)){
	    die('There was an error running the query [' . $con->error . ']');
	}	
}



# LIBRARY
$string = file_get_contents("./site/output/library.json");
// NB it assumes dos2unix has happened

$json_cat=json_decode($string,true);

# Delete
$sql1 = <<<SQL
DELETE FROM library WHERE 1;
SQL;

if(!$result = mysqli_query($con,$sql1)){
    die('There was an error running the query [' . $con->error . ']');
}

foreach ($json_cat as $element) {


    $library_id = $element["id"];
    $author = htmlentities($element["author"]);
    $date = $element["date"];
    $isbn = $element["isbn"];
    $oclc = $element["oclc"];
    $publisher = $element["publisher"];
    $subject = $element["subject"];
    $title = htmlentities($element["title"]);
    $title = str_replace("\\","",$title);
	
	$sql2 = <<<SQL
INSERT INTO library (library_id, author, date, isbn, oclc, publisher, subject, title)
VALUES ("$library_id", "$author", "$date", "$isbn", "$oclc", "$publisher", "$subject", "$title");
SQL;

	
	if(!$result = mysqli_query($con,$sql2)){
	    die('There was an error running the query [' . $con->error . ']');
	}	

	
}



# REPOSITORY
$string = file_get_contents("./site/output/publications.json");
// NB it assumes dos2unix has happened

$json_cat=json_decode($string,true);

# Delete
$sql1 = <<<SQL
DELETE FROM publications WHERE 1;
SQL;

if(!$result = mysqli_query($con,$sql1)){
    die('There was an error running the query [' . $con->error . ']');
}

foreach ($json_cat as $element) {


    $puburl = $element["url"];
    $authorslist = implode(",", $element["authors"]);
    $title = htmlentities($element["title"]);
    $doi = $element["doi"];
    $year = $element["year"];
    $repository = $element["repository"];
    $abstract = htmlentities($element["abstract"]);
    
	
	$sql2 = <<<SQL
INSERT INTO publications (puburl, authorslist, title, doi, year, repository, abstract)
VALUES ("$puburl", "$authorslist", "$title", "$doi", "$year", "$repository", "$abstract");
SQL;

	
	if(!$result = mysqli_query($con,$sql2)){
	    die('There was an error running the query [' . $con->error . ']');
	}	

	
}

?>