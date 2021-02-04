define(['jquery',  'bootstrap', 'ui' , 'ui_sortable' ], function ($) {
    $(document).ready(function () {
 
    $("#loading").hide(500); 
    console.log(" ajax-diaporama chargé ");
  // Affiche dans la modal la liste des élèves du groupe sélectionné
 


 
        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('body').on('click', '.selector_slide' , function (event) {


            let diaporama_id = $("#diaporama_id").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();  console.log(diaporama_id) ; 

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'diaporama_id': diaporama_id,
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
        $('body').on('click', '#submit_slide' , function (event) {

            // obliger un titre
            if ($("#id_title").val() == "") { alert("Vous devez renseigner le titre") ; $("#id_title").focus() ; return false ;}


            var formData = new FormData($("#slide_form")[0]);
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            // var content = $( '#id_texte' ).val();
            // formData.append('texte', content ); 
            $.ajax(
                {
                    type: "POST",
                    data: formData,
                    url: "../send_slide",
                    contentType: false, 
                    processData: false,
                    success: function (data) {

                        $('#body_question').html(data.html);
                        $('#id_title').val("");
                        $('#id_content').val(""); 

                        if (data.new) {
                            $('#slides_sortable_list').append(data.slide);  
                        }

                        else {
                            $('#slide'+data.id).append(data.name);  
                            $('#fa'+data.id).addClass(data.class).removeClass(data.noclass);  
                        }

                    }
                }
            )
         });
 
 

        $('#slides_sortable_list').sortable({
            start: function( event, ui ) { 
                   $(ui.item).css("box-shadow", "2px 1px 2px gray").css("background-color", "#271942").css("color", "#FFF"); 
               },
            stop: function (event, ui) {

                var valeurs = "";
                         
                $(".sorted_slide_id").each(function() {
                    let this_slide_id = $(this).val();
                    valeurs = valeurs + this_slide_id +"-";
                });


                $(ui.item).css("box-shadow", "0px 0px 0px transparent").css("background-color", "#dbcdf7").css("color", "#271942"); 


                console.log(valeurs) ; 



                $.ajax({
                        data:   { 'valeurs': valeurs ,   } ,   
                        type: "POST",
                        dataType: "json",
                        url: "../slide_sorter" 
                    }); 
                }
            });


 

            // Affiche une question
            $('body').on('click', '.update_slide' , function (event) {   
                
                let diaporama_id = $(this).attr("data-diaporama_id");
                let slide_id = $(this).attr("data-slide_id");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
     
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'diaporama_id': diaporama_id,
                            'slide_id': slide_id,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: "../get_slide_type",
                        success: function (data) {

                            $('#body_slide').html(data.html);
     
     
                        }
                    }
                )
             });

 
    });
});