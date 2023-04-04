define(['jquery',  'bootstrap',  'config_toggle'], function ($) {
    $(document).ready(function () {


    console.log(" ajax-mental chargé ");





    $('body').on('change','.onselect',  function (event) {


        let id_levels   = $("#id_levels").val();
        let id_subjects = $("#id_subjects").val();

        if ( (id_levels) && (id_subjects) )
        {
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val(); 

            url_ = "../ajax_charge_mentaltitle" ;
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'id_levels'  : id_levels, 
                        'id_subjects': id_subjects,                   
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : url_,
                    success: function (data) {

                        themes = data["themes"] ; 
                        $('select[name=mentaltitle]').empty("");
                        if (themes.length >0)
                        { for (let i = 0; i < themes.length; i++) { 
                                    
                                    let themes_id = themes[i][0];
                                    let themes_name =  themes[i][1]  ;
                                    let option = $("<option>", {
                                        'value': Number(themes_id),
                                        'html': themes_name
                                    });

                                $('select[name=mentaltitle]').append(option);    
                                }

                        }
                        else
                        {
                                    let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                    });
                            $('select[name=mentaltitle]').append(option);
                        }


                    }
                }
            )
        }
    });


 
 
    });
});