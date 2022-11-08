define(['jquery',  'bootstrap', 'ui' , 'ui_sortable' , 'uploader','config_toggle'], function ($) {
    $(document).ready(function () {


    console.log(" qcm-numeric chargé ");

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



        function asnwerfontsize(choice) {

            let fs ;
            if ( choice.length > 50) { fs = 1.2 ;}
            else if ( choice.length > 17) { fs = 1.7 ;}
            else if ( choice.length > 10) { fs = 2.5 ;}
            else { fs = 3 ;}

            return fs;
        }




        // // Chargement d'une image dans la réponse possible.
        // $('body').on('click', '.automatic_insertion' , function (event) {  
 
        //     var feed_back = $(this).attr('id');
        //     $("#div_"+feed_back).toggle(500);

        //  });



        // Chargement d'une image dans la réponse possible.
        $('body').on('click', '.checker' , function (event) {  

            var global_div = $(this).parent().parent().parent();
 
            if ($(this).is(":checked")) { global_div.addClass("border_green");  }
            else { global_div.removeClass("border_green");  }
 

         });





        // function noPreviewFile(nb) {  
        //     $("#id_choices-"+nb+"-imageanswer").attr("src", "" );
        //     $("#preview"+nb).val("") ;  
        //     $("#file-image"+nb).removeClass("preview") ;
        //     $("#preview"+nb).addClass("preview") ; 
        //     $("#id_choices"+nb+"-imageanswer").removeClass("preview") ;
        //   }




        // $('body').on('change', '.choose_imageanswer' , function (event) {
        //     var suffix = this.id.match(/\d+/); 
        //     previewFile(suffix) ;
        //  });  



        // $('body').on('click', '.deleter_img' , function (event) {

        //         var suffix = $(this).data("id"); 
        //         noPreviewFile(suffix) ;
        //         $(this).remove(); 
        //     });  


        $('#click_button').on('click',  function (event) { 

                if( !$('.checker').is(':checked') ){
                    alert(" Cocher au moins une réponse "); return false ;
                }  

            });




        // $(document).on('click', '.add_more', function (event) {


        //         var total_form = $('#id_choices-TOTAL_FORMS') ;
        //         var totalForms = parseInt(total_form.val())  ;

        //         var thisClone = $('#rowToClone');
        //         rowToClone = thisClone.html() ;

        //         $('#formsetZone').append(rowToClone);

        //         $('#duplicate').attr("id","duplicate"+totalForms) 
        //         $('#cloningZone').attr("id","cloningZone"+totalForms) 
        //         $('#imager').attr("id","imager"+totalForms) 
        //         $('#file-image').attr("id","file-image"+totalForms) 
        //         $('#feed_back').attr("id","feed_back"+totalForms)          
        //         $('#div_feed_back').attr("id","div_feed_back"+totalForms)     
                
        //         $("#choices-"+totalForms+"-is_correct").prop("checked", false); 
        //         $("#duplicate"+totalForms+" input").each(function(){ 
        //             $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
        //             $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
        //         });

 
        //         $("#duplicate"+totalForms+" textarea").each(function(){ 
        //             $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
        //             $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
        //         });
 

        //         $('#spanner').attr("id","spanner"+totalForms) ;
        //         $('#preview').attr("id","preview"+totalForms) ;
        //         total_form.val(totalForms+1);
        //     });



        // $(document).on('click', '.remove_more', function () {
        //     var total_form = $('#id_choices-TOTAL_FORMS') ;
        //     var totalForms = parseInt(total_form.val())-1  ;

        //     $('#duplicate'+totalForms).remove();
        //     total_form.val(totalForms)
        // });

 
    });
});