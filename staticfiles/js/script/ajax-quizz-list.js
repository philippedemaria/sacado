define(['jquery',  'bootstrap', 'ui' , 'ui_sortable' , 'uploader','config_toggle'], function ($) {
    $(document).ready(function () {


    console.log(" ajax-quizz-list chargé ");


        // ====================================================================================================================
        // ====================================================================================================================
        // ============================================       Mes accordions       ============================================ 
        // ====================================================================================================================
        // ====================================================================================================================
 

 
            $('.collapsed').hide() ;
            collapser = 0 ;
            $('.accordion').on('click', function (event) {

                let target = $(this).attr("data-target");

                $(".subquizz"+target).toggle(500);

                if (collapser %2 == 0) 
                    { 
                        $("#pop"+target).removeClass('fa-chevron-down').addClass('fa-chevron-up');

                        $(".selected_tr").addClass('no_visu_on_load');
                        $("#tr"+target).removeClass('no_visu_on_load').addClass('bg_violet');
                    } 
                else 
                    {
                        $("#pop"+target).removeClass('fa-chevron-up').addClass('fa-chevron-down');

                        $(".selected_tr").removeClass('no_visu_on_load');
                        $("#tr"+target).removeClass('bg_violet');

                    }
                collapser++;                     
             }) ;






 

        $('#DataTables_Table_0_wrapper').find('.col-sm-6').first().append("<h2 class='thin sacado_color_text'><i class='fa fa-folder-open'></i>   dans des dossiers </h2> ") ;
        $('#DataTables_Table_1_wrapper').find('.col-sm-6').first().append("<h2 class='thin sacado_color_text'><i class='fa fa-th-list'></i>   hors dossier</h2> ") ;
 


 
    });
});