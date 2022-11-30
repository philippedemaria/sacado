define(['jquery','bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-evaluation.js OK");
 


       
        $('#id_is_favorite').prop('checked', true); 

        $('#id_zoom').prop('checked', false); 
        $('#id_is_share').prop('checked', false); 
        $('#id_is_publish').prop('checked', false); 
        $('#id_is_achievement').prop('checked', false); 
        $('#id_is_next').prop('checked', false); 
        $('#id_is_exit').prop('checked', false); 
        $('#id_is_stop').prop('checked', false); 
        $('#id_is_exit_div').hide(); 
 
        $("#id_is_next").change(function () {
                        if ($("#id_is_next").is(":checked")) {
                           $("#id_is_exit_div").show(500);
                        } else {
                          $("#id_is_exit_div").hide(500);
                        }
                    })



    $('body').on('change', '#id_subject' , function (event) {

 
        let id_subject = $("#id_subject").val();
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        url_ = "../../../tool/ajax_charge_groups" ;
        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'id_subject': id_subject,                       
                    csrfmiddlewaretoken: csrf_token
                },
                url : url_,
                success: function (data) {

                    groups = data["groups"] ; 
                    $('#grplist').empty("");

                    if (groups.length >0)
                    { for (let i = 0; i < groups.length ; i++) {
                                
                                let groups_id   = groups[i][0]; 
                                let groups_name =  groups[i][1] ; 

                                $('#grplist').append('<label for="cb'+Number(groups_id)+'"><input type="checkbox" id="cb'+Number(groups_id)+'" class="select_all" name="groups" value="'+Number(groups_id)+'" /> '+groups_name+'</label><br/>')
                            }
                    }

                }
            }
        )
    });

 

    $('body').on('change', '#id_level' , function (event) {

 
        let id_subject = $("#id_subject").val();
        let id_level   = $(this).val();
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        url_ = "../../../tool/ajax_charge_groups_level" ;
        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'id_subject': id_subject,   
                    'id_level'  : id_level,                  
                    csrfmiddlewaretoken: csrf_token
                },
                url : url_,
                success: function (data) {


                    if (data.imagefiles) { 

                                $('#label_vignette').html("").html("<label>Proposition de vignettes - cliquer pour sélectionner</label>");

                                $('#prop_vignette').html("");
                                imgs = "";
                                for (let i = 0; i < data.imagefiles.length; i++) {
                             
                                                imgs = imgs + "<img src='https://sacado.xyz/ressources/"+data.imagefiles[i]+"'  width='200px'  data-url_image='"+data.imagefiles[i]+"' class='selector_image_from_ajax' />";
                                            }
                                        
                                        $('#prop_vignette').append(imgs);

                                    }



                    groups = data["groups"] ; 
                    $('#grplist').empty("");

                    if (groups.length >0)
                    { for (let i = 0; i < groups.length ; i++) {
                                
                                let groups_id   = groups[i][0]; 
                                let groups_name =  groups[i][1] ; 

                                $('#grplist').append('<label for="cb'+Number(groups_id)+'"><input type="checkbox" id="cb'+Number(groups_id)+'" class="select_all" name="groups" value="'+Number(groups_id)+'" /> '+groups_name+'</label><br/>')
                            }
                    }

                }
            }
        )
    });


        // // Affiche dans la modal la liste des élèves du groupe sélectionné
        // $('#id_level').on('change', function (event) {
        //     let id_level = $(this).val();
        //     if ((id_level == "")||(id_level == " ")) { alert("Sélectionner un niveau") ; return false ;}
        //     let id_subject = $("#id_subject").val();
        //     let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        //     let is_update = $("#is_update").val();

        //     if (is_update=="1") {
        //             url_ = "../../../../../ajax/chargethemes" ;
        //     } 
        //     else {
        //             url_ = "../../ajax/chargethemes" ;
        //     }

        //     $.ajax(
        //         {
        //             type: "POST",
        //             dataType: "json",
        //             traditional: true,
        //             data: {
        //                 'id_level': id_level,
        //                 'id_subject': id_subject,                        
        //                 csrfmiddlewaretoken: csrf_token
        //             },
        //             url : "ajax/chargethemes",
        //             success: function (data) {

        //                 themes = data["themes"] ; 
        //                 $('select[name=theme]').empty("");



        //                 if (data.imagefiles) { 

        //                             $('#label_vignette').html("").html("<label>Proposition de vignettes - cliquer pour sélectionnner</label>");

        //                             $('#prop_vignette').html("");
        //                             imgs = "";
        //                             for (let i = 0; i < data.imagefiles.length; i++) {
                                 
        //                                             imgs = imgs + "<img src='https://sacado-academie.fr/ressources/"+data.imagefiles[i]+"'  width='200px'  data-url_image='"+data.imagefiles[i]+"' class='selector_image_from_ajax' />";
        //                                         }
                                            
        //                                     $('#prop_vignette').append(imgs);

        //                                 }



        //                 if (themes.length >0)
        //                 { for (let i = 0; i < themes.length; i++) {
                                    

        //                             console.log(themes[i]);
        //                             let themes_id = themes[i][0];
        //                             let themes_name =  themes[i][1]  ;
        //                             let option = $("<option>", {
        //                                 'value': Number(themes_id),
        //                                 'html': themes_name
        //                             });
        //                             $('select[name=theme]').append(option);
        //                         }
        //                 }
        //                 else
        //                 {
        //                             let option = $("<option>", {
        //                                 'value': 0,
        //                                 'html': "Aucun contenu disponible"
        //                             });
        //                     $('select[name=theme]').append(option);
        //                 }


        //             }
        //         }
        //     )
        // });
 
 
 
  // récupère l'url de l'image dans le form d'un parcours pour l'utiliser dans la base de données
        $('body').on('click', '.selector_image_from_ajax' , function () {

                let url_image = $(this).data("url_image");

                console.log(url_image) ;
                $('#this_image_selected').val(url_image);

                $('.selector_image_from_ajax').addClass('opacity_selector_img');  
                $(this).removeClass('opacity_selector_img'); 

            });



    $('body').on('change','.select_all',  function (event) {

        var valeurs = [];
        $('.select_all').each(function() {

            if ($(this).is(":checked"))

                    {   let group_id = $(this).val(); 
                        if (group_id !="")
                            {valeurs.push(group_id);}
                    }

        });

        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        url_ = "../../../tool/ajax_charge_folders" ;
        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'group_ids': valeurs,                       
                    csrfmiddlewaretoken: csrf_token
                },
                url : url_,
                success: function (data) {

                    folders = data["folders"] ; 
                    $('#flist').empty("");

                    if (folders.length >0)
                    { for (let i = 0; i < folders.length ; i++) {
                                
                                let folders_id = folders[i][0]; 
                                let folders_name =  folders[i][1] ; 

                                $('#flist').append('<label for="cb'+Number(folders_id)+'"><input type="checkbox" id="cb'+Number(folders_id)+'" name="folders" value="'+Number(folders_id)+'" /> '+folders_name+'</label><br/>')
                            }
                    }

                }
            }
        )
    });
















    });
});