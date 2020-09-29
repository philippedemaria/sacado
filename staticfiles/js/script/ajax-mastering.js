define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-mastering.js OK");
        console.log("mastering chargé celui-ci.");

 
  $(window).on('load', function () {
    if ($('#preloader').length) {
      $('#preloader').delay(100).fadeOut('slow', function () {
        $(this).remove();
      });
    }
  });

        $("#id_writing").attr("checked",false);



        $('.select_mastering').on('click', function (event) {
        
        let layer_value = $(this).attr("data-layer");

        $("#id_scale").val(layer_value);


        });
        // ================================ FIN ============================ 

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_level').on('change', function (event) {
            let id_level = $(this).val();
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            console.log(id_level) ; 
            console.log(id_subject) ;

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
                    url : "../../ajax/chargethemes",
                    success: function (data) {

                        themes = data["themes"]
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




 
        $('select[name=theme]').on('change', function (event) {

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
 

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            url = "../../ajax_level_exercise" ; 
 
            $("#loader").html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>");

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'level_id': level_id,
                        'theme_id': theme_id,
                         csrfmiddlewaretoken: csrf_token
                    },
                    url: url,
                    success: function (data) {
 
                        $('#content_exercises').html("").html(data.html);
                        $("#loader").html("").hide(); 
                        
                        }
                }
            )

        }


 



        $('.select_support_mastering').on('click', function (event) {
            
            let mastering_id = $(this).attr("data-mastering_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            console.log(mastering_id);

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'mastering_id': mastering_id,                      
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "../../ajax/mastering_modal_show",
                    success: function (data) {
                        $('#m_modale').removeClass(data.nocss);
                        $('#m_body').html(data.html);
                        $('#m_consigne').html(data.consigne);
                        $('#m_duration').html(data.duration);
                        $('#m_modale').addClass(data.css);
 
                    }
                }
            )
        });




    });        
});