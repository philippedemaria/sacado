define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 
 
    console.log(" ajax-quizz-complement chargé ");
 
  
        $(document).ready(function(){
            (function(){
                var i = 0;
                setInterval(function(){
                    $("body").removeClass("bg1, bg2, bg3, bg4, bg5, bg6, bg7, bg8").addClass("bg"+(i++%8 + 1));
                }, 4000);
            })();
        });


        $('#id_is_publish').prop('checked', true); 
        $('#id_is_numeric').prop('checked', false); 
        $('#id_is_video').prop('checked', false); 
        $('#id_is_archive').prop('checked', false); 
        $('#id_is_mark').prop('checked', false); 
        $('#id_is_random').prop('checked', false); 
        $('#id_is_ranking').prop('checked', false); 
        $('#id_is_shuffle').prop('checked', false); 
        $('#id_is_back').prop('checked', false);
        $('#id_is_result').prop('checked', false);


        $('.div_is_mark').hide() ; 
        $(".div_is_ranking").hide(); 
        $(".div_time").hide(); 
        $('.div_interslide').hide() ; 

        $('#id_is_numeric').on('change', function (event) {
            $('.div_is_mark').toggle(300) ; 
        });
        $('#id_is_video').on('change', function (event) {
            $('.div_is_ranking').toggle(300) ;
            $('.div_interslide').toggle(300) ; 
        });
        $('#id_is_publish').on('change', function (event) {
            $('.div_time').toggle(300) ; 
        });


 



        $('.generated_quizz').on('click', function (event) {

            let gq_id = $(this).data("gq_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'gq_id': gq_id,                     
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "../ajax_show_generated",
                    success: function (data) {

                        $("#body_gq").html("").html(data.html);
                    }
                }
            )
        });




    $("#loading").hide(500); 

  // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_levels').on('change', function (event) {
            let id_level = $(this).val();
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $("#loading").html("<i class='fa fa-spinner fa-pulse fa-fw'></i>");
            $("#loading").show(); 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'id_level': id_level,
                        'id_subject': id_subject,                        
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "../../qcm/ajax/chargethemes_parcours",
                    success: function (data) {

                        themes = data["themes"];
                        $('select[name=themes]').empty("");
                        if (themes.length >0)

                        { for (let i = 0; i < themes.length; i++) {
                                    

                                    console.log(themes[i]);
                                    let themes_id = themes[i][0];
                                    let themes_name =  themes[i][1]  ;
                                    let option = $("<option>", {
                                        'value': Number(themes_id),
                                        'html': themes_name
                                    });
                                    $('select[name=themes]').append(option);
                                }
                        }
                        else
                        {
                                    let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                    });
                            $('select[name=themes]').append(option);
                        }


 

                        $("#loading").hide(500); 
                    }
                }
            )
        });






        $('.show_my_quizz_result').on('click', function (event) {

            let gquizz = $(this).data("gquizz");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'gquizz': gquizz,                      
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "ajax_show_my_result",
                    success: function (data) {

                        $("#my_result").html(data.html); 
                    }
                }
            )
        });


        $('#display_init').on('click', function (event) {
            $('.no_display_init').toggle(300) ; 
        });
 

 
    });
});