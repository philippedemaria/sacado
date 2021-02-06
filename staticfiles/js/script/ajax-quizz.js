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
                    url : "../../qcm/ajax/chargethemes_parcours",
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





        $('input[name=waitings]').on('click', function (event) {

            let waitings = $(this).val();
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $("#loading").html("<i class='fa fa-spinner fa-pulse fa-fw'></i>");
            $("#loading").show(); 

            console.log(waitings) ;

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'waitings': waitings,                     
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "../../tool/ajax_chargeknowledges",
                    success: function (data) {

                        knowledges = data["knowledges"];
 
 

                        for (let i = 0; i < knowledges.length; i++) {
                                
                                console.log(knowledges[i]);
                                let knowledges_id = knowledges[i][0];
                                
                                $('hidden_knowledges').hide(500);
                                $('knowledge'+knowledges_id).show(500);
                            }
                      
                  

 

                        $("#loading").hide(500); 
                    }
                }
            )
        });




        $("#div_is_mark").hide(); 

            function makeItemAppear($toggle, $item) {
                    $toggle.change(function () {
                        if ($toggle.is(":checked")) {
                            $item.show(500);
                        } else {
                            $item.hide(500);
                        }
                    });
                }
 
        makeItemAppear($("#id_is_numeric"), $("#div_is_mark"));





        // Fonction de sélection du Vrai faux
        function checked_vf(){ 
            if( $("#check1").hasClass("checked")  )  
                {   
                    // Gestion du check
                    $('#check1').removeClass("checked");
                    $('#check2').addClass("checked");
                    // affiche du fa
                    $('#check1').css("display","none");
                    $('#noCheck1').css("display","block");
                    $('#check2').css("display","block");
                    $('#noCheck2').css("display","none");
                    $("#id_is_correct").prop("checked", false); 
                } 
            else 
                {   
                    // Gestion du check
                    $('#check1').addClass("checked");
                    $('#check2').removeClass("checked");
                    // affiche du fa
                    $('#check2').css("display","none");
                    $('#noCheck2').css("display","block");
                    $('#check1').css("display","block");
                    $('#noCheck1').css("display","none");
                    $("#id_is_correct").prop("checked", true); 
                }             
        }

        $('body').on('click', '#vf_zone1' , function (event) {  
            checked_vf() ;
        }); 
        $('body').on('click', '#vf_zone2' , function (event) {  
            checked_vf() ;
        }); 

        // Fonction de sélection du de la calculatrice ou de la publication
        $('body').on('click', '#check_calculator' , function (event) {  
            check_assets("#id_calculator"); 
        }); 
        $('body').on('click', '#check_publish' , function (event) {  
            check_assets("#id_is_publish"); 
        }); 



        function check_assets(cible){

            if ($(cible).is(":checked"))
            {
             $(cible).prop("checked", false); 
            }
            else
            {
             $(cible).prop("checked", true); 
            }  
        }



        $("#id_calculator").prop("checked", false);   
        $("#id_is_publish").prop("checked", true); 


        $('body').on('click', '#checking_zone0' , function (event) {  
            checked_and_checked(0) ;
        });
        $('body').on('click', '#checking_zone1' , function (event) {  
            checked_and_checked(1) ;
        });
        $('body').on('click', '#checking_zone2' , function (event) {  
            checked_and_checked(2) ;
        });
        $('body').on('click', '#checking_zone3' , function (event) {  
            checked_and_checked(3) ;
        });


        function checked_and_checked(nb){ 
                qtype = $("#qtype").val() ;

                if( $("#check"+nb).hasClass("checked")  )  
                    {   
                        $('#check'+nb).removeClass("checked");
                        $('#check'+nb).css("display","none");
                        $('#noCheck'+nb).css("display","block");
                        $("#id_choice-"+nb+"-is_correct").prop("checked", false);                         

                    } 
                else 
                    {   
                        $('#check'+nb).addClass("checked");
                        $('#check'+nb).css("display","block");
                        $('#noCheck'+nb).css("display","none");
                        $("#id_choice-"+nb+"-is_correct").prop("checked", true);                     
                    }
 
                if (qtype==4 && $(".checked").length > 1 ) { 
                    alert("Vous avez choisi un QCS dans lequel une seule réponse est autorisée. Optez pour le QCM alors.") ; 
                    $('#check'+nb).removeClass("checked");
                    $('#check'+nb).css("display","none");
                    $('#noCheck'+nb).css("display","block");
                    $("#id_choice-"+nb+"-is_correct").prop("checked", false);                         
                    return false;
                }
            }
 

        // Sélectionne la couleur de fond lorsque la réponse est écrite
        function change_bg_and_select( nb, classe ){

            $('body').on('keyup', "#id_choice-"+nb+"-answer" , function (event) {   
                
                    var comment =  $("#id_choice-"+nb+"-answer").val()  ;

                if (  comment.length > 0   )
                { 
                  $("#answer"+nb+"_div").addClass(classe) ; 
                  $("#id_choice-"+nb+"-answer").css("color","white") ;
                }
                else
                {
                   $("#answer"+nb+"_div").removeClass(classe) ; 
                  $("#id_choice-"+nb+"-answer").css("color","#666") ;
                }
             });
        }

       change_bg_and_select( 0,  "bgcolorRed" );
       change_bg_and_select( 1,  "bgcolorBlue" );
       change_bg_and_select( 2,  "bgcolorOrange" );
       change_bg_and_select( 3,  "bgcolorGreen" );



 
       // Trie des diapositives
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
                        url: "../../question_sorter" 
                    }); 
                }
            });
 
       // Prévisualisation des images
        $("#id_imagefile").withDropZone("#drop_zone", {
            action: {
              name: "image",
              params: {
                preview: true,
              }
            },
          });


        // Chargement d'une image dans la réponse possible.
        $('body').on('change', '#id_choice-0-imageanswer' , function (event) {  
            previewFile(0,"bgcolorRed") ;
         });

        $('body').on('change', '#id_choice-1-imageanswer' , function (event) {   
            previewFile(1,"bgcolorBlue") ;
         });
 
        $('body').on('change', '#id_choice-2-imageanswer' , function (event) {   
            previewFile(2,"bgcolorOrange") ;
         });
 
        $('body').on('change', '#id_choice-3-imageanswer' , function (event) {   
            previewFile(3,"bgcolorGreen") ;
         });      

 
        function previewFile(nb,classe) {

            const preview = $('#preview'+nb);
            const file = $('#id_choice-'+nb+'-imageanswer')[0].files[0];
            const reader = new FileReader();


            $("#preview"+nb).val("") ;  
            $("#answer"+nb+"_div").addClass(classe) ;
            $("#id_choice-"+nb+"-answer").addClass("preview") ;
            $("#preview"+nb).removeClass("preview") ; 
            $("#delete_img"+nb).removeClass("preview") ; 

            reader.addEventListener("load", function (e) {
                                                var image = e.target.result ; 
                                                $("#preview"+nb).attr("src", image );
                                            }) ;

            if (file) { console.log(file) ;
              reader.readAsDataURL(file);
            }            

          }
 
         
        // Chargement d'une image dans la réponse possible.
        $('body').on('click', '#delete_img0' , function (event) {  
            noPreviewFile(0,"bgcolorRed") ;
         });

        $('body').on('click', '#delete_img1' , function (event) {   
            noPreviewFile(1,"bgcolorBlue") ;
         });
 
        $('body').on('click', '#delete_img2' , function (event) {   
            noPreviewFile(2,"bgcolorOrange") ;
         });
 
        $('body').on('click', '#delete_img3' , function (event) {   
            noPreviewFile(3,"bgcolorGreen") ;
         }); 


        function noPreviewFile(nb,classe) {

                $("#preview"+nb).attr("src", "" );
                $("#answer"+nb+"_div").removeClass(classe) ;
                $("#id_choice-"+nb+"-answer").removeClass("preview") ;
                $("#preview"+nb).addClass("preview") ; 
                $("#delete_img"+nb).addClass("preview") ;      
          }













 
    });
});