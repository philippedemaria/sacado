define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-school.js OK");

        

 




        $("input:checkbox.select_radio").on('click', function (event) {

            let counter = $(this).attr("data-counter");

            $("input:checkbox.choice"+counter).not($(this)).removeAttr("checked");

            $(this).attr("checked", $(this).attr("checked"));    

        });





 

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('select[name=subject]').on('change', function (event) {
            let subject_id = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'subject_id': subject_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_subject_teacher",
                    success: function (data) {
                        $('select[name=teacher]').html("");
                        // Remplir la liste des choix avec le résultat de l'appel Ajax
                        teachers = data["teachers"]
                        for (let i = 0; i < teachers.length; i++) {

                            let teacher_id = teachers[i][0];
                            let name =  teachers[i][1];                
                            let option = $("<option>", {
                                'value': Number(teacher_id),
                                'html': name
                            });
                            $('#id_teacher').append(option);
                        }
                    }
                }
            )
        }); 






    });
 
});

