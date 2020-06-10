requirejs.config({
    baseUrl: "../../static/js", 
    waitSeconds: 90,
    paths: {
        jquery: ['//ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min', 'lib/jquery-2.2.4.min'],
        jquery19: ['//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min'],
 
        ui: "lib/jquery-ui.min",
 
        ui_sortable: "script/ui-sortable",
 
 
 
    },
    shim: {
        "bootstrap": {
            deps: ['jquery']
        }, 
 
        "bootstrap": {
            deps: ['jquery' ]
        },
 

 
    }
});

require(['jquery', 'bootstrap',  'ui', 'ui_sortable',   ]);

// suppression de admin dans le chargement  : 'admin', 
//  'admin',  'ckeditor', 'ckeditor_init', 'ckeditor_jquery', 'datatables', 'datatables_bootstrap',    'config_select2',   'config_toggle', 'config_colorpicker', 'fonctions_jquery', 'fonctions' ,      'multiselect', 'slimscroll',