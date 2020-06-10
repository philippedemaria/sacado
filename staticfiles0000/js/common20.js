requirejs.config({
    baseUrl: "../../static/js", 
    waitSeconds: 90,
    paths: {
        jquery: ['//ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min', 'lib/jquery-2.2.4.min'],
        jquery19: ['//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min'],  
        select2: "lib/select2.full.min",
        bootstrap: "lib/bootstrap.min",
        toggle: ["lib/bootstrap-toggle.min"],
        multiselect: "lib/multiselect.min",
        mathjax: ["https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_CHTML&amp;delayStartupUntil=configured"],
        datatables: "lib/jquery.dataTables.min",
        datatables_bootstrap: "lib/dataTables.bootstrap.min",
        config_select2: "script/config-select2",
        config_datepicker: "script/config-datepicker",
        config_toggle: "script/config-toggle",
        config_datatable: "script/config-datatable", 
        colorpicker: "lib/bootstrap-colorpicker.min",
        config_colorpicker: "script/config-colorpicker",       
        fonctions_jquery: "script/fonctions-jquery",
        fonctions: "script/fonctions",
        bootstrapjs: "bootstrap",
        ui: "lib/jquery-ui.min",
        ui_draggable: "script/ui-draggable",
        ui_sortable: "script/ui-sortable",
    },
    shim: {
        "bootstrap": {
            deps: ['jquery']
        },
        "toggle": {
            deps: ['jquery',   'bootstrap']
        },
        "datepicker": {
            deps: [ 'jquery', 'bootstrap']
        },
        "multiselect": {
            deps: ['jquery', 'ui']
        },
        "slimscroll": {
            deps: ['jquery']
        },
        "ckeditor_jquery": {
            deps: ['jquery', 'ckeditor']
        },
        "admin": {
            deps: ['jquery']
        },
        "bootstrapjs": {
            deps: ['jquery']
        },

        mathjax: {
            exports: "MathJax",
            init: function () {
                MathJax.Hub.Config({
                    extensions: ["tex2jax.js"],
                    jax: ["input/TeX", "output/HTML-CSS"],
                    tex2jax: {
                        inlineMath: [['$', '$'], ["\\(", "\\)"]],
                        displayMath: [['$$', '$$'], ["\\[", "\\]"]],
                        processEscapes: true
                    },
                    "HTML-CSS": {availableFonts: ["TeX"], scale: 90}
                });
                MathJax.Hub.Startup.onload();
                return MathJax;
            }
        }
    }
});

require(['jquery', 'bootstrap', 'mathjax', 'bootstrapjs', 'datatables', 'datatables_bootstrap','config_colorpicker', 'ui_sortable', 'config_select2',  
      'config_datepicker',  'config_toggle', 'fonctions_jquery', 'fonctions','ui',   'config_datatable']);

// suppression de admin dans le chargement  : 'admin', 