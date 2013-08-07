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
          <div class="hero-unit">
            <h1>SGUL Open Data</h1>
            <p>St George's University of London's Administrative, Research, and Statistical Open Data.</p>
            <p>Welcome to SGUL's Open Data portal. We aim to collect the several sources of Open Data available within the institution, reprocess them and repackage them in machine-readable formats, and license them for reuse under licences such as the Open Government Licence.</p>
            <p>Where possible, we intend to provide the data as Linked Data, providing a SPARQL endpoint and an API, together with examples and documentation.</p>
            <p>This service is highly experimental, as we identify the data sources and work with them. Please get in touch if you have any query.</p>

          </div>
          <!--div class="row-fluid">
            <div class="span4">
              <h2>Vacancies</h2>
              <p><a href="http://jobs.sgul.ac.uk">Original</a> | <a href="output/jobs.csv">CSV</a> | <a href="output/jobs.json">JSON</a> | <a href="output/jobs.rdf">RDF-XML</a> | <a href="">SPARQL [Coming soon]</a></p>
              <p>License: <a href="http://www.nationalarchives.gov.uk/doc/open-government-licence/">OGL</a></p>
            </div>
            <div class="span4">
              <h2>Publications</h2>
              Expected release: August.
            </div>
            <div class="span4">
              <h2>XCRI Data</h2>
              Expected release: September.
            </div>
          </div--><!--/row-->

        </div><!--/span-->
      </div><!--/row-->
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
