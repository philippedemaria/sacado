requirejs.config({
    baseUrl: "../static/js", 
    waitSeconds: 90,
    paths: {
        jquery: ['//ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min', 'lib/jquery-2.2.4.min'],
        jquery19: ['//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min'],
 
 
        webSimple0: "ggb/webSimple-0",
        webSimple12: "ggb/webSimple-12",
        webSimple4: "ggb/webSimple-4",
        webSimple5: "ggb/webSimple-5",
        webSimple6: "ggb/webSimple-6",
        webSimple7: "ggb/webSimple-7",
        webSimple9: "ggb/webSimple-9", 
        webSimpleNoCache: "ggb/webSimple.nocache", 
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
 
 

        }
    }
);

require(['jquery', 'bootstrap',   'webSimple0', 'webSimple12','webSimple4','webSimple5','webSimple6','webSimple7','webSimple9','webSimpleNoCache' ]);