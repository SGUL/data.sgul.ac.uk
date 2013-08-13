
<!DOCTYPE html>
<html>
<head>

    <!--link href='//fonts.googleapis.com/css?family=Droid+Sans:400,700' rel='stylesheet' type='text/css'/-->
    <link href='swagger-ui-dist/css/hightlight.default.css' media='screen' rel='stylesheet' type='text/css'/>
    <link href='swagger-ui-dist/css/screen.css' media='screen' rel='stylesheet' type='text/css'/>
    <script src='swagger-ui-dist/lib/jquery-1.8.0.min.js' type='text/javascript'></script>
    <script src='swagger-ui-dist/lib/jquery.slideto.min.js' type='text/javascript'></script>
    <script src='swagger-ui-dist/lib/jquery.wiggle.min.js' type='text/javascript'></script>
    <script src='swagger-ui-dist/lib/jquery.ba-bbq.min.js' type='text/javascript'></script>
    <script src='swagger-ui-dist/lib/handlebars-1.0.rc.1.js' type='text/javascript'></script>
    <script src='swagger-ui-dist/lib/underscore-min.js' type='text/javascript'></script>
    <script src='swagger-ui-dist/lib/backbone-min.js' type='text/javascript'></script>
    <script src='swagger-ui-dist/lib/swagger.js' type='text/javascript'></script>
    <script src='swagger-ui-dist/swagger-ui.js' type='text/javascript'></script>
    <script src='swagger-ui-dist/lib/highlight.7.3.pack.js' type='text/javascript'></script>

    <script type="text/javascript">
  $(function () {
      window.swaggerUi = new SwaggerUi({
                discoveryUrl:"http://data.sgul.ac.uk/api-docs.json",
                apiKey:"",
                dom_id:"swagger-ui-container",
                supportHeaderParams: false,
                supportedSubmitMethods: ['get', 'post', 'put'],
                onComplete: function(swaggerApi, swaggerUi){
                  if(console) {
                        console.log("Loaded SwaggerUI")
                        console.log(swaggerApi);
                        console.log(swaggerUi);
                    }
                  $('pre code').each(function(i, e) {hljs.highlightBlock(e)});
                },
                onFailure: function(data) {
                  if(console) {
                        console.log("Unable to Load SwaggerUI");
                        console.log(data);
                    }
                },
                docExpansion: "none"
            });

            window.swaggerUi.load();
        });

    </script>

</head>
</body>
<div id="message-bar" class="swagger-ui-wrap">
    &nbsp;
</div>

<div id="swagger-ui-container" class="swagger-ui-wrap">

</div>




</body>










