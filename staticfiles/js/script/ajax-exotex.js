define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-exercise.js OK");



        $('[type=checkbox]').prop('checked', false);            

        $('#id_is_publish').prop('checked', true);
        $('#id_is_share').prop('checked', true);  
        $("#publication_div").hide();
 

            makeDivAppear($("#id_is_publish"), $("#publication_div"));


            function makeDivAppear($toggle, $item) {
                    $toggle.change(function () {
                         $item.toggle();
                    });
                }
 

        $('#enable_correction_div').hide();
        $("#enable_correction").click(function(){ 
            $('#enable_correction_div').toggle(500);
        });


        $('#id_level').on('change', function (event) {
            let id_level = $(this).val();


    
            if ((id_level == "")||(id_level == " ")) { alert("Sélectionner un niveau") ; return false ;}
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            url_ = "../ajax_chargethemes" ;

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
            let bibliotex_id = $("#bibliotex_id").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            console.log(subject_id  ) ;
            url= "../ajax_level_exotex" ; 


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
                        'bibliotex_id': bibliotex_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: url,
                    success: function (data) {

                        if (data.knowledges) {


                                knowledges = data["knowledges"] ; 
                                $('select[name=knowledge]').empty("");
                                if (knowledges.length >0)
                                { 
                                    for (let i = 0; i < knowledges.length; i++) {
                                            
                                            let knowledges_id = knowledges[i][0];
                                            let knowledges_name =  knowledges[i][1]  ;
                                            let option = $("<option>", {
                                                'value': Number(knowledges_id),
                                                'html': knowledges_name
                                            });
                                            $('select[name=knowledge]').append(option);
                                        }
                                }
                                else
                                {
                                    let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                    });
                                    $('select[name=knowledge]').append(option);
                                }


                                knowledges_level = data["knowledges_level"] ; 
                                $('select[name=knowledges]').empty("");
                                if (knowledges_level.length >0)
                                { 
                                    for (let i = 0; i < knowledges_level.length; i++) {
                                            let knowledges_id = knowledges_level[i][0];
                                            let knowledges_name =  knowledges_level[i][1]  ;
                                            let option = $("<option>", {
                                                'value': Number(knowledges_id),
                                                'html': knowledges_name
                                            });
                                            $('select[name=knowledges]').append(option);
                                        }
                                }
                                else
                                {
                                    let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                    });
                                    $('select[name=knowledges]').append(option);
                                }



                        }
                        else {

                            $('#content_exercises').html("").html(data.html);
                            $("#loader").html(""); 

                        }

                    }
                }
            )
        }


});

});

