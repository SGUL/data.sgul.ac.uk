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
  <h2>Frequently Asked Questions</h2>
  <div class="accordion" id="accordion2">
  <div class="accordion-group">
    <div class="accordion-heading">
      <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseOne">
        What about Open Data?
      </a>
    </div>
    <div id="collapseOne" class="accordion-body collapse in">
      <div class="accordion-inner">
        <a href="http://en.wikipedia.org/wiki/Open_data">Open Data</a> is, according to Wikipedia, <i> is the idea that certain data should be freely available to everyone to use and republish as they wish, without restrictions from copyright, patents or other mechanisms of control</i>. In the last few years, this ideas has given origin to a big movement of people interested in getting access to data generated by a number of institutions, agencies, and entities, fostered by <a href="http://en.wikipedia.org/wiki/Freedom_of_information">Freedom of Information</a> legislation all over the world. Several national and local "Open Data portals" have been created, notably the United States' <a href="http://data.gov">data.gov</a>, the United Kingdom's <a href="http://data.gov.uk">data.gov.uk</a> and the Greater London Authority's <a href="http://data.london.gov.uk">data.london.gov.uk</a>.
      </div>
    </div>
  </div>
  <div class="accordion-group">
    <div class="accordion-heading">
      <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseTwo">
        Why Open Data in Academia?
      </a>
    </div>
    <div id="collapseTwo" class="accordion-body collapse">
      <div class="accordion-inner">
        A big drive in the creation of the Open Data movement has come from academic institutions, notably the <a href="http://data.southampton.ac.uk">University of Southampton</a>. It's time that other institutions join the Open Data movement as data producers, and share the overwhelming amount of data they hold - from administrative and statistical datasets, to research raw data and outcomes.
      </div>
    </div>
  </div>
  <div class="accordion-group">
    <div class="accordion-heading">
      <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseThree">
        What are the components of this Open Data project?
      </a>
    </div>
    <div id="collapseThree" class="accordion-body collapse">
      <div class="accordion-inner">
        There are several deliverables of this project:
        <ul>
            <li>the datasets and, possibly, an institutional ontology</li>
            <li>an API</li>
            <li>a SPARQL endpoint</li>
            <li>documentation, metadata, and legal information.</li>
        </ul>
      </div>
    </div>
  </div>
  <div class="accordion-group">
    <div class="accordion-heading">
      <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseFour">
        What is exactly an Academic API?
      </a>
    </div>
    <div id="collapseFour" class="accordion-body collapse">
      <div class="accordion-inner">
        An Academic API is, simply, an API returning a number of information about an academic institution. Developing an Academic API is the most speculative goal of this project. The idea behind an Academic API is that of seeking interoperability between the data services of different institution. We want to understand what are the most popular datasets, and how people link these datasets to generate derivative datasets. It makes sense, in this context, to provide the users with an easy to use, pre-developed API.
      </div>
    </div>
  </div>
  <div class="accordion-group">
    <div class="accordion-heading">
      <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseFive">
        What is a SPARQL Endpoint?
      </a>
    </div>
    <div id="collapseFive" class="accordion-body collapse">
      <div class="accordion-inner">
        SPARQL (SPARQL Protocol and RDF Query Language) is a query language for RDF, that is a language to retrieve and manipulate data from a specific type of "database" using the Resource Description Framework format, i.e. graph-related data. It is one of the most important technologies used for the so called semantic web.
      </div>
    </div>
  </div>
  <div class="accordion-group">
    <div class="accordion-heading">
      <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseSix">
        Who develops and maintains this website?
      </a>
    </div>
    <div id="collapseSix" class="accordion-body collapse">
      <div class="accordion-inner">
        The Open Data service is an experimental project developed by Giuseppe Sollazzo in Computing Services. It aims to investigate what are the sources of Open Data within SGUL and what processes should be put in place to ensure their accurate and accessible publication.
      </div>
    </div>
  </div>
  <div class="accordion-group">
    <div class="accordion-heading">
      <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseSeven">
        Is this portal an authoritative source of SGUL Data?
      </a>
    </div>
    <div id="collapseSeven" class="accordion-body collapse">
      <div class="accordion-inner">
        Although we download and elaborate data directly from the authoritative sources, the datasets available on this portal should always be considered non-authoritative sources, at least while the service stays in beta. <br/>
        That said, we aim at providing data with maximum accuracy and to mirror any update in the original sources.<br/>
        Please also note that there is a separate FOI (Freedom Of Information) structure which offers direct answers for
      </div>
    </div>
  </div>
  <div class="accordion-group">
    <div class="accordion-heading">
      <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseEight">
        How often is this portal updated?
      </a>
    </div>
    <div id="collapseEight" class="accordion-body collapse">
      <div class="accordion-inner">
        We aim to update the data at least once a week, or more often if possible. The last update is reported on each dataset's page.
      </div>
    </div>
  </div>
  <div class="accordion-group">
    <div class="accordion-heading">
      <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseTen">
        How can I learn more about the available datasets?
      </a>
    </div>
    <div id="collapseTen" class="accordion-body collapse">
      <div class="accordion-inner">
        If you click on the "Datasets" link in the upper navigation bar, or go directly into a dataset on the left, you will see all available Metadata for a given dataset, with details on how to access the actual data. <br/>
        We aim to provide:
        <ul>
            <li>Metadata (licence, update frequency, source of the data, external URL when available)</li>
            <li>Linked data info, including vocabularies, classes, and predicates used in the dataset</li>
            <li>Direct access links to the data, including dumps in several formats (JSON, CSV, RDF-XML, example SPARQL queries, and a list of the main API calls returning the chosen dataset).</li>
        </ul>
      </div>
    </div>
  </div>
  <div class="accordion-group">
    <div class="accordion-heading">
      <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseNine">
        I have a question, can I get in touch with you?
      </a>
    </div>
    <div id="collapseNine" class="accordion-body collapse">
      <div class="accordion-inner">
        Sure. Please go through the FAQs first, then you're welcome to get in touch with Giuseppe Sollazzo in Computing Services, who maintains these pages, at <a href="mailto:opendata@sgul.ac.uk">opendata@sgul.ac.uk</a>.
      </div>
    </div>
  </div>
</div>
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
