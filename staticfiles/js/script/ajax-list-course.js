define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS list-course.js OK");

 
        // ====================================================================================================================
        // ====================================================================================================================
        // ============================================       Mes accordions       ============================================ 
        // ====================================================================================================================
        // ====================================================================================================================
            $('.collapsed').hide() ;
            collapser = 0 ;
            $('.accordion').on('click', function (event) {

                let target = $(this).attr("data-target");

                $(".subparcours"+target).toggle(500);

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
 

 
        // ==================================================================================================
        // ==================================================================================================
        // ============= Mutualisation de cours
        // ==================================================================================================
        // ==================================================================================================

 

              $('.course_sharer').on('click', function (event) {
                let course_id = $(this).attr("data-course_id");
                let statut = $(this).attr("data-statut");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'course_id': course_id,
                            'statut': statut,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: "ajax_sharer_course" ,
                        success: function (data) {
                            $('#course_sharer'+course_id).attr("data-statut",data.statut);                  
                            $('#course_sharer_statut'+course_id).removeClass(data.noclass);
                            $('#course_sharer_statut'+course_id).addClass(data.class);
                            $('#course_sharer_statut'+course_id).html("").html(data.label);
 
                        }
                    }
                )

                }); 
 
 
 
        // ==================================================================================================
        // ==================================================================================================
        // ============= Publication de cours
        // ==================================================================================================
        // ==================================================================================================

 
 
        $('body').on('click','.course_publisher', function (event) {
                let course_id = $(this).attr("data-course_id");
                let statut = $(this).attr("data-statut");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                url_from = "ajax_publish_course" ;

                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'course_id': course_id,
                            'statut': statut,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: url_from ,
                        success: function (data) {
                            $('#course_publisher'+course_id).attr("data-statut",data.statut);                  
                            $('#course_statut'+course_id).removeClass(data.noclass);
                            $('#course_statut'+course_id).addClass(data.class);
                            $('#course_statut'+course_id).html("").html(data.label);

  
                        }
                    }
                )

            }); 
 
 
    });

});

