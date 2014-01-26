require.config({
  baseUrl: '/static/js/',
  paths: {
    "jquery": "//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min, jquery.min",
    "bootstrap": "bootstrap.min",
    "datepicker": "bootstrap-datepicker",
    "timepicker": "bootstrap-timepicker.min",
    "footable": "footable",
    "alphanumeric": "jquery.alphanumeric",
    "datatables": "jquery.dataTables.min",
    "multiselect": "jquery.multi-select",
    "mousetrap": "mousetrap.min",
    "modernizr": "modernizr",
  },

  shim: {
    "bootstrap": ["jquery"],
    "datepicker": ["jquery"],
    "timepicker": ["jquery"],
    "footable": ["jquery"],
    "alphanumeric": ["jquery"],
    "datatables": ["jquery"],
    "multiselect": ["jquery"],
    "modernizr": {
      exports: 'Modernizr'
    },
  }
});

requirejs(['sacramentos']);