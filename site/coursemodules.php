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
<?php include_once("analyticstracking.php"); ?>
	<?php include 'navbar.php';?>
  <div class="container-fluid"> 
 <div class="row-fluid">
	<?php include 'menu.php';?>

	
<div class="span9">
    <h2>Course Modules</h2>
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
        <td>Yearly</td>
    </tr>
    <tr>
        <th>Last update</th>
        <td>Wed Apr 04 16:49:00 BST 2014</td>
    </tr>
    <tr>
        <th>Source</th>
        <td>FOI (Registry), Reference FOI2013-2014 106 </td>
    </tr>
    <tr>
        <th>External URL</th>
        <td>none</td>
    </tr>
    <tr >
        <th colspan="2">Linked Data Info</th>
    </tr>
    <tr>
        <th>Vocabularies</th>
        <td>
            <ul>
                <li><a href="http://www.w3.org/TR/rdf-schema/">RDF-Schema</a></li>
            </ul>
        </td>
    </tr>
    <tr>
        <th>Classes</th>
        <td>
            <ul>
                <li><a href="">rdf:Description</a></li>
            </ul>
        </td>
    </tr>
    <tr>
        <th>Predicates</th>
        <td>
            <ul>
                <li><a href="">rdf:type</a></li>
                <li><a href="">rdfs:label</a></li>
            </ul>
        </td>
    </tr>
    <tr >
        <th colspan="2">Data access</th>
    </tr>
    <tr>
        <th>JSON</th>
        <td><a href="output/coursemodules.json">coursemodules.json</a></td>
    </tr>
    <tr>
        <th>CSV</th>
        <td><a href="output/coursemodules.csv">coursemodules.csv</a></td>
    </tr>
    <tr>
        <th>RDF-XML dump</th>
        <td><a href="output/coursemodulesrdf.tar">coursemodulesrdf.tar</a></td>
    </tr>
    <tr>
        <th>SPARQL examples</th>
        <td>
            <b>Get up to 20 modules</b>
            <form method="post" action="http://data.sgul.ac.uk/sparql/">
         
<input type="hidden" name="query" id="query" value="


        PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt;
        PREFIX rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt;


            SELECT ?s ?title ?type WHERE {
            ?s rdfs:label ?title .
            ?s rdf:type ?type .
            FILTER (?type != &quot;http://www.w3.org/ns/dcat#Distribution&quot;)
            FILTER (?type != &quot;http://purl.org/ontology/bibo/AcademicArticle&quot;)
            FILTER (?type != &quot;http://purl.org/ontology/bibo/Document&quot;)
            FILTER (?type != &quot;http://www.w3.org/2002/07/owl#Thing&quot;)
            FILTER (?type != &quot;http://purl.org/ontology/bibo/Article&quot;)
            FILTER (?type != &quot;http://purl.org/openorg/vacancy/Vacancy&quot;)
        
                                }
"

</input>
<pre>
        PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt;
        PREFIX rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt;


            SELECT ?s ?title ?type WHERE {
            ?s rdfs:label ?title .
            ?s rdf:type ?type .
            FILTER (?type != &quot;http://www.w3.org/ns/dcat#Distribution&quot;)
            FILTER (?type != &quot;http://purl.org/ontology/bibo/AcademicArticle&quot;)
            FILTER (?type != &quot;http://purl.org/ontology/bibo/Document&quot;)
            FILTER (?type != &quot;http://www.w3.org/2002/07/owl#Thing&quot;)
            FILTER (?type != &quot;http://purl.org/ontology/bibo/Article&quot;)
            FILTER (?type != &quot;http://purl.org/openorg/vacancy/Vacancy&quot;)
        
                                }
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
            none
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
