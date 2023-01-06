define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-list_my_own_exercises.js OK");

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.subjects_levels').on('change', function (event) {

            $('#loading_spin').html("<div class='alert alert-info'><i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>  Recherche en cours</div>") ;

            let subject_ids = $('#id_subjects').val();            
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let skill_ids     = $('#id_skills').val();
            let level_ids     = $('#id_levels').val();
            let theme_ids     = $('#id_themes').val();
            let knowledge_ids = $('#id_knowledges').val();

            dataset = {csrfmiddlewaretoken: csrf_token }

            if (subject_ids){ dataset['subject_ids'] = subject_ids;  }
            if (level_ids)  { dataset['level_ids'] = level_ids ; }
            if (skill_ids){ dataset['skill_ids'] = skill_ids;  }
            if (theme_ids){ dataset['theme_ids'] = theme_ids;  }
            if (knowledge_ids){ dataset['knowledge_ids'] = knowledge_ids ; }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional : true,
                    data: dataset,
                    url: "ajax_customexercises_subjects_levels",
                    success: function (data) {

                        $('#loading_spin').html("") ;

                        $('select[name=themes]').html("");
                        // Remplir la liste des choix avec le résultat de l'appel Ajax
                        let themes = JSON.parse(data["themes"]);
                        for (let i = 0; i < themes.length; i++) {

                            let theme_id = themes[i].pk;
                            let name =  themes[i].fields['name'];
                            let option = $("<option>", {
                                'value': Number(theme_id),
                                'html': name
                            });
                            $('#id_themes').append(option);
                        } ;

                        $('select[name=skills]').html("");
                        // Remplir la liste des choix avec le résultat de l'appel Ajax
                        let skills = JSON.parse(data["skills"]);
                        for (let i = 0; i < skills.length; i++) {

                            let skill_id = skills[i].pk;
                            let name =  skills[i].fields['name'];
                            let option = $("<option>", {
                                'value': Number(skill_id),
                                'html': name
                            });
                            $('#id_skills').append(option);
                        };

                        $('select[name=knowledges]').html("");
                        // Remplir la liste des choix avec le résultat de l'appel Ajax
                        let knowledges = JSON.parse(data["knowledges"]);
                        for (let i = 0; i < knowledges.length; i++) {

                            let knowledge_id = knowledges[i].pk;
                            let name =  knowledges[i].fields['name'];
                            let option = $("<option>", {
                                'value': Number(knowledge_id),
                                'html': name
                            });
                            $('#id_knowledges').append(option);
                        }

                        $('#result_div').html("").html(data.customexercises);  
                    }
                }
            )
        });
 
        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_skills').on('change', function (event) {

            $('#loading_spin').html("<div class='alert alert-info'><i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>  Recherche en cours</div>") ;

            let subject_ids   = $('#id_subjects').val();            
            let csrf_token    = $("input[name='csrfmiddlewaretoken']").val();
            let skill_ids     = $('#id_skills').val();
            let level_ids     = $('#id_levels').val();
            let theme_ids     = $('#id_themes').val();
            let knowledge_ids = $('#id_knowledges').val();



            dataset = {csrfmiddlewaretoken: csrf_token }

            if (subject_ids){ dataset['subject_ids'] = subject_ids;  }
            if (level_ids)  { dataset['level_ids'] = level_ids ; }
            if (skill_ids){ dataset['skill_ids'] = skill_ids;  }
            if (theme_ids){ dataset['theme_ids'] = theme_ids;  }
            if (knowledge_ids){ dataset['knowledge_ids'] = knowledge_ids ; }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional : true,
                    data: dataset,
                    url: "ajax_customexercises_skills",
                    success: function (data) {

                        $('#loading_spin').html("") ;
                        $('#result_div').html("").html(data.customexercises);  
                    }
                }
            )
        });


        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_themes').on('change', function (event) {

            $('#loading_spin').html("<div class='alert alert-info'><i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>  Recherche en cours</div>") ;

            let subject_ids   = $('#id_subjects').val();            
            let csrf_token    = $("input[name='csrfmiddlewaretoken']").val();
            let skill_ids     = $('#id_skills').val();
            let level_ids     = $('#id_levels').val();
            let theme_ids     = $('#id_themes').val();
            let knowledge_ids = $('#id_knowledges').val();

            dataset = {csrfmiddlewaretoken: csrf_token }

            if (subject_ids){ dataset['subject_ids'] = subject_ids;  }
            if (level_ids)  { dataset['level_ids'] = level_ids ; }
            if (skill_ids){ dataset['skill_ids'] = skill_ids;  }
            if (theme_ids){ dataset['theme_ids'] = theme_ids;  }
            if (knowledge_ids){ dataset['knowledge_ids'] = knowledge_ids ; }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional : true,
                    data: dataset,
                    url: "ajax_customexercises_themes",
                    success: function (data) {

                        $('#result_div').html("").html(data.customexercises);  

                        if( data["knowledges"] )
                        {
                            $('select[name=knowledges]').html("");
                            // Remplir la liste des choix avec le résultat de l'appel Ajax
                            let knowledges = JSON.parse(data["knowledges"]);
                            for (let i = 0; i < knowledges.length; i++) {

                                let knowledge_id = knowledges[i].pk;
                                let name =  knowledges[i].fields['name'];
                                let option = $("<option>", {
                                    'value': Number(knowledge_id),
                                    'html': name
                                });
                                $('#id_knowledges').append(option);
                            }  
                        }


                        $('#loading_spin').html("") ;


                    }
                }
            )
        });



// Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_knowledges').on('change', function (event) {

            $('#loading_spin').html("<div class='alert alert-info'><i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>  Recherche en cours</div>") ;

            let subject_ids   = $('#id_subjects').val();            
            let csrf_token    = $("input[name='csrfmiddlewaretoken']").val();
            let skill_ids     = $('#id_skills').val();
            let level_ids     = $('#id_levels').val();
            let theme_ids     = $('#id_themes').val();
            let knowledge_ids = $('#id_knowledges').val();

            dataset = {csrfmiddlewaretoken: csrf_token }

            if (subject_ids){ dataset['subject_ids'] = subject_ids;  }
            if (level_ids)  { dataset['level_ids'] = level_ids ; }
            if (skill_ids){ dataset['skill_ids'] = skill_ids;  }
            if (theme_ids){ dataset['theme_ids'] = theme_ids;  }
            if (knowledge_ids){ dataset['knowledge_ids'] = knowledge_ids ; }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional : true,
                    data: dataset,
                    url: "ajax_customexercises_knowledges",
                    success: function (data) {

                        $('#loading_spin').html("") ;
                        $('#result_div').html("").html(data.customexercises);  

                    }
                }
            )
        });






        $(document).on('click', '.parcours_selector_support' , function (event) {
            let loop = $(this).data("loop") ;
            $("#parcours_div_support"+loop).toggle(500) ;
        })

        $(document).on('click', '.close_parcours_div_support' , function (event) {
            let loop = $(this).data("loop") ;
            $("#parcours_div_support"+loop).toggle(500) ;
        })


        $(document).on('click', '#show_exercises_search_div' , function (event) {
            $("#exercises_search_div").toggle(500) ;
        })


        //************************************************************************************
        //********** Depuis les pages my_own_exercises
        //************************************************************************************
        $(document).on('click', '.assign_exercise_to_parcours' , function (event) {

 
            let csrf_token   = $("input[name='csrfmiddlewaretoken']").val();
            let exercise_id  = $(this).data("exercise_id") ;
            let parcours_id  = $(this).data("parcours_id") ;
            let loop         = $(this).data("loop") ;
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'exercise_id': exercise_id,
                        'parcours_id': parcours_id,
                        'loop'       : loop,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_assign_exercise_to_parcours",
                    success: function (data) {

                        $("#parcours"+exercise_id+"-"+loop).removeClass('btn-default') ;
                        $("#parcours"+exercise_id+"-"+loop).addClass('btn-primary') ;
                        $("#assign_exercise_to_parcours"+exercise_id+"-"+loop).remove();

                    }
                }
            )
         });
        //====================================================================================
        //====================================================================================
        //====================================================================================












});

});

