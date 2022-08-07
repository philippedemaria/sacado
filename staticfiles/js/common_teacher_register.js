requirejs.config({
    baseUrl: "/static/js", 
    waitSeconds: 90,
    paths: {
       
 
        jquery: ['//ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min', 'lib/jquery-2.2.4.min'],
        config_select2: "script/config-select2",
        multiselect: "lib/multiselect.min",
    },
    shim: {
       

 

    }
});

require(['jquery',  'multiselect',  'config_select2',   ]);