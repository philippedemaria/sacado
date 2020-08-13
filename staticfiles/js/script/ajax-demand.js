define(['jquery','bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-parcours.js OK");


        // ================================ FIN ============================ 

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_level').on('change', function (event) {
            let id_level = $(this).val();
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            console.log(id_level) ; 
            console.log(id_subject) ;

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
                    url : "ajax/chargethemes",
                    success: function (data) {

                        themes = data["themes"]
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
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'id_theme': id_theme,                      
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "ajax/chargeknowledges",
                    success: function (data) {

                        knowledges = data["knowledges"]
                        $('select[name=knowledge]').empty("");
                        if (knowledges.length >0)
                        { 
                            for (let i = 0; i < knowledges.length; i++) {
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


 


 
        $('.select_done').on('click', function (event) {
            let id = $(this).attr("data-id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let code = $("#code"+id).val();


            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'id': id,
                        'code': code,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax/demand_done",
                    success: function (data) {

                       $("#tr"+id).css("background","#e6e2dd") ;
 
                    }
                }
            )
        });









       

    });
});