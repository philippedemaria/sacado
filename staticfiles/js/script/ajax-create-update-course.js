define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-create-update-course.js OK");

 



        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_level').on('change', function (event) {
            let id_level = $(this).val();
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $("#loading").html("<i class='fa fa-spinner fa-pulse fa-fw'></i>");
            $("#loading").show(); 

            if (id_subject > 0)
            {
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
                        url : "../ajax_course_charge_parcours",
                        success: function (data) {

                            console.log(data.parcours) ;

                            parcours = data["parcours"]
                            $('select[name=parcours]').empty("");
                            if (parcours.length >0)

                            { for (let i = 0; i < parcours.length; i++) {
                                        
                                        let parcours_id = parcours[i][0];
                                        let parcours_name =  parcours[i][1]  ;
                                        let option = $("<option>", {
                                            'value': Number(parcours_id),
                                            'html': parcours_name
                                        });
                                        console.log(option);
                                        $('select[name=parcours]').append(option);
                                    }
                            }
                            else
                            {
                                        let option = $("<option>", {
                                            'value': 0,
                                            'html': "Aucun contenu disponible"
                                        });
                                $('select[name=parcours]').append(option);
                            }

                            $("#loading").html("").hide(500); 
                        }
                    }
                )                
            }

        });
 

 
 
 
    });

});

