requirejs.config({
    baseUrl: "/static/js", 
    waitSeconds: 90,
    paths: {
       
        bootstrap: "lib/bootstrap.min",
        bootstrap_popover: ["https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.6/umd/popper.min", 'lib/popper.min'], 
        jquery: ['//ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min', 'lib/jquery-2.2.4.min'],
        select2: "lib/select2.full.min",
        config_select2: "script/config-select2",
        multiselect: "lib/multiselect.min",
    },
    shim: {
       

 

    }
});

require(['jquery',  'multiselect',  'config_select2', 'bootstrap', 'bootstrap_popover',   ]);