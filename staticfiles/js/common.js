requirejs.config({
    baseUrl: "/static/js", 
    waitSeconds: 90,
    paths: {
       
 
  

        jquery: "../index/lib/jquery/jquery.min",
        jquerymigrate:"../index/lib/jquery/jquery-migrate.min",
        bootstrapbundle:"../index/lib/bootstrap/js/bootstrap.bundle.min",
        easing:"../index/lib/easing/easing.min",
        mobile:"../index/lib/mobile-nav/mobile-nav",

        waypoints:"../index/lib/waypoints/waypoints.min",
        counterup:"../index/lib/counterup/counterup.min",

        lightbox:"../index/lib/lightbox/js/lightbox.min",
        contactform:"../index/contactform/contactform",
        main:"../index/js/main",
 
    },
    shim: {
       
        "jquerymigrate": {
            deps: ['jquery']
        },
        "bootstrapbundle": {
            deps: ['jquery']
        },
        "easing": {
            deps: ['jquery']
        },
        "mobile": {
            deps: ['jquery']
        },
        "waypoints": {
            deps: ['jquery']
        },
        "counterup": {
            deps: ['jquery']
        },





        "main": {
            deps: ['jquery']
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

require(['jquery',  'jquerymigrate',  'mathjax',   'bootstrapbundle',  'easing', 'mobile', 'waypoints','counterup',      'contactform', 'main',     ]);