define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
 
 console.log("ajax-associations chargé") ;

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.create_association').on('click', function (event) {

            let exercise_id = $(this).attr("data-exercise_id");
            let code = $("#create_code"+exercise_id).val();
            let action = $(this).attr("data-action");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            console.log(exercise_id+"----"+action+"----"+code);

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'code': code,
                        'exercise_id': exercise_id,
                        'action': action,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_update_association",
                    success: function (data) {

                        $("#row"+exercise_id).append(data.html) ;
                        $("#error_str"+exercise_id).html("").append(data.error) ;
                       
                    }
                }
            )
        });




        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.update_association').on('click', function (event) {

            let exercise_id = $(this).attr("data-exercise_id");
            let action = $(this).attr("data-action");
            let code = $("#update_code"+exercise_id).val();
                if (code == "") { alert("Vous devez renseigner le code d'un support."); return false; }                
                if (!confirm("Vous souhaitez modifier l'association avec ce support "+code+" ?")) return false; 
           

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            console.log(exercise_id+"----"+action+"----"+code);

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'code': code,
                        'exercise_id': exercise_id,
                        'action': action,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_update_association",
                    success: function (data) {

                        $("#association"+exercise_id).html("").append(data.html) ;
                        $("#error_str"+exercise_id).html("").append(data.error) ;

                    }
                }
            )
        });








        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.delete_association').on('click', function (event) {

            let exercise_id = $(this).attr("data-exercise_id");
            let action = $(this).attr("data-action");
            if (!confirm("Vous souhaitez supprimer l'association avec ce support ?")) return false;  
     
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();


            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'exercise_id': exercise_id,
                        'action': action,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_update_association",
                    success: function (data) {

                        $("#new_exercice"+exercise_id).remove() ;
                    }
                }
            )
        });

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.load_modal').on('click', function (event) {

            let exercise_id = $(this).data("exercise_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();


            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'exercise_id': exercise_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_load_modal",
                    success: function (data) {

                        $("#change_knowledge").html("").html(data.listing_w) ;
                    }
                }
            )
        });



        function sorter_exercises_from_admin($div_class , $exercise_class ) {

                $($div_class).sortable({
                    cursor: "move",
                    swap: true,    
                    animation: 150,
                    distance: 50,
                    revert: true,
                    tolerance: "pointer" , 
                    start: function( event, ui ) { 
                           $(ui.item).css("box-shadow", "10px 5px 10px gray"); 
                       },
                    stop: function (event, ui) {

 
                        var valeurs = "";
 

                        $($exercise_class).each(function() {
 
                            let div_exercise_id = $(this).find('input').val();
                            valeurs = valeurs + div_exercise_id +"-";
 
                        });

                        console.log(valeurs) ;
 

                        $(ui.item).css("box-shadow", "0px 0px 0px transparent");  

                        $.ajax({
                                data:   { 'valeurs': valeurs  } ,    
                                type: "POST",
                                dataType: "json",
                                url: "../ajax_sort_exercise_from_admin" 
                            }); 
                        }
                    });
                }

    
        sorter_exercises_from_admin(  '#exercise_ranking' ,".this_exercise");




        $('.input-sm').on('keyup', function (event) {  

            if ($('.input-sm').val() != "")
                { $("tr.opener_e").css("display","table-row")  ; } 
            else 
                { $("tr.opener_e").css("display","none")  ; } 

        });


 

        $('.opener_k').hide() ;
        $('.opener_e').hide() ;
 

        $('.opener').on('click' ,function () { 
            $('.opener_k').hide() ;

            if( $(this).hasClass("out") )
            {
                $(".opener ~ .opened"+this.id).show();
                $(this).removeClass("out").addClass("in");
                $(this).find('.fa').removeClass('fa-caret-right').addClass('fa-caret-down'); 
            }
            else 
            {
                $(".opener ~ .opened"+this.id).hide();  
                $(this).removeClass("in").addClass("out");
                $(this).find('.fa').removeClass('fa-caret-down').addClass('fa-caret-right');     
            }
 
        });



        $('.opener_k').on('click' ,function () { 
            $('.opener_e').hide() ;

            if( $(this).hasClass("out") )
                {
                $(".opener_k ~ .openedk"+this.id).show();
                $(this).removeClass("out").addClass("in");
                $(this).find('.fa').removeClass('fa-caret-right').addClass('fa-caret-down');
                }
            else 
            {
                $(".opener_k ~ .openedk"+this.id).hide();  
                $(this).removeClass("in").addClass("out");
                $(this).find('.fa').removeClass('fa-caret-down').addClass('fa-caret-right');            
            }
 
        });













 
    });
});