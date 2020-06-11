define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-parcours.js OK");

                $('[data-toggle="popover"]').popover() ;

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('select[name=level]').on('change', function (event) {
            let is_parcours = $("#is_parcours").val();
            let level_id = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if ( is_parcours == "1" ) 
                { 
                    var parcours_id = $("#id_parcours").val();  
                    url= "../../ajax_level_exercise" ; 
                } 
            else 
                {  var parcours_id = "0" ; 
                    url = "ajax_level_exercise";
                }



            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'parcours_id': parcours_id ,
                        'level_id': level_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: url,
                    success: function (data) {

                        container = $('#content_exercises');
                        
                        // Remplir la liste des choix avec le résultat de l'appel Ajax
                        container.html("");
                        for (let i = 0; i < data.length; i++) {

                            let exercise_id = data[i]['id'];
                            let knowledge =  data[i]['name'];
                            let checked =  data[i]['checked'];
                            let code =  data[i]['code'];
                            let option = $("<input />", {
                                'type': 'checkbox',
                                'name':  "exercises" ,
                                'checked':  checked  ,
                                'id':  exercise_id+"_exercise" ,
                                'value':  Number(exercise_id)
                            });
                            let label = $("<label />", {
                                'for':  exercise_id+"_exercise" ,
                                text: " "+knowledge+" ["+code+"]" 
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