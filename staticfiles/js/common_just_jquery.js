requirejs.config({
    baseUrl: "../../../../static/js", 
    waitSeconds: 90,
    paths: {
        jquery: ['//ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min', 'lib/jquery-2.2.4.min'],
        jquery19: ['//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min'],  

    },
    shim: {
        "bootstrap": {
            deps: ['jquery']
        }

    }
});

require(['jquery', 'bootstrap',  ]);

// suppression de admin dans le chargement  : 'admin', 
//  ,'slimscroll', 'chart'
