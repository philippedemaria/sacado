define(['jquery',  'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS update_customexercises.js OK");

        //*************************************************************************************************************  
        // Gestion des items
        //************************************************************************************************************* 

        // $(document).on('click', '.add_more', function (event) {


        //         var total_form = $('#id_customchoices-TOTAL_FORMS') ;
        //         var totalForms = parseInt(total_form.val())  ;

        //         $("#nb_pseudo_aleatoire").html("").html(totalForms+1);

        //         var thisClone = $('#rowToClone');
        //         rowToClone = thisClone.html() ;

        //         $('#formsetZone').append(rowToClone);
        //         $('#duplicate').attr("id","duplicate"+totalForms) ;

        //         $("#duplicate"+totalForms+" input").each(function(index){ 
        //             $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
        //             $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
        //         });

        //         $('#duplicate'+totalForms).find("input[type='checkbox']").bootstrapToggle();
 
        //         $("#duplicate"+totalForms+" textarea").each(function(){ 
        //             $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
        //             $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
        //         });

        //         total_form.val(totalForms+1);
        //     });



 


        // $(document).on('click', '.remove_more', function () {
        //     var total_form = $('#id_customchoices-TOTAL_FORMS') ;
        //     var totalForms = parseInt(total_form.val())-1  ;

        //     $('#duplicate'+totalForms).remove();
        //     total_form.val(totalForms);
        //     $("#nb_pseudo_aleatoire").html("").html(totalForms);
        // });

	 
 
	    $('#on_mark').hide(); 
	    $("#publication_div").hide(); 
	    // Gère l'affichage de la div des notes.
	    if ($("#id_is_mark").is(":checked")) {$("#on_mark").show();} else { $("#on_mark").hide(); } 

	    clickDivAppear( "#show_latex_formula" , $("#latex_formula"));
	 

	    function clickDivAppear(toggle, $item) {
	        $(document).on('click', toggle , function () {
	                    $(".no_display").hide();        
	                    $item.toggle(500);
	            });
	        }

	    $(document).on('click', "#support_audio_image" , function () {
	                    $(".no_display").hide();
	                    $("#drop_zone_image").toggle(500);
	                    $("#audio_div").toggle(500);            
	                });


	    makeDivDisappear( "#id_is_publish" , $("#publication_div"));
	    makeDivAppear( "#id_is_mark" , $("#on_mark"));
	    function makeDivAppear(toggle, $item) {
	        $(document).on('change', toggle , function () {
	                if ($(toggle).is(":checked")) {
	                    $item.show(500);
	                } else {
	                    $item.hide(500);
	                }
	            });
	        }
	    function makeDivDisappear(toggle, $item) {
	        $(document).on('change', toggle , function () {
	                if ($(toggle).is(":checked")) {
	                    $item.hide(500);
	                } else {
	                    $item.show(500);
	                }
	            });
	        }
 
    });
});