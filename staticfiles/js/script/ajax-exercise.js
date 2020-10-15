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
            let level_id = $('select[name=level]').val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'theme_id': theme_id,
                        'level_id': level_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_knowledge_exercice",
                    success: function (data) {
                        $('select[name=knowledge]').html("");
                        // Remplir la liste des choix avec le résultat de l'appel Ajax
                        let knowledges = JSON.parse(data["knowledges"]);
                        for (let i = 0; i < knowledges.length; i++) {

                            let knowledge_id = knowledges[i].pk;
                            let name =  knowledges[i].fields['name'];
                            let option = $("<option>", {
                                'value': Number(knowledge_id),
                                'html': name
                            });

                            $('#id_knowledge').append(option);
                        }
                    }
                }
            )
        });

 
            $(".setup_no_ggb").hide();
            makeItemAppear($("#id_is_ggbfile"), $(".setup_ggb"), $(".setup_no_ggb"));
            function makeItemAppear($toggle, $item, $itm) {
                    $toggle.change(function () {
                        if ($toggle.is(":checked")) {
                            $item.show(500);
                            $itm.hide(500);

                        } else {
                            $item.hide(500);
                            $itm.show(500);
                            }
                    });
                }





        $("#click_button").on('click', function () {

            if ($("#id_is_ggbfile").is(":checked")) {
                if ($("#id_ggbfile").val() == "") { alert("vous devez uploader un ficher GGB") ; return false ;}
            };
        });



        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.choose_student').on('click', function (event) {

            let relationship_id = $(this).attr("data-relationship_id");
            let student_id = $(this).attr("data-student_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'student_id': student_id,
                        'relationship_id': relationship_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax_choose_student",
                    success: function (data) {

                            $('#correction_div').html("").html(data.html);
                    }
                }
            )
         });








 
});

});

