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
            <h2>SPARQL Endpoint</h2>
		<form action="sparql/sparql" method="get">
	        	<p>
	        	  <textarea name="query" cols="100" rows="20">
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?name ?weblog ?sha1
FROM <http://www.ldodds.com/ldodds-knows.rdf>
WHERE
{
	?x foaf:name ?name.
	?x foaf:weblog ?weblog.
	?x foaf:mbox_sha1sum ?sha1
}	
			  </textarea>
		          <br/>
		          Target graph URI (or use <code>FROM</code> in the query)
		          <input name="default-graph-uri" size="25" value="" />
		          <br/>

		      Output: <select name="output">
			        <option value="json">JSON</option>
			        <option value="xml">XML</option>
			        <option value="text">Text</option>
			        <option value="csv">CSV</option>
			        <option value="tsv">TSV</option>
			      </select>
		      <br/>
	              XSLT style sheet (blank for none):
		      <input name="stylesheet" size="20" value="/xml-to-html.xsl" />
		      <br/>
		      <input type="checkbox" name="force-accept" value="text/plain"/>
		      Force the accept header to <tt>text/plain</tt> regardless
	              <br/>
	              <input type="submit" value="Get Results" />
	        </p>
      	    </form>

          
        </div><!--/span-->
      </div><!--/row-->

      <hr>
	<?php include 'footer.php';?>

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
