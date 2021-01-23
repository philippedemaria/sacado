define(['jquery',  'bootstrap', 'ui' , 'ui_sortable' , 'uploader'], function ($) {
    $(document).ready(function () {
 
    $("#loading").hide(500); 
    console.log(" ajax-quizz chargé ");
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
                    url : "../qcm/ajax/chargethemes_parcours",
                    success: function (data) {

                        themes = data["themes"];
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


 

                        $("#loading").hide(500); 
                    }
                }
            )
        });



 
        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('body').on('click', '.selector_question' , function (event) {

            let kind = $(this).attr("data-kind");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'kind': kind,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../get_question_type",
                    success: function (data) {

                        $('#body_question').html(data.html);
                        $('#type_of_question_in_title').html(data.title);
 
                    }
                }
            )
         });


 
        // Soumission de la question.
        $('body').on('click', '#submit_question' , function (event) {

            // obliger un titre
            if ($("#id_title").val() == "") { alert("Vous devez renseigner la question") ; $("#id_title").focus() ; return false ;}

            // obliger une réponse
            if ($("#kind").val() == "1") { 
                if ($(".checkbox_no_display").length == 0) { alert("Vous devez choisir LA bonne réponse.") ;  return false ;}
            }
            else if ($("#kind").val() == "2") 
            { 
                if ($("#answers").length  == 0) { alert("Vous devez écrire la réponse attendue.") ;  return false ;}
            }
            else 
            { 
                if ($(".checkbox_no_display").length  == 0) { alert("Vous devez choisir au moins une réponse vraie.") ;  return false ;}
            }


            // obliger qu'une seule réponse dans le QCS
            var n = $( "input:checked" ).length;  console.log(n) ; 
            if (($("#kind").val() == "4")&& (n>1)) { 
                alert("Vous avez choisi le type QCS. Vous ne pouvez renseigner qu'une seule bonne réponse. Choisissez le type QCM sinon.") ;
                return false ;
            }

            var formData = new FormData($("#question_form")[0]);
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            // Chargement des images de question
            var imagefile = $("#id_imagefile")[0].files[0];
            if (imagefile)
            {
                formData.append('imagefile[]', imagefile, imagefile.name);                
            }

            // Chargement des images de réponses
            if ( $("#kind").val() > 2 )
            {
                    for (var j = 1; j < 4; j++) { 
                        var imagefiles = $("#id_imageanswer"+j)[0].files;
                        if (imagefiles.length > 0 )

                            {   console.log("ici");
                                imagefile = imagefiles[0] ; 
                                formData.append('imagefiles[]', imagefile, imagefile.name);  
                            } 
                    }                
            }




            $.ajax(
                {
                    type: "POST",
                    data: formData,
                    url: "../send_question",
                    contentType: false, 
                    processData: false,
                    success: function (data) {

 

                        $('#body_question').html(data.html);
                        $('#questions_sortable_list').append(data.question);

 
                    }
                }
            )
         });
 
 

        // Sélectionne le choix de la réponse écrite vraie
        function checked_and_checked(nb){ 

            $('body').on('click', '#checking_zone'+nb , function (event) {     console.log( $("#id_is_correct"+nb).is(":checked") ) ;

                if( $("#id_is_correct"+nb).is(":checked")  )  
                    {   
                        $("#id_is_correct"+nb).removeAttr("checked");
                        $('#check'+nb).removeAttr("style");
                        $('#noCheck'+nb).removeAttr("style");
                        console.log("il est no checked"  ) ;
                    } 
                else 
                    {   
                        $("#id_is_correct"+nb).attr("checked",true);
                        $('#check'+nb).css("display","block");
                        $('#noCheck'+nb).css("display","none");
                        console.log( "il est checked"  ) ;
                    }
            });

        }

        checked_and_checked( '1') ;
        checked_and_checked( '2') ;
        checked_and_checked( '3') ;
        checked_and_checked( '4') ;

 

        // Sélectionne la couleur de fond lorsque la réponse est écrite
        function change_bg_and_select( nb, classe ){

            $('body').on('keyup', "#answer"+nb , function (event) {   
                
                    var comment =  $("#answer"+nb).val()  ;

                if (  comment.length > 0   )
                { 
                  $("#answer"+nb+"_div").addClass(classe) ; 
                  $("#answer"+nb).css("color","white") ;
                }
                else
                {
                   $("#answer"+nb+"_div").removeClass(classe) ; 
                  $("#answer"+nb).css("color","#666") ;
                }
             });
        }

       change_bg_and_select( "1",  "bgcolorRed" );
       change_bg_and_select( "2",  "bgcolorBlue" );
       change_bg_and_select( "3",  "bgcolorOrange" );
       change_bg_and_select( "4",  "bgcolorGreen" );



 

        $('#questions_sortable_list').sortable({
            start: function( event, ui ) { 
                   $(ui.item).css("box-shadow", "2px 1px 2px gray").css("background-color", "#271942").css("color", "#FFF"); 
               },
            stop: function (event, ui) {

                var valeurs = "";
                         
                $(".sorted_question_id").each(function() {
                    let this_question_id = $(this).val();
                    valeurs = valeurs + this_question_id +"-";
                });


                $(ui.item).css("box-shadow", "0px 0px 0px transparent").css("background-color", "#dbcdf7").css("color", "#271942"); 

                $.ajax({
                        data:   { 'valeurs': valeurs ,   } ,   
                        type: "POST",
                        dataType: "json",
                        url: "../question_sorter" 
                    }); 
                }
            });


        $('[type=checkbox]').prop('checked', false);     

        // Affiche une question
        $('body').on('click', '.update_question' , function (event) {   
            
            let quizz_id = $(this).attr("data-quizz_id");
            let question_id = $(this).attr("data-question_id");
            let kind = $(this).attr("data-kind");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'quizz_id': quizz_id,
                        'question_id': question_id,
                        'kind': kind,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../get_question_type",
                    success: function (data) {

                        $('#body_question').html(data.html);
 
 
                    }
                }
            )
         });
 
 

            $('.carousel').carousel({
              interval: 1000 * 10 
            });
 
 


 
    });
});