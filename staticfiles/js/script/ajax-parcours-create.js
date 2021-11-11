define(['jquery',  'bootstrap',  'config_toggle'], function ($) {
    $(document).ready(function () {


    console.log(" ajax-folders-create chargé ");



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


   // récupère l'url de l'image dans le form d'un parcours pour l'utiliser dans la base de données
        $('body').on('click', '.selector_image_from_ajax' , function () {

                let url_image = $(this).data("url_image");

                $('#this_image_selected').val(url_image);

                $('.selector_image_from_ajax').addClass('opacity_selector_img');  
                $(this).removeClass('opacity_selector_img'); 

            });
 
    });
});