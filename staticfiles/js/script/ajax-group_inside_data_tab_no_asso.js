define(['jquery','bootstrap_popover', 'bootstrap' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS inside_data_tab.js OK");

        $('.dataTables_filter').append(" <a  href='#' title='Version établissement requise'   style='float:left' class='btn btn-success btn-xs'> Aide </a>  ");
        $('.dataTables_length').append("  <a href='#' title='Version établissement requise'   class='btn btn-default pull-right'>Exporter les compétences</a>  ") ;

    });
});