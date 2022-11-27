define(['jquery',  'bootstrap', 'ui' , 'ui_sortable' , 'config_toggle'], function ($) {
    $(document).ready(function () {


    console.log(" create_questions_all_forms chargé ");


    $("#loading").hide(500); 

 

        $(document).on('click', '.add_more', function (event) {


                var total_form = $('#id_choices-TOTAL_FORMS') ;
                var totalForms = parseInt(total_form.val())  ;

                var thisClone = $('#rowToClone');
                rowToClone = thisClone.html() ;

                $('#formsetZone').append(rowToClone);

                $('#duplicate').attr("id","duplicate"+totalForms) ;
                $('#cloningZone').attr("id","cloningZone"+totalForms) ;
                $('#imager').attr("id","imager"+totalForms) ;
                $('#file-image').attr("id","file-image"+totalForms) ;
                $('#feed_back').attr("id","feed_back"+totalForms)  ;       
                $('#div_feed_back').attr("id","div_feed_back"+totalForms)  ;
                $('#delete_img').attr("id","delete_img"+totalForms)  ;

                if( $('#imagerbis').length ) { 

                    $('#imagerbis').attr("id","imagerbis"+totalForms) ; 
                    $('#file-imagebis').attr("id","file-imagebis"+totalForms) ;
                    $('#preview_bis').attr("id","preview_bis"+totalForms) ;
                    $('#delete_imgbis').attr("id","delete_imgbis"+totalForms)  ;
                } 


                if( $('#imagersub').length ) { 

                    $('#subformsetZone').attr("id","subformsetZone"+totalForms)  ;

                    items = $("#subformsetZone"+totalForms+' .get_image') ; 
                    var i = 0 ;
                    for( var item in items ){
                        var suf = totalForms+'-'+i ; 
                        $('#imagersub').attr("id","imagersub"+suf) ;
                        $('#file-imagesub').attr("id","file-imagesub"+suf) ;
                        $('#previewsub').attr("id","previewsub"+suf) ;
                        $('#delete_subimg').attr("id","delete_subimg"+suf)  ;
                        i++;
                    }
 
                } 


                
                $("#choices-"+totalForms+"-is_correct").prop("checked", false); 
                $("#duplicate"+totalForms+" input").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });
                $('#duplicate'+totalForms).find("input[type='checkbox']").bootstrapToggle();
 
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

 


        $(document).on('click', '.add_sub_more', function (event) {


                var total_form = $('#id_subchoices-TOTAL_FORMS') ;
                var totalForms = parseInt(total_form.val())  ;

                var thisClone = $('#subToClone');
                subToClone = thisClone.html() ;

                loop = $(this).attr("data_loop");

                $('#subformsetZone'+loop).append(subToClone);

                $('#subduplicate').attr("id","subduplicate"+totalForms) ;
                $('#subcloningZone').attr("id","subcloningZone"+totalForms) ;
                $('#imagersub').attr("id","imagersub"+totalForms)    ;
                $('#file-imagesub').attr("id","file-imagesub"+totalForms);

                $("#subchoices-"+totalForms+"-is_correct").prop("checked", false); 
                $("#subduplicate"+totalForms+" input").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });

 
                $("#subduplicate"+totalForms+" textarea").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });
 

                $('#spanner').attr("id","spanner"+totalForms) ;
                $('#previewsub').attr("id","previewsub"+totalForms) ;
                total_form.val(totalForms+1);
            });



        $(document).on('click', '.remove_sub_more', function () {
            var total_form = $('#id_subchoices-TOTAL_FORMS') ;
            var totalForms = parseInt(total_form.val())-1  ;

            $('#subduplicate'+totalForms).remove();
            total_form.val(totalForms)
        });



 






    });
});