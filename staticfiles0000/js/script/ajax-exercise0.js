define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-exercise.js OK");

 

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('select[name=level]').on('change', function (event) {
            let level_id = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'level_id': level_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_theme_exercice",
                    success: function (data) {
                        $('select[name=theme]').html("");
                        // Remplir la liste des choix avec le résultat de l'appel Ajax
                        let themes = JSON.parse(data["themes"]);
                        for (let i = 0; i < themes.length; i++) {

                            let theme_id = themes[i].pk;
                            let name =  themes[i].fields['name'];
                            let option = $("<option>", {
                                'value': Number(theme_id),
                                'html': name
                            });

                            $('#id_theme').append(option);
                        }
                    }
                }
            )
        }); 
 
   
        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('select[name=theme]').on('change', function (event) {
            let theme_id = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'theme_id': theme_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_knowledge_exercice",
                    success: function (data) {
                        $('select[name=knowledge]').html("");
                        $('#content_knowledges').html("");
                        // Remplir la liste des choix avec le résultat de l'appel Ajax
                        container = $('#content_knowledges');
                        for (let i = 0; i < data.length; i++) {

                            let knowledge_id = data[i]['id'];
                            let knowledge =  data[i]['name'];
                            let nb =  data[i]['nb'];
                            let option = $("<input />", {
                                'type': 'radio',
                                'name':  "knowledge" ,

                                'id':  "id_knowledge_"+i ,
                                'value':  Number(knowledge_id)
                            });
                            let label = $("<label />", {
                                'for':  "id_knowledge_"+i ,
                                text: "  "+knowledge + "  ---> "+nb+ " exercice.s proposé.s" 
                            });


                            option.appendTo(container);
                            label.appendTo(container);
                            container.append("<br/>");

 
                        }
                    }
                }
            )
        });


    });
});