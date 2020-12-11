define(['jquery','bootstrap_popover', 'bootstrap' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS inside_data_tab.js OK");




        $('.dataTables_filter').append(" <a  href='#' data-toggle='modal' data-target='#export_help'   style='float:left' class='btn btn-success btn-xs'> Aide </a>  ");


        $('.dataTables_length').append("  <a href='#'  title='Version établissement requise'   class='btn btn-default pull-right'><i class='fa fa-print'></i></a>  ") ;        

        $('.dataTables_length').append("  <a href='#'  title='Version établissement requise' class='btn btn-default pull-right'>Exporter les notes vers Pronote</a>  ") ;

        $('.dataTables_length').append("  <a href='#'  title='Version établissement requise'   class='btn btn-default pull-right'>Exporter les compétences vers Pronote</a>  ") ;




        $('#mini_loader').hide() ;
		$('body').on('click' , "#mini_loader_shower", function () {
				$('#mini_loader').show(300) ;

				setTimeout(function() {
					    $('#mini_loader').hide(300) ;
					}, 20000);
	         })
 

        $('.mark_div_in_score').hide() ;
		$('body').on('change' , "#mark_shower", function () {

	        if ( $("#mark_shower").is(":checked") )
	            {   
					$('.mark_div_in_score').show() ;
	            }
	        else 
	            {   
					$('.mark_div_in_score').hide() ;
	            }
	         })

    });
});