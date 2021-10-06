define(['jquery','bootstrap_popover', 'bootstrap' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS inside_data_tab.js OK");

        $('#DataTables_Table_0_wrapper').find('.col-sm-6').first().append("<h1 class='thin sacado_color_text'><i class='fa fa-folder-open'></i> Dossiers </h1> ") ;
        $('#DataTables_Table_1_wrapper').find('.col-sm-6').first().append("<h1 class='thin sacado_color_text'><i class='fa fa-trophy'></i> Evaluations </h1> ") ;
    });
});