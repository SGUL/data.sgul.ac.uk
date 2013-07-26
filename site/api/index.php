<?php

require("Toro.php");

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



Toro::serve(array(
    "/" => "HelloHandler",
    "/abc" => "HelloHandler",
    "/publications/list/:string" => "PubListHandler",
    "/publications/get/:number" => "PubGetHandler",
    "/publications/search/:alpha" => "PubSearchHandler",
    "/jobs/list/:string" => "JobListHandler",
    "/jobs/get/:alpha" => "JobGetHandler",
    "/jobs/search/:alpha" => "JobSearchHandler",
));
