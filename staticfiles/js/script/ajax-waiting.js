define(['jquery','bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-waiting.js OK");
 
        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_theme').on('change', function (event) {
            let id_theme = $(this).val();
            let id_level = $("#id_level").val();
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
                    url : "../../ajax/chargewaitings",
                    success: function (data) {

                        waitings = data["waitings"]
                        $('select[name=waiting]').empty("");
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
 
 

        
    });
});