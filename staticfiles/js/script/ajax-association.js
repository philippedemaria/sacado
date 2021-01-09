define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-association.js OK");

    
        
        $("#existing_user").hide();
        $("#extra_member").hide();

        $("#type_of_member0").on('change', function (event) {
                $("#existing_user").show();
                $("#extra_member").hide();
        }); 

        $("#type_of_member1").on('change', function (event) {
                $("#existing_user").hide();
                $("#extra_member").show();
        }); 


        // Affiche dans la modal la liste des élèves du groupe sélectionné
        // $('select[name=level]').on('change', function (event) {
        //     let level_id = $(this).val();
        //     let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
        //     $.ajax(
        //         {
        //             type: "POST",
        //             dataType: "json",
        //             data: {
        //                 'level_id': level_id,
        //                 csrfmiddlewaretoken: csrf_token
        //             },
        //             url: "ajax_theme_exercice",
        //             success: function (data) {
        //                 $('select[name=theme]').html("");
        //                 // Remplir la liste des choix avec le résultat de l'appel Ajax
        //                 let themes = JSON.parse(data["themes"]);
        //                 for (let i = 0; i < themes.length; i++) {

        //                     let theme_id = themes[i].pk;
        //                     let name =  themes[i].fields['name'];
        //                     let option = $("<option>", {
        //                         'value': Number(theme_id),
        //                         'html': name
        //                     });

        //                     $('#id_theme').append(option);
        //                 }
        //             }
        //         }
        //     )
        // }); 
  


});

});

