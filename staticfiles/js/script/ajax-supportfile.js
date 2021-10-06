define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-supportfile.js OK --");

         
 



        $('.input-sm').on('keyup', function (event) {  

            if ($('.input-sm').val() != "")
                { $("tr.opener_e").css("display","table-row")  ; } 
            else 
                { $("tr.opener_e").css("display","none")  ; } 

        });


        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.selector_e').on('click' ,function () {

            let parcours_id = $(this).attr("data-parcours_id"); 
            let exercise_id = $(this).attr("data-exercise_id"); 
            let statut = $(this).attr("data-statut"); 
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'parcours_id': parcours_id,
                        'exercise_id': exercise_id,
                        'statut': statut,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../ajax_populate",
                    success: function (data) {
                        if (data.no_store) { alert("Vous ne pouvez pas enregistrer cet exercice. Cet exercice est déjà dans ce parcours.")}
                            else
                            {
                                $('#is_selected'+exercise_id).html(data.html);   
                                $('#selector_e'+exercise_id).attr("data-statut",data.statut);                  
                                $('#selector_e'+exercise_id).removeClass(data.noclass);
                                $('#selector_e'+exercise_id).addClass(data.class);
                                $('#selector_e'+exercise_id).focus();
                            }
                    }
                }
            )
        });

        $('.selector_m').on('click' ,function () {

            let relationship_id = $("#relationship").val(); 
            let exercise_id = $(this).attr("data-exercise_id"); 
            let statut = $(this).attr("data-statut"); 
            let scale = $("#id_scale").val(); 
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'relationship_id': relationship_id,
                            'exercise_id': exercise_id,
                            'scale': scale,     
                            'statut': statut,
                        },
                        url: "../../ajax_populate_mastering",
                        success: function (data) {

                            if (data.no_store) { alert("Vous ne pouvez pas enregistrer cet exercice. Cet exercice est déjà dans ce parcours.")}
                                else
                                { 
                                    $('#is_selected'+exercise_id).html(data.html);   
                                    $('#selector_e'+exercise_id).attr("data-statut",data.statut);                  
                                    $('#selector_e'+exercise_id).removeClass(data.noclass);
                                    $('#selector_e'+exercise_id).addClass(data.class);
                                    if(data.statut == "True") 
                                        { $("#selector_e"+exercise_id).attr('checked', true);  } 
                                    else { $("#selector_e"+exercise_id).attr('checked', false);  }
                                }

                            

                        }
                    }
                )
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
 


        function sorter_supportfiles($div_class , $exercise_class ) {

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
                                url: "../ajax/sort_supportfile" 
                            }); 
                        }
                    });
                }

    
        sorter_supportfiles(  '#supportfile_ranking' ,".this_supportfile");
        
 
 



    });
});