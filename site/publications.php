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
    <h2>Publications</h2>
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
        <td><?php $file = file_get_contents('./.datefile.txt', true); echo $file;?></td>
    </tr>
    <tr>
        <th>Source</th>
        <td>Library</td>
    </tr>
    <tr>
        <th>External URL</th>
        <td><a href="http://openaccess.sgul.ac.uk">openaccess.sgul.ac.uk</a></td>
    </tr>
    <tr >
        <th colspan="2">Linked Data Info</th>
    </tr>
    <tr>
        <th>Vocabularies</th>
        <td>
            <ul>
                
                <li><a href="http://www.w3.org/TR/rdf-schema/">RDF-Schema</a></li>
                <li><a href="http://dublincore.org/documents/2012/06/14/dcmi-terms/?v=elements#">Dublin Core Metadata Terms 1.1</a></li>
                <li><a href="http://www.w3.org/1999/02/22-rdf-syntax-ns#">RDF Vocabulary</a></li>
                <li><a href="http://data.sgul.ac.uk/ontology/lib/">SGUL Ontology</a></li>
                <li><a href="http://purl.org/ontology/bibo/">BIBO Bibliographic Ontology</a></li>
                <li><a href="http://vivoweb.org/ontology/core#">VIVO Core Ontology</a></li>
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
                <li><a href="">bibo:abstract</a></li>
                <li><a href="">bibo:doi</a></li>
                <li><a href="">dc:author</a></li>
                <li><a href="">bibo:dateTime</a></li>
                <li><a href="">sgul:repositoryLink</a></li>
            </ul>
        </td>
    </tr>
    <tr >
        <th colspan="2">Data access</th>
    </tr>
    <tr>
        <th>JSON</th>
        <td><a href="output/publications.json">publications.json</a></td>
    </tr>
    <tr>
        <th>CSV</th>
        <td><a href="output/publications.csv">publications.csv</a></td>
    </tr>
    <tr>
        <th>RDF-XML dump</th>
        <td><a href="output/publicationsrdf.tar">publicationsrdf.tar</a></td>
    </tr>
    <tr>
        <th>SPARQL examples</th>
        <td>
            <b>Get id, title, authors, link to open access repository and DOI of up to 20 publications</b>
            <form method="post" action="http://data.sgul.ac.uk/sparql/">
         
<input type="hidden" name="query" id="query" value="
PREFIX bibo: &lt;http://purl.org/ontology/bibo/&gt;
                PREFIX sgul: &lt;http://data.sgul.ac.uk/ontology/lib/&gt;
                PREFIX vivo: &lt;http://vivoweb.org/ontology/core#&gt;
                PREFIX rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt;
                PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt;


                SELECT ?s ?title ?repositoryLink ?doi  WHERE {
                    ?s sgul:repositoryLink ?repositoryLink.
                    ?s rdfs:label ?title.
                    ?s bibo:doi ?doi.
                } LIMIT 20"
</input>
<pre>
PREFIX bibo: &lt;http://purl.org/ontology/bibo/&gt;
PREFIX sgul: &lt;http://data.sgul.ac.uk/ontology/lib/&gt;
PREFIX vivo: &lt;http://vivoweb.org/ontology/core#&gt;
PREFIX rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt;
PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt;

SELECT ?s ?title ?repositoryLink ?doi  WHERE {
    ?s sgul:repositoryLink ?repositoryLink.
    ?s rdfs:label ?title.
    ?s bibo:doi ?doi.
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
            <a href="api.php#pubs">/api/publications/list/</a><br/>
            <a href="api.php#pubs">/api/publications/get/</a><br/>
            <a href="api.php#pubs">/api/publications/search/</a><br/>
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
