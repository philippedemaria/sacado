requirejs.config({
    baseUrl: "../../static/js", 
    waitSeconds: 90,
    paths: {
        jquery: ['//ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min', 'lib/jquery-2.2.4.min'],
        jquery19: ['//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min'],
        select2: "lib/select2.full.min",
        ui: "lib/jquery-ui.min",
        ui_draggable: "script/ui-draggable",
        ui_sortable: "script/ui-sortable",
        jquery_sortable: "lib/jquery-sortable",
 
 
        bootstrap: "lib/bootstrap.min",
        popoverx: "lib/bootstrap-popover-x.min",
        ckeditor: "../ckeditor/ckeditor/ckeditor",
        ckeditor_init: "../ckeditor/ckeditor-init",
        ckeditor_jquery: "../ckeditor/ckeditor/adapters/jquery",
        toggle: ["//gitcdn.github.io/bootstrap-toggle/2.2.2/js/bootstrap-toggle.min", "lib/bootstrap-toggle.min"],
        colorpicker: "lib/bootstrap-colorpicker.min",
        multiselect: "lib/multiselect.min",
        mathjax: ["https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_CHTML&amp;delayStartupUntil=configured"],
        fastclick: "lib/fastclick.min",
        slimscroll: "lib/jquery.slimscroll.min",
        datatables: "lib/jquery.dataTables.min",
        datatables_bootstrap: "lib/dataTables.bootstrap.min",
 
        admin: "lib/app.min",
        config_select2: "script/config-select2",
        config_datepicker: "script/config-datepicker",
        config_toggle: "script/config-toggle",
        config_datatable: "script/config-datatable", 
        config_colorpicker: "script/config-colorpicker", 
        popper: 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min',
        fonctions_jquery: "script/fonctions-jquery",
        fonctions: "script/fonctions",
    },
    shim: {
        "bootstrap": {
            deps: ['jquery']
        }, 
        "toggle": {
            deps: ['jquery']
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
 
 

        "mathjax": {
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

require(['jquery', 'bootstrap', 'mathjax',   'ckeditor', 'ckeditor_init', 'ckeditor_jquery', 'datatables', 'datatables_bootstrap',
    'config_select2',   'config_toggle', 'config_colorpicker', 'fonctions_jquery', 'fonctions' , 'ui', 'ui_sortable', 
    'multiselect', 'slimscroll',    ]);

// suppression de admin dans le chargement  : 'admin', 
 