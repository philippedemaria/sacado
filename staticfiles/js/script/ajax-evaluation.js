define(['jquery','bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-evaluation.js OK");
 


       
        $('#id_is_favorite').prop('checked', true); 

        $('#id_zoom').prop('checked', false); 
        $('#id_is_share').prop('checked', false); 
        $('#id_is_publish').prop('checked', false); 
        $('#id_is_achievement').prop('checked', false); 
        $('#id_is_next').prop('checked', false); 
        $('#id_is_exit').prop('checked', false); 

        $('#id_is_exit_div').hide(); 
 
        $("#id_is_next").change(function () {
                        if ($("#id_is_next").is(":checked")) {
                           $("#id_is_exit_div").show(500);
                        } else {
                          $("#id_is_exit_div").hide(500);
                        }
                    })



    });
});