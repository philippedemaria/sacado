define(['jquery','bootstrap'], function ($) {
    $(document).ready(function () {

        console.log("chargement JS ajax-parcours.js OK");

        $(".is_evaluation").attr("checked",false);

        // ================================================================ 
        // Parcours menu vertical pour les cours
        var navItems = $('.admin-menu li > a');
        var navListItems = $('.admin-menu li');
        var allWells = $('.admin-content');
        var allWellsExceptFirst = $('.admin-content:not(:first)');
        allWellsExceptFirst.hide();
        navItems.click(function(e)
        {
            e.preventDefault();
            navListItems.removeClass('active');
            $(this).closest('li').addClass('active');
            
            allWells.hide();
            var target = $(this).attr('data-target-id');
            $('#' + target).show();
        });
        // ================================ FIN ============================ 

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_level').on('change', function (event) {

            let id_level = $(this).val();
            let id_parcours = $("#id_parcours").val();
            let type_of_document = $("#type_of_document").val();
            if ((id_level == "")||(id_level == " ")) { alert("Sélectionner un niveau") ; return false ;}
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if($("#loader")) {$("#loader").html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>");      }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'id_parcours': id_parcours ,
                        'id_level': id_level,
                        'id_subject': id_subject,

                        'type_of_document': type_of_document,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_find_peuplate_sequence" ,
                    success: function (data) {
 
                        $('#content_exercises').html("").html(data.html);
                        $("#loader").html(""); 
                        
                        }
                }
            )
        });





         





    });
});