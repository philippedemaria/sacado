define(['jquery',  'bootstrap', 'ui' , 'ui_sortable' , 'uploader','config_toggle'], function ($) {
    $(document).ready(function () {


    console.log(" ajax-quizz-create chargé ");



    $('body').on('change', '#id_subject' , function (event) {

 
        let id_subject = $("#id_subject").val();
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        url_ = "../ajax_charge_groups" ;
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





    $('body').on('change', '.select_all' , function (event) {

        var valeurs = [];
        $(".select_all").each(function() {

            if ($(this).is(":checked"))

                    {   let group_id = $(this).val(); 
                        if (group_id !="")
                            {valeurs.push(group_id);}
                    }

        });

        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        url_ = "../ajax_charge_folders" ;
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
                    $('#cblist').empty("");

                    if (folders.length >0)
                    { for (let i = 0; i < folders.length ; i++) {
                                
                                let folders_id = folders[i][0]; 
                                let folders_name =  folders[i][1] ; 

                                $('#cblist').append('<label for="cb'+Number(folders_id)+'"><input type="checkbox" id="cb'+Number(folders_id)+'" class="select_folders" name="folders" value="'+Number(folders_id)+'" /> '+folders_name+'</label><br/>')
                            }
                    }

                }
            }
        )
    });



    $('body').on('change','.select_folders',  function (event) {

        var valeurs = [];
        $('.select_folders').each(function() {

            if ($(this).is(":checked"))

                    {   let folder_id = $(this).val(); 
                        if (folder_id !="")
                            {valeurs.push(folder_id);}
                    }

        });

        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        url_ = "../ajax_charge_parcours" ;
        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'folder_ids': valeurs,                       
                    csrfmiddlewaretoken: csrf_token
                },
                url : url_,
                success: function (data) {

                    parcours = data["parcours"] ; 
                    $('#pclist').empty("");

                    if (parcours.length >0)
                    { for (let i = 0; i < parcours.length ; i++) {
                                
                                let parcours_id = parcours[i][0]; 
                                let parcours_name =  parcours[i][1] ; 

                                $('#pclist').append('<label for="cb'+Number(parcours_id)+'"><input type="checkbox" id="cb'+Number(parcours_id)+'" name="parcours" value="'+Number(parcours_id)+'" /> '+parcours_name+'</label><br/>')
                            }
                    }

                }
            }
        )
    });


 
 
    });
});