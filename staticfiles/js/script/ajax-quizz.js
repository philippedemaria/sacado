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


            if ($("#id_title").val() == "") { alert("Vous devez renseigner la question") ; $("#id_title").focus() ; return false ;}


            var n = $( "input:checked" ).length; console.log(n) ;

            if (($("#type_of_question").val() == "4")&& (n>1)) { 

                alert("Vous avez choisi le type QCS. Vous ne pouvez renseigner qu'une seule bonne réponse. Choisissez le type QCM sinon.") ;
                return false ;
            }

            var datas = $("#question_form").serialize();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: datas,
                    url: "../send_question",
                    success: function (data) {

 

                        $('#body_question').html(data.html);
                        $('#questions_sortable_list').append(data.question);

 
                    }
                }
            )
         });
 
 


        function checked_and_checked(clic, check, cible,  nockeck){ 

            $('body').on('click', clic , function (event) {     console.log( $(cible).is(":checked") ) ;

                if( $(cible).is(":checked")  )  
                    {   
                        $(cible).removeAttr("checked");
                        $(check).removeAttr("style");
                        $(nockeck).removeAttr("style");
                        console.log("il est no checked"  ) ;
                    } 
                else 
                    {   
                        $(cible).attr("checked",true);
                        $(check).css("display","block");
                        $(nockeck).css("display","none");
                        console.log( "il est checked"  ) ;
                    }
            });

        }

        checked_and_checked( '#checking_zone1' ,  '#check1', "#id_is_correct1", '#noCheck1') ;
        checked_and_checked( '#checking_zone2' ,  '#check2', "#id_is_correct2", '#noCheck2') ;
        checked_and_checked( '#checking_zone3' ,  '#check3', "#id_is_correct3", '#noCheck3') ;
        checked_and_checked( '#checking_zone4' ,  '#check4', "#id_is_correct4", '#noCheck4') ;

 


        function change_bg_and_select( cible, cible_div , classe ){
            $('body').on('keyup', cible , function (event) {   
                
                    var comment =  $(cible).val()  ;

                if (  comment.length > 0   )
                { 
                  $(cible_div).addClass(classe) ; 
                  $(cible).css("color","white") ;
                }
                else
                {
                   $(cible_div).removeClass(classe) ; 
                  $(cible).css("color","#666") ;
                }
             });
        }

       change_bg_and_select( "#answer1", "#answer1_div" , "bgcolorRed" );
       change_bg_and_select( "#answer2", "#answer2_div" , "bgcolorBlue" );
       change_bg_and_select( "#answer3", "#answer3_div" , "bgcolorOrange" );
       change_bg_and_select( "#answer4", "#answer4_div" , "bgcolorGreen" );



        // Selecteur du vrai faux
        $('body').on('click', '.selector_answer' , function (event) {   
            
            var classList = $(this).attr("class").split(/\s+/) ;  

            if ( classList.indexOf("quizz_true") !== -1    )
            { 
                $(".true_sentence").attr('checked',true) ;
                $(".wrong_sentence").attr('checked',false) ;
                $("#span_true").css('display','block') ;
                $("#span_wrong").css('display','none') ;
            }
            else
            {
                $(".wrong_sentence").attr('checked',true) ;
                $(".true_sentence").attr('checked',false) ;
                $("#span_true").css('display','none') ;
                $("#span_wrong").css('display','block') ;
            }


         });


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
                    url: "../get_an_existing_question",
                    success: function (data) {

                        $('#body_question').html(data.html);
 
 
                    }
                }
            )
         });
 
 


 
 


 
    });
});