define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-flashpack.js OK");

  


        $('#id_level').on('change', function (event) {
            let id_level = $(this).val();
    
            if ((id_level == "")||(id_level == " ")) { alert("Sélectionner un niveau") ; return false ;}
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            url_ = "ajax_chargethemes" ;

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
                    url : url_,
                    success: function (data) {

                        themes = data["themes"] ; 
                        $('select[name=theme]').empty("");

                        if (themes.length >0)
                        { for (let i = 0; i < themes.length; i++) {
                                    

                                    console.log(themes[i]);
                                    let themes_id = themes[i][0];
                                    let themes_name =  themes[i][1]  ;
                                    let option = $("<option>", {
                                        'value': Number(themes_id),
                                        'html': themes_name
                                    });
                                    $('select[name=theme]').append(option);
                                }
                        }
                        else
                        {
                                    let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                    });
                            $('select[name=theme]').append(option);
                        }


                    }
                }
            )
        });
 


        $('#id_theme').on('change', function (event) {

            if (  $('select[name=level]').val() > 0 )
            {
                ajax_choice($('select[name=level]'),$('select[name=theme]')) ;            
            }
            else 
            {   
                alert("Vous devez choisir un niveau."); return false;             
            }
        }); 

 
        function ajax_choice(param0, param1){

            let level_id = param0.val();
            let theme_id = param1.val();
            let subject_id = $("#id_subject").val();
            let flashpack_id = $("#flashpack_id").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            console.log(subject_id  ) ;
            url= "ajax_search_flashpack" ; 


            if($("#loader")) {$("#loader").html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>");      }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'level_id': level_id,
                        'theme_id': theme_id,
                        'subject_id': subject_id,
                        'flashpack_id': flashpack_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: url,
                    success: function (data) {
 
                        $('#content_flashpack').html("").html(data.html);
                        $("#loader").html(""); 
                        
                        }
                }
            )
        }






        $('.click_this_level').on('click', function (event) {

            let level_id = $(this).data("level_id");
            let subject_id = $(this).data("subject_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'level_id'  : level_id,
                        'subject_id': subject_id,                    
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "ajax_my_flashpacks" ,
                    success: function (data) {

                        $("#my_biblio").html(data.html) ;

                    }
                }
            )


        });




    $('#id_waiting').on('change', function (event) {

        let level_id = $("#id_level").val();
        let subject_id = $("#id_subject").val();
        let theme_id = $("#id_theme").val();
        let waiting_id = $(this).val();
        let flashpack_id = $("#flashpack_id").val();
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 

        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'level_id'  : level_id,
                    'subject_id': subject_id,  
                    'waiting_id'  : waiting_id,   
                    'theme_id': theme_id, 
                    'flashpack_id': flashpack_id,
                    csrfmiddlewaretoken: csrf_token
                },
                url : "ajax_search_flashpack" ,
                success: function (data) {

                    $("#content_flashpack").html(data.html) ;

                }
            }
        )
    });


    $('#keyword').on('keyup', function (event) {

        let level_id = $("id_level").val();
        let subject_id = $("id_subject").val();
        let waiting_id =  $("#waiting_id").val();
        let keyword = $(this).val();
        let theme_id = $("#id_theme").val();
        let flashpack_id = $("#flashpack_id").val();
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'level_id'  : level_id,
                    'subject_id': subject_id,  
                    'waiting_id': waiting_id,   
                    'keyword'   : keyword, 
                    'theme_id': theme_id,
                    'flashpack_id': flashpack_id,
                    csrfmiddlewaretoken: csrf_token
                },
                url : "ajax_search_flashcard" ,
                success: function (data) {

                    $("#content_flashpack").html(data.html) ;

                }
            }
        )
    });




    $('body').on('click', '.get_flashpack' , function (event) {

 
        let flashpack_id = $("#flashpack_id").val();
        let flashcard_id = $(this).data("flashcard_id");
        let statut = $(this).data("statut");   
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'flashpack_id' : flashpack_id, 
                    'flashcard_id' : flashcard_id,
                    'statut'       : statut,
                    csrfmiddlewaretoken: csrf_token
                },
                url : "../ajax_set_flashcard_in_flashpack" ,
                success: function (data) {

                    $("#contenair_search_flashcard"+flashcard_id).remove() ;
                    $("#nb_flashcards").html(data.nb);
                }
            }
        )
    });



    

});

});

