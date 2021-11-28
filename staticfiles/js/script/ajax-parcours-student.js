define(['jquery','bootstrap'], function ($) {
    $(document).ready(function () {

        console.log("chargement JS ajax-parcours-student.js OK");
 

 
        // $('body').on('click' , '.selector_e', function () {

        //     let parcours_id = $(this).attr("data-parcours_id"); 
        //     let exercise_id = $(this).attr("data-exercise_id"); 
        //     let statut = $(this).attr("data-statut"); 

        //     let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

        //     $.ajax(
        //         {
        //             type: "POST",
        //             dataType: "json",
        //             data: {
        //                 'parcours_id': parcours_id,
        //                 'exercise_id': exercise_id,
        //                 'statut': statut,
        //                 csrfmiddlewaretoken: csrf_token
        //             },
        //             url: "../../ajax_populate",
        //             success: function (data) {
        //                 $('#is_selected'+exercise_id).html(data.html);   
        //                 $('#selector_e'+exercise_id).attr("data-statut",data.statut);                  
        //                 $('#selector_e'+exercise_id).removeClass(data.noclass);
        //                 $('#selector_e'+exercise_id).addClass(data.class);
        //                 $('#nb_exercises').html("").html(data.nb+" exercice.s");     
        //             }
        //         }
        //     )
        // });

        

        $('body').on('click' , '.show_parcours_tag_student_submenu' , function () { 
                $(this).hide(500);
                let parcours_tag_student = $(this).parent();
                parcours_tag_student.find('.parcours_tag_student_fermeture').show(500);
                parcours_tag_student.find('.parcours_tag_student_submenu').show(500);
                parcours_tag_student.animate({top: '2px',height:'296px'});
                parcours_tag_student.addClass('parcours_tag_student_background');

        });



        

        $('body').on('click' , '.parcours_tag_student_fermeture' , function () { 
                $(this).hide(500);
                let parcours_tag_student = $(this).parent();
                parcours_tag_student.find('.show_parcours_tag_student_submenu').show(500);
                parcours_tag_student.find('.parcours_tag_student_fermeture').hide(500);
                parcours_tag_student.find('.parcours_tag_student_submenu').hide(500);
                parcours_tag_student.animate({top: '160px' });
                parcours_tag_student.removeClass('parcours_tag_student_background');

        });
 



    });
});