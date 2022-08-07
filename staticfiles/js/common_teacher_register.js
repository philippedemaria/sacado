requirejs.config({
    baseUrl: "/static/js", 
    waitSeconds: 90,
    paths: {
       
 
  

        jquery: "../index/lib/jquery/jquery.min",

 
    },
    shim: {
       




        "main": {
            deps: ['jquery']
        },

    }
});

require(['jquery',     ]);