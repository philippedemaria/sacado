define(['jquery','bootstrap_popover', 'bootstrap' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS inside_data_tab.js OK");

        $('.dataTables_filter').append(" <a  href='#' data-toggle='modal' data-target='#export_help'   style='float:left' class='btn btn-success btn-xs'> Aide </a>  ");
        $('.dataTables_length').append("  <a href='#' data-toggle='modal' data-target='#export_skills'  class='btn btn-default pull-right'><i class='bi bi-file-arrow-down'></i> Compétences vers Pronote</a>  ") ;

    });
});