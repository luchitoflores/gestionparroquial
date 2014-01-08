require(["jquery", "bootstrap", "bootstrap-datepicker"], function($) {
    //the jquery.alpha.js and jquery.beta.js plugins have been loaded.
    $(function() {
        $('body').alpha().beta();
    });
});


requirejs.config({
    baseUrl: 'static/js/',
    paths: {
        "jquery": "jquery.min",
        "bootstrap": "bootstrap.min",
        "bootstrap-datepicker" : "bootstrap-datepicker",
        "bootstrap-timepicker" : "bootstrap-timepicker.min",
        "footable" : "footable",
        "jquery.alphanumeric" : "jquery.alphanumeric",
        "jquery.dataTables" : "jquery.dataTables.min",
        "jquery.multi-select" : "jquery.multi-select",
        "modernizr" : "modernizr",
        "prefixfree" : "prefixfree.min",
        "sacramentos" : "sacramentos",
        "tablas" : "tablas",
    },

    shim: {
       "bootstrap": ["jquery"],
       "bootstrap-datepicker" : ["jquery"],
       "bootstrap-timepicker" : ["jquery"],
       "footable" : ["jquery"],
       "jquery.alphanumeric" : ["jquery"],
       "jquery.dataTables" : ["jquery"],
       "jquery.multi-select" : ["jquery"],
       "modernizr" : ["jquery"],
       "prefixfree" : ["jquery"],
       "sacramentos" : ["jquery"],
       "tablas" : ["jquery"],
   }
});


requirejs(["static/js/main"]);