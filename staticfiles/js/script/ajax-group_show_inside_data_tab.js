define(['jquery','bootstrap_popover', 'bootstrap' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS inside_data_tab.js OK");

        $('.dataTables_length').append(" <span style='font-size:12px' class='text-danger'><i class='fa fa-warning'></i> Les champs modifiés sont directement enregistrés. </font> ") ;


    });
});