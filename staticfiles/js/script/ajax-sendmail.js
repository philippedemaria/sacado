define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-sendmail.js OK");


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




        $('#test_not_empty').on('click', function () {

            f1 = $('#id_groups').val();
            f2 = $('#id_receivers').val();
 
            if (f1.value == "" && f2.value == "") {
                alert('Vous devez choisir un destinataire');
                return false;
            }  
        });



    $('.response_call').on('click', function () { 
        $('#response').toggle(500);
            });



        // Ajoute ou supprime une pièce jointe
        $('#more_file').on('click', function () { 
            $("#file_attach").append('<input type="file" id="file_a" name="attachment" class="file_email btn btn-default btn-file" />');
        })
        $('#less_file').on('click', function () {
            $("#file_a").remove();
        })



        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.show_email').on('click', function (event) {
            let email_id = $(this).attr("data-email_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

 

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'email_id': email_id,
 
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax/show_email/",
                    success: function (data) {
                    $("#email_restitution").html("").append(data.html); 
                    }
                }
            )
        });




        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.show_com').on('click', function (event) {
            let communication_id = $(this).attr("data-communication_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

 

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'communication_id': communication_id,
 
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax/show_communication/",
                    success: function (data) {
                    $("#communication_restitution").html("").append(data.html); 
                    }
                }
            )
        });


        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.update_Com').on('click', function (event) {
            let communication_id = $(this).attr("data-communication_id");


            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'communication_id': communication_id,
                    },
                    url: "ajax/update_communication/",
                    success: function (data) {
                    $("#update_communication").html("").append(data.html); 
                    }
                }
            )
        });







    });
});