define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-flashpack.js OK");

  

        $("#show_answer").click(function(){ 
            $('#answer').toggle(500);
            $('#buttons').toggle(500);
            $('#offset').remove();
            $('#offsethelper').remove();
        });

        $("#show_helper").click(function(){ 
            $('#helper').toggle(500);
        });











        $('.select_all').on('change', function (event) {

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
 
                                    $('#cblist').append('<label for="cb'+Number(folders_id)+'"><input type="checkbox" id="cb'+Number(folders_id)+'" name="folders" value="'+Number(folders_id)+'" /> '+folders_name+'</label><br/>')
                                }
                        }
 



                    }
                }
            )
        });



 

});

});

