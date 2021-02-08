define(['jquery', 'bootstrap' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-qrandom.js OK");


        $("[input='checkbox']").prop("checked",false);

 
        $('#id_level').on('change', function (event) {
            let id_level = $(this).val();
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
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
                    }
                }
            )
        });


        $('#id_theme').on('change', function (event) {
            let id_theme = $(this).val();
            let id_level = $("#id_level").val();
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'id_theme': id_theme,
                        'id_level': id_level,                     
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "../tool/ajax_chargewaitings",
                    success: function (data) {

                        let initial = $("<option>", {
                                        'value': 0,
                                        'html': "Choisir un attendu"
                                    });

                        $('select[name=waiting]').empty("").append(initial);

                        waitings = data["waitings"];
                        if (waitings.length >0)

                        { for (let i = 0; i < waitings.length; i++) {
                                    

                                    console.log(waitings[i]);
                                    let waitings_id = waitings[i][0];
                                    let waitings_name =  waitings[i][1]  ;
                                    let option = $("<option>", {
                                        'value': Number(waitings_id),
                                        'html': waitings_name
                                    });
                                    $('select[name=waiting]').append(option);
                                }
                        }
                        else
                        {
                                    let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                    });
                            $('select[name=waiting]').append(option);
                        }
                    }
                }
            )
        });


        $('#id_waiting').on('change', function (event) {

            let id_waiting = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'id_waiting': id_waiting,                     
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "../tool/ajax_chargeknowledges",
                    success: function (data) {

                        knowledges = data["knowledges"];

                        let initial = $("<option>", {
                                        'value': 0,
                                        'html': "Choisir un savoir faire"
                                    });

                        $('select[name=knowledge]').empty("").append(initial);
                        if (knowledges.length >0)

                        { for (let i = 0; i < knowledges.length; i++) {
                                    

                                    console.log(knowledges[i]);
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

                    }
                }
            )
        });

 


        $(document).on('click', '.add_more', function (event) {


                var total_form = $('#id_variables-TOTAL_FORMS') ;
                var totalForms = parseInt(total_form.val())  ;

                var thisClone = $('#rowToClone');
                rowToClone = thisClone.html() ;

                $('#formsetZone').append(rowToClone);

                $('#duplicate').attr("id","duplicate"+totalForms) 
                $('#cloningZone').attr("id","cloningZone"+totalForms) 

                $('#duplicate'+totalForms).find('.delete_button').html('<a href="javascript:void(0)" class="btn btn-danger remove_more" ><i class="fa fa-trash"></i></a>'); 
                $('#duplicate'+totalForms).find("input[type='checkbox']").bootstrapToggle();

                $("#duplicate"+totalForms+" input").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });

                console.log(totalForms+1);
                total_form.val(totalForms+1);
            });



        $(document).on('click', '.remove_more', function () {
            var total_form = $('#id_variables-TOTAL_FORMS') ;
            var totalForms = parseInt(total_form.val())-1  ;

            $('#duplicate'+totalForms).remove();
            total_form.val(totalForms)
        });


 

        $(document).on('click', '.add_more_image', function (event) {


            var total_form     = $('#id_variables-TOTAL_FORMS') ;
            var totalForms     = parseInt(total_form.val())-1  ;
            var variable       = $("#id_variables-"+totalForms+"-name").val();
            var selector_image = $('#id_images-TOTAL'+totalForms) ;
            var number_image   = parseInt(selector_image.val());
            var thisClone      = $('#imageToClone') ;
            var imageToClone   = thisClone.html() ;

            if (variable=="") { alert("Nommer la variable"); return false;}

            $('#cloningZone'+totalForms).append(imageToClone);
            $('#duplicateImage').attr("id","duplicateImage"+number_image) 
            $('#duplicateImage'+number_image).find('.delete_button_image').html('<a href="javascript:void(0)" class="btn btn-danger remove_more_image" ><i class="fa fa-trash"></i></a>'); 
            $('#duplicateImage'+number_image+" input").each(function(){ 
                $(this).attr('id',$(this).attr('id').replace('__var__',variable));
                $(this).attr('id',$(this).attr('id').replace('__nbr__',number_image));
                $(this).attr('name',$(this).attr('name').replace('__var__',variable));
                $(this).attr('name',$(this).attr('name').replace('__nbr__',number_image));
            });

            selector_image.val(number_image + 1);

            });



        $(document).on('click', '.remove_more_image', function () {
            var total_form   = $('#id_variables-TOTAL_FORMS') ;
            var totalForms   = parseInt(total_form.val())-1  ;
            var selector_img = $('#id_images-TOTAL'+totalForms)  ;
            var nbr_img      = selector_img.val();
            var nbr_rmv_img  = parseInt(nbr_img)-1 ;

            $('#duplicateImage'+nbr_rmv_img).remove();
            selector_img.val(nbr_rmv_img) ;
        });



                
    });

});
 

 
 

 
 
 