requirejs.config({
    baseUrl: "../../../static/js", 
    waitSeconds: 90,
    paths: {
        jquery: ['//ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min', 'lib/jquery-2.2.4.min'],
 
        bootstrap: "lib/bootstrap.min",
 
        webSimple_zero: "ggb/webSimple_0",
        webSimple_douze: "ggb/webSimple_12",
        webSimple_quatre: "ggb/webSimple_4",
        webSimple_cinq: "ggb/webSimple_5",
        webSimple_six: "ggb/webSimple_6",
        webSimple_sept: "ggb/webSimple_7",
        webSimple_neuf: "ggb/webSimple_9", 
        webSimpleNoCache: "ggb/webSimple.nocache", 


    },
    shim: {


            "webSimple_douze": {
                deps: ['webSimple_zero']
            },
            "webSimple_quatre": {
                deps: ['webSimple_douze']
            },
            "webSimple_cinq": {
                deps: ['webSimple_quatre']
            },
            "webSimple_six": {
                deps: ['webSimple_cinq']
            },
            "webSimple_sept": {
                deps: [ 'webSimple_six']
            },
            "webSimple_neuf": {
                deps: ['webSimple_sept']
            },
            "webSimpleNoCache": {
                deps: ['webSimple_neuf']
            },
 
        }
});

require(['jquery', 'webSimple_zero', 'webSimple_douze','webSimple_quatre','webSimple_cinq','webSimple_six','webSimple_sept','webSimple_neuf','webSimpleNoCache' ]);