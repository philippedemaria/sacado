define(['jquery','bootstrap_popover', 'bootstrap' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS inside_data_tab.js OK");

        $('.dataTables_wrapper').last().find('.col-sm-6').first().append("<h2 class='thin sacado_color_text'><i class='fa fa-th'></i> hors dossier </h2> ") ;
    });
});