<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>SGUL Open Data Repository (beta)</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="assets/css/bootstrap.css" rel="stylesheet">
    <style type="text/css">
      body {
        padding-top: 60px;
        padding-bottom: 40px;
      }
      .sidebar-nav {
        padding: 9px 0;
      }
    </style>
    <link href="assets/css/bootstrap-responsive.css" rel="stylesheet">

    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <!-- Le fav and touch icons -->
    <link rel="shortcut icon" href="assets/ico/favicon.ico">
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="assets/ico/apple-touch-icon-114-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="assets/ico/apple-touch-icon-72-precomposed.png">
    <link rel="apple-touch-icon-precomposed" href="assets/ico/apple-touch-icon-57-precomposed.png">
  </head>

  <body>

	<?php include 'navbar.php';?>
  <div class="container-fluid"> 
 <div class="row-fluid">
	<?php include 'menu.php';?>

	
<div class="span9">
    <h2>Job Vacancies</h2>
  <table class="table">
    <tr >
        <th colspan="2">Metadata</th>
    </tr>
    <tr>
        <th>Licence</th>
        <td>OGL</td>
    </tr>
    <tr>
        <th>Update frequency</th>
        <td>Weekly</td>
    </tr>
    <tr>
        <th>Last update</th>
        <td>08 Aug 2013</td>
    </tr>
    <tr>
        <th>Source</th>
        <td>Human Resources</td>
    </tr>
    <tr>
        <th>External URL</th>
        <td><a href="http://jobs.sgul.ac.uk">jobs.sgul.ac.uk</a></td>
    </tr>
    <tr >
        <th colspan="2">Linked Data Info</th>
    </tr>
    <tr>
        <th>Vocabularies</th>
        <td>
            <ul>
                <li><a href="http://xmlns.com/foaf/0.1/">Friend of a Friend (FOAF)</a></li>
                <li><a href="http://www.w3.org/TR/rdf-schema/">RDF-Schema</a></li>
                <li><a href="http://dublincore.org/documents/2012/06/14/dcmi-terms/?v=elements#">Dublin Core Metadata Terms 1.1</a></li>
                <li><a href="http://purl.org/openorg/vacancy/">PURL Neologism Vacancy Terms</a></li>
                <li><a href="http://www.w3.org/1999/02/22-rdf-syntax-ns#">RDF Vocabulary</a></li>
            </ul>
        </td>
    </tr>
    <tr>
        <th>Classes</th>
        <td>
            <ul>
                <li><a href="">foaf:Document</a></li>
                <li><a href="">vacancy:Vacancy</a></li>
            </ul>
        </td>
    </tr>
    <tr>
        <th>Predicates</th>
        <td>
            <ul>
                <li><a href="">foaf:primaryTopic</a></li>
                <li><a href="">vacancy:employer</a></li>
                <li><a href="">vacancy:organizationalUnit</a></li>
                <li><a href="">vacancy:availableOnline</a></li>
                <li><a href="">vacancy:applicationInterviewNotificationByDate</a></li>
                <li><a href="">vacancy:applicationClosingDate</a></li>
                <li><a href="">vacancy:salary</a></li>
            </ul>
        </td>
    </tr>
    <tr >
        <th colspan="2">Data access</th>
    </tr>
    <tr>
        <th>JSON</th>
        <td><a href="output/jobs.json">jobs.json</a></td>
    </tr>
    <tr>
        <th>CSV</th>
        <td><a href="output/jobs.csv">jobs.csv</a></td>
    </tr>
    <tr>
        <th>RDF-XML dump</th>
        <td><a href="output/jobsrdf.tar">jobsrdf.tar</a></td>
    </tr>
    <tr>
        <th>SPARQL examples</th>
        <td>
            <b>Get job title, employer, organisational unit, salary, url, date interview, and date of application closing</b>
            <form method="post" action="http://data.sgul.ac.uk/sparql/">
         
<input type="hidden" name="query" id="query" value="
PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt;
PREFIX vacancy: &lt;http://purl.org/openorg/vacancy/&gt;
                

SELECT ?title ?employer ?ou ?salary ?url ?dateInterviewBy ?dateClosing WHERE {
    ?s rdfs:label ?title.
    ?s vacancy:employer ?employer.
    ?s vacancy:salary ?salary.
    ?s vacancy:availableOnline ?url.
    ?s vacancy:organizationalUnit ?ou.
    ?s vacancy:applicationInterviewNotificationByDate ?dateInterviewBy.
    ?s vacancy:applicationClosingDate ?dateClosing.
} LIMIT 20"
</input>
<pre>
PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt;
PREFIX vacancy: &lt;http://purl.org/openorg/vacancy/&gt;
                

SELECT ?title ?employer ?ou ?salary ?url ?dateInterviewBy ?dateClosing WHERE {
    ?s rdfs:label ?title.
    ?s vacancy:employer ?employer.
    ?s vacancy:salary ?salary.
    ?s vacancy:availableOnline ?url.
    ?s vacancy:organizationalUnit ?ou.
    ?s vacancy:applicationInterviewNotificationByDate ?dateInterviewBy.
    ?s vacancy:applicationClosingDate ?dateClosing.
} LIMIT 20
</pre>
<br/>
            
            <em>Soft limit</em> <input type="text" name="soft-limit">
<select name="output">
<option>xml</option>
<option>json</option>
<option>text</option>
</select>

            <input type="submit" value="Try"/>
            </form>
        </td>
    </tr>
    <tr>
        <th>API endpoints</th>
        <td>
            <a href="api.php#jobs">/api/jobs/list/</a><br/>
            <a href="api.php#jobs">/api/jobs/get/</a><br/>
            <a href="api.php#jobs">/api/jobs/search/</a><br/>
        </td>
    </tr>
  </table>
</div>
</div>
      <hr>
    <?php
    include 'footer.php';
    ?>

    </div><!--/.fluid-container-->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="assets/js/jquery.js"></script>
    <script src="assets/js/bootstrap-transition.js"></script>
    <script src="assets/js/bootstrap-alert.js"></script>
    <script src="assets/js/bootstrap-modal.js"></script>
    <script src="assets/js/bootstrap-dropdown.js"></script>
    <script src="assets/js/bootstrap-scrollspy.js"></script>
    <script src="assets/js/bootstrap-tab.js"></script>
    <script src="assets/js/bootstrap-tooltip.js"></script>
    <script src="assets/js/bootstrap-popover.js"></script>
    <script src="assets/js/bootstrap-button.js"></script>
    <script src="assets/js/bootstrap-collapse.js"></script>
    <script src="assets/js/bootstrap-carousel.js"></script>
    <script src="assets/js/bootstrap-typeahead.js"></script>

  </body>
</html>
