define(['jquery',  'bootstrap', 'ui' , 'ui_sortable' , 'uploader','config_toggle'], function ($) {
    $(document).ready(function () {


    console.log(" ajax-quizz-numeric chargé ");


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


    $('input[name=waitings]').on('click', function (event) {

            let waitings = $(this).val();
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


 


        $("#id_calculator").prop("checked", false);   
        $("#id_is_publish").prop("checked", true); 

 
 

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




 

        $("#support_image").on('click', function (event) {

            get_the_target("#support_image","#drop_zone_image","#video_div","#audio_div")

        })



        $("#support_video").on('click', function (event) { 

            get_the_target("#support_video","#video_div","#drop_zone_image","#audio_div")

        })



        $("#support_audio").on('click', function (event) { 

            get_the_target("#support_audio","#audio_div","#drop_zone_image","#video_div")

        })


        $("#support_audio_image").on('click', function (event) { 

            get_the_target_2("#support_audio_image","#drop_zone_image","#audio_div","#video_div")

        })



 
        function get_the_target(target,cible,f1,f2){

            $(f1).removeClass("allowed_display");
            $(f2).removeClass("allowed_display");
            $(f1).addClass("not_allowed_display");
            $(f2).addClass("not_allowed_display");

            if ($(cible).hasClass("not_allowed_display")) 
            {
                $(cible).removeClass("not_allowed_display");
                $(cible).addClass("allowed_display");
            } else {
                $(cible).removeClass("allowed_display");                
                $(cible).addClass("not_allowed_display");
            }
        }

        function get_the_target_2(target,cible,f1,f2){

            $(f1).removeClass("allowed_display");
            $(f2).removeClass("allowed_display");
            $(f1).addClass("not_allowed_display");
            $(f2).addClass("not_allowed_display");

            if ($(cible).hasClass("not_allowed_display")) 
            {
                $(cible).removeClass("not_allowed_display");
                $(cible).addClass("allowed_display");
                $(f1).removeClass("not_allowed_display");
                $(f1).addClass("allowed_display");
            } else {
                $(cible).removeClass("allowed_display");                
                $(cible).addClass("not_allowed_display");
                $(f1).removeClass("not_allowed_display");
                $(f1).addClass("allowed_display");
            }
        }



        $("#this_question_display_overview").on('click', function (event) {  

            MathJax.Hub.Queue(["Typeset",MathJax.Hub]);

            let type = $("#qtype").val(); 
            let title      = $("#id_title").val();
            let fontsize   = $("#id_size").val();
            let calculator = $("#id_calculator").val();
            let duration   = $("#id_duration").val();
            let audio      = $("#id_audio").val();  
            let video      = $("#id_video").val(); 
            let preview    = $("#drop_zone img")[0]; 
            let imagefile  = $("#id_imagefile").val(); 

            $("#overview_text").html(title);
            $("#overview_text").css("font-size",fontsize);
            $("#overview_duration").html(duration);


            let qcm ;

            if (type == 1 )
            {
                let true_false = "<div class='col-sm-12 col-md-6  bgcolorBlue white'  align='center' style='border-radius : 10px'><h1 style='font-size:3.5em' class='thin'>VRAI </h1></div><div class='col-sm-12 col-md-6  bgcolorRed white'  align='center' style='border-radius : 10px'><h1 style='font-size:3.5em' class='thin'>FAUX </h1></div>"
                $("#overview_answers").html("").append(true_false);
            }
            else if (type > 2 )
            {
                qcm = "" ;
                var i = 1;
                $.each($(".quizz_answer"), function(index, value) {
                  choice = $( this ).val();
                  if (i%2==1) { var colorback = "#f1eef7" ; } else { var colorback = "#FFF" ; }
                  qcm = qcm + "<div class='col-sm-12 col-md-12' style='font-size:30px;border-radius : 10px;background-color:"+colorback+";margin:10px 0px; padding:10px;'>"+i +". "+choice +"</div>";
                  i++;
                });

                $("#overview_answers").html("").append(qcm);
            }


 
            if (audio)
            {
                let overview_audio = "<audio controls><source src='#' type='audio/mpeg'></audio>"
                $("#overview_audio").html("").append(overview_audio);
            }

            if (video)
            {
                $("#overview_video").html("").append(video);
            }

            if (imagefile)
            {
                let size_img ;
                if (type == 2 ){ size_img = 550+"px" ;  } else { size_img = 350+"px" ;  }  
                overviewpreviewFile();  
                $("#overview_imagefile").attr("width", size_img );
            }
            else 
            {
 
                if ( $("#drop_zone img")[0] ) 
                    {   
                        let size_img ;
                        if (type == 2 ){ size_img = 550+"px" ;  } else { size_img = 350+"px" ;  }  
                        $("#overview_imagefile").attr("width", size_img ).attr("src", $("#drop_zone img")[0].currentSrc );
                    }
 
            }


            let file0 = $("#preview0").attr('src') ;
            let file1 = $("#preview1").attr('src') ;
            let file2 = $("#preview2").attr('src') ;
            let file3 = $("#preview3").attr('src') ;

            if (file0)
            {

 
                if (theme) {  
                    qcm = "<div class='col-sm-12 col-md-6'   style='border-radius : 10px'>"
                    if(file0) { qcm = qcm +"<img src='"+file0+"' height='90px' id='id_choices-0' />"}
                    qcm = qcm +"</div><div class='col-sm-12 col-md-6'   style='border-radius : 10px'>"
                    if(file2) { qcm = qcm +"<img src='"+file2+"' height='90px' id='id_choices-1' />"}
                    qcm = qcm +"</div><div class='col-sm-12 col-md-6'  style='border-radius : 10px'>"
                    if(file1) { qcm = qcm + "<img src='"+file1+"' height='90px' id='id_choices-2' />"}
                    qcm = qcm + "</div><div class='col-sm-12 col-md-6'  style='border-radius : 10px'>"
                    if(file3) { qcm = qcm + "<img  src='"+file3+"' height='90px' id='id_choices-3' />"}
                    qcm = qcm + "</div>"  
                }
                else{ 
 
                    qcm = "<div class='col-sm-12 col-md-6 bgcolorRed white'   style='border-radius : 10px'>"
                    if(file0) { qcm = qcm +"<img src='"+file0+"' height='90px' id='id_choices-0' />"}
                    qcm = qcm +"</div><div class='col-sm-12 col-md-6 bgcolorBlue white'   style='border-radius : 10px'>"
                    if(file2) { qcm = qcm +"<img src='"+file2+"' height='90px' id='id_choices-1' />"}
                    qcm = qcm +"</div><div class='col-sm-12 col-md-6  bgcolorOrange white'  style='border-radius : 10px'>"
                    if(file1) { qcm = qcm + "<img src='"+file1+"' height='90px' id='id_choices-2' />"}
                    qcm = qcm + "</div><div class='col-sm-12 col-md-6 bgcolorGreen white'  style='border-radius : 10px'>"
                    if(file3) { qcm = qcm + "<img  src='"+file3+"' height='90px' id='id_choices-3' />"}
                    qcm = qcm + "</div>"


                }
                $("#overview_answers").html("").append(qcm);

            }
        })

        function overviewpreviewFile() {

            const file = $('#id_imagefile')[0].files[0];
            const reader = new FileReader();

            reader.addEventListener("load", function (e) {
                                                var image = e.target.result ; 
                                                $("#overview_imagefile").attr("src", image );
                                            }) ;

            if (file) { console.log(file) ;
              reader.readAsDataURL(file);
            }            

          }

        function asnwerfontsize(choice) {

            let fs ;
            if ( choice.length > 50) { fs = 1.2 ;}
            else if ( choice.length > 17) { fs = 1.7 ;}
            else if ( choice.length > 10) { fs = 2.5 ;}
            else { fs = 3 ;}

            return fs;
        }




        // Chargement d'une image dans la réponse possible.
        $('body').on('click', '.automatic_insertion' , function (event) {  
 
            var feed_back = $(this).attr('id');
            $("#div_"+feed_back).toggle(500);

         });



        // Chargement d'une image dans la réponse possible.
        $('body').on('click', '.checker' , function (event) {  

            var global_div = $(this).parent().parent().parent();
 
            if ($(this).is(":checked")) { global_div.addClass("border_green");  }
            else { global_div.removeClass("border_green");  }
 

         });





 
        function previewFile(nb) {

            const file = $('#id_choices-'+nb+'-imageanswer')[0].files[0];
            const reader = new FileReader();

 

            $("#preview"+nb).val("") ;  
            $("#file-image"+nb).addClass("preview") ;
            $("#preview"+nb).removeClass("preview") ; 
            $("#id_choices"+nb+"-imageanswer").addClass("preview") ; 
            $("#imager"+nb).prepend("<a href='#' data-id='"+nb+"' class='deleter_img'><i class='bi bi-trash'></i></a>");
            reader.addEventListener("load", function (e) {
                                                var image = e.target.result ; 
                                                $("#preview"+nb).attr("src", image );
                                            }) ;

            if (file) { console.log(file) ;
              reader.readAsDataURL(file);
            }            

          }



        function noPreviewFile(nb) {  
            $("#id_choices-"+nb+"-imageanswer").attr("src", "" );
            $("#preview"+nb).val("") ;  
            $("#file-image"+nb).removeClass("preview") ;
            $("#preview"+nb).addClass("preview") ; 
            $("#id_choices"+nb+"-imageanswer").removeClass("preview") ;
          }




        $('body').on('change', '.choose_imageanswer' , function (event) {
            var suffix = this.id.match(/\d+/); 
            previewFile(suffix) ;
         });  



        $('body').on('click', '.deleter_img' , function (event) {

                var suffix = $(this).data("id"); 
                noPreviewFile(suffix) ;
                $(this).remove(); 
            });  


        $('#click_button').on('click',  function (event) { 

                if( !$('.checker').is(':checked') ){
                    alert(" Cocher au moins une réponse "); return false ;
                }  

            });




        $(document).on('click', '.add_more', function (event) {


                var total_form = $('#id_choices-TOTAL_FORMS') ;
                var totalForms = parseInt(total_form.val())  ;

                var thisClone = $('#rowToClone');
                rowToClone = thisClone.html() ;

                $('#formsetZone').append(rowToClone);

                $('#duplicate').attr("id","duplicate"+totalForms) 
                $('#cloningZone').attr("id","cloningZone"+totalForms) 
                $('#imager').attr("id","imager"+totalForms) 
                $('#file-image').attr("id","file-image"+totalForms) 
                $('#feed_back').attr("id","feed_back"+totalForms)          
                $('#div_feed_back').attr("id","div_feed_back"+totalForms)     
                
                $("#choices-"+totalForms+"-is_correct").prop("checked", false); 
                $("#duplicate"+totalForms+" input").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });

 
                $("#duplicate"+totalForms+" textarea").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });
 

                $('#spanner').attr("id","spanner"+totalForms) ;
                $('#preview').attr("id","preview"+totalForms) ;
                total_form.val(totalForms+1);
            });



        $(document).on('click', '.remove_more', function () {
            var total_form = $('#id_choices-TOTAL_FORMS') ;
            var totalForms = parseInt(total_form.val())-1  ;

            $('#duplicate'+totalForms).remove();
            total_form.val(totalForms)
        });

 
    });
});