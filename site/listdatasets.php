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
  <h2>Datasets</h2>
  <table class="table">
    <tr>
        <th>Name</th>
        <th>Description</th>
        <th>Source</th>
        <th>Licence</th>
        <th>Open Data</th>
    </tr>
    <tr>
        <td><a href="#">Data catalogue</a></td>
        <td>The data catalogue in a linked-data machine-readable format.</td>
        <td>Computing Services</td>
        <td><a href="http://www.nationalarchives.gov.uk/doc/open-government-licence/version/1/open-government-licence.htm">Open Government Licence</a></td>
        <td><img src="./images/data-badge-5.png"/></td>
    </tr>
    <tr>
        <td><a href="vacancies.php">Job vacancies</a></td>
        <td>Job vacancies advertised within SGUL, as presented on <a href="http://jobs.sgul.ac.uk">jobs.sgul.ac.uk</a></td>
        <td>Human Resources</td>
        <td><a href="http://www.nationalarchives.gov.uk/doc/open-government-licence/version/1/open-government-licence.htm">Open Government Licence</a></td>
        <td><img src="./images/data-badge-4.png"/></td>
    </tr>
    <tr>
        <td><a href="publications.php">Publications</a></td>
        <td>Academic publications from SGUL's institutional repository <a href="http://openaccess.sgul.ac.uk">SORA</a></td>
        <td>Library</td>
        <td><a href="http://www.nationalarchives.gov.uk/doc/open-government-licence/version/1/open-government-licence.htm">Open Government Licence</a></td>
        <td><img src="./images/data-badge-5.png"/></td>
    </tr>
    <tr>
        <td><a href="#">XCRI</a> (available in winter 2013)</td>
        <td><a href="http://www.xcri.co.uk/">XCRI</a> (eXchanging Course Related Information) information - XCRI Course Advertising Profile (<a href="http://www.xcri.co.uk/what-is-xcri-cap.html">XCRI-CAP</a>); it's made of information about courses in away that allow comparisons among UK education institutions and aggregators such as UCAS and other sites that advertise courses.</td>
        <td>Registry</td>
        <td><a href="http://www.nationalarchives.gov.uk/doc/open-government-licence/version/1/open-government-licence.htm">Open Government Licence</a></td>
        <td><img src="./images/data-badge-5.png"/></td>
    </tr>
    <tr>
        <td><a href="#">Library catalogue</a> (available in winter 2013)</td>
        <td>A list of the books available in the institutional Library</td>
        <td>Library</td>
        <td><a href="http://www.nationalarchives.gov.uk/doc/open-government-licence/version/1/open-government-licence.htm">Open Government Licence</a></td>
        <td><img src="./images/data-badge-3.png"/></td>
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
