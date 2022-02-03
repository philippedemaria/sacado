define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-flashpack.js OK");

        $("#publication_div").hide();
 

            makeDivAppear($("#id_is_publish"), $("#publication_div"));
            makeDivAppear($("#id_is_global"), $("#save_with_cards"));

 
            $("#id_is_global").change(function () {

                        $("#save_without_cards").toggleClass('btn-primary').toggleClass('btn-default');
                    });


            function makeDivAppear($toggle, $item) {
                    $toggle.change(function () {
                         $item.toggle();
                    });
                }
   
 


            $('body').on('change', '#id_subject' , function (event) {

         
                let id_subject = $("#id_subject").val();
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                url_ = "../../../tool/ajax_charge_groups" ;
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        traditional: true,
                        data: {
                            'id_subject': id_subject,                       
                            csrfmiddlewaretoken: csrf_token
                        },
                        url : url_,
                        success: function (data) {

                            groups = data["groups"] ; 
                            $('#grplist').empty("");

                            if (groups.length >0)
                            { for (let i = 0; i < groups.length ; i++) {
                                        
                                        let groups_id   = groups[i][0]; 
                                        let groups_name =  groups[i][1] ; 

                                        $('#grplist').append('<label for="cb'+Number(groups_id)+'"><input type="checkbox" id="cb'+Number(groups_id)+'" class="select_all" name="groups" value="'+Number(groups_id)+'" /> '+groups_name+'</label><br/>')
                                    }
                            }

                        }
                    }
                )
            });



        $('.select_all').on('change', function (event) {

            var valeurs = [];
            $(".select_all").each(function() {

                if ($(this).is(":checked"))

                        {   let group_id = $(this).val(); 
                            if (group_id !="")
                                {valeurs.push(group_id);}
                        }

            });

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            url_ = "../ajax_charge_folders" ;

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'group_ids': valeurs,                       
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : url_,
                    success: function (data) {

                        folders = data["folders"] ; 
                        $('#cblist').empty("");

                        if (folders.length >0)
                        { for (let i = 0; i < folders.length ; i++) {
                                    
                                    let folders_id = folders[i][0]; 
                                    let folders_name =  folders[i][1] ; 
 
                                    $('#cblist').append('<label for="cb'+Number(folders_id)+'"><input type="checkbox" id="cb'+Number(folders_id)+'" name="folders" value="'+Number(folders_id)+'" /> '+folders_name+'</label><br/>')
                                }
                        }

                        $('#id_themes_div').show();

                        themes = data["themes"] ; 
                        $('select[name=themes]').empty("");

                        if (themes.length >0)
                        { for (let i = 0; i < themes.length; i++) {
                                    

                                    console.log(themes[i]);
                                    let themes_id = themes[i][0];
                                    let themes_name =  themes[i][1]  ;
                                    let option = $("<option>", {
                                        'value': Number(themes_id),
                                        'html': themes_name
                                    });
                                    $('select[name=themes]').append(option);
                                }
                        }
                        else
                        {
                                    let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                    });
                            $('select[name=themes]').append(option);
                        }

                        $("#id_subject").val(data.subject);


                    }
                }
            )
        });



        $('#id_level').on('change', function (event) {
            let id_level = $(this).val();
    
            if ((id_level == "")||(id_level == " ")) { alert("Sélectionner un niveau") ; return false ;}
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            url_ = "../ajax_chargethemes" ;

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
                    url : url_,
                    success: function (data) {

                        themes = data["themes"] ; 
                        $('select[name=theme]').empty("");

                        if (themes.length >0)
                        { for (let i = 0; i < themes.length; i++) {
                                    

                                    console.log(themes[i]);
                                    let themes_id = themes[i][0];
                                    let themes_name =  themes[i][1]  ;
                                    let option = $("<option>", {
                                        'value': Number(themes_id),
                                        'html': themes_name
                                    });
                                    $('select[name=theme]').append(option);
                                }
                        }
                        else
                        {
                                    let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                    });
                            $('select[name=theme]').append(option);
                        }


                    }
                }
            )
        });
 


        $('#id_theme').on('change', function (event) {

            if (  $('select[name=level]').val() > 0 )
            {
                ajax_choice($('select[name=level]'),$('select[name=theme]')) ;            
            }
            else 
            {   
                alert("Vous devez choisir un niveau."); return false;             
            }
        }); 

 
        function ajax_choice(param0, param1){

            let level_id = param0.val();
            let theme_id = param1.val();
            let subject_id = $("#id_subject").val();
            let flashpack_id = $("#flashpack_id").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            console.log(subject_id  ) ;
            url= "../ajax_level_flashcard" ; 


            if($("#loader")) {$("#loader").html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>");      }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'level_id': level_id,
                        'theme_id': theme_id,
                        'subject_id': subject_id,
                        'flashpack_id': flashpack_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: url,
                    success: function (data) {
 
                        $('#content_cards').html("").html(data.html);
                        $("#loader").html(""); 
                        
                        }
                }
            )
        }






        $('.click_this_level').on('click', function (event) {

            let level_id = $(this).data("level_id");
            let subject_id = $(this).data("subject_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if($("#loader")) {$("#loader").html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>");      }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'level_id'  : level_id,
                        'subject_id': subject_id,                    
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "ajax_my_flashpacks" ,
                    success: function (data) {

 
                        $('#content_cards').html("").html(data.html);
                        $("#loader").html(""); 

                    }
                }
            )


        });




    $('#id_waiting').on('change', function (event) {

        let level_id = $("#id_level").val();
        let subject_id = $("#id_subject").val();
        let theme_id = $("#id_theme").val();
        let waiting_id = $(this).val();
        let flashpack_id = $("#flashpack_id").val();
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
        if($("#loader")) {$("#loader").html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>");      }

        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'level_id'  : level_id,
                    'subject_id': subject_id,  
                    'waiting_id'  : waiting_id,   
                    'theme_id': theme_id, 
                    'flashpack_id': flashpack_id,
                    csrfmiddlewaretoken: csrf_token
                },
                url : "../ajax_level_flashcard" ,
                success: function (data) {

                    $("#content_cards").html(data.html) ;
                    $("#loader").html(""); 

                }
            }
        )
    });


    $('#keyword').on('keyup', function (event) {

        let level_id = $("#id_level").val();
        let subject_id = $("#id_subject").val();
        let waiting_id =  $("#waiting_id").val();
        let keyword = $(this).val();
        let theme_id = $("#id_theme").val();
        let flashpack_id = $("#flashpack_id").val();
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

        if($("#loader")) {$("#loader").html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>");      }
        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'level_id'  : level_id,
                    'subject_id': subject_id,  
                    'waiting_id': waiting_id,   
                    'keyword'   : keyword, 
                    'theme_id': theme_id,
                    'flashpack_id': flashpack_id,
                    csrfmiddlewaretoken: csrf_token
                },
                url : "../ajax_level_flashcard" ,
                success: function (data) {

                    $("#content_cards").html(data.html) ;
                    $("#loader").html(""); 

                }
            }
        )
    });




    $('body').on('click', '.get_flashcard' , function (event) {

 
        let flashpack_id = $("#flashpack_id").val();
        let flashcard_id = $(this).data("flashcard_id");
        let statut = $(this).data("statut");   
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();



        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'flashpack_id' : flashpack_id, 
                    'flashcard_id' : flashcard_id,
                    'statut'       : statut,
                    csrfmiddlewaretoken: csrf_token
                },
                url : "../ajax_set_flashcard_in_flashpack" ,
                success: function (data) {


                    $("#selected_flashcard"+flashcard_id).addClass(data.class) ;
                    $("#selected_flashcard"+flashcard_id).removeClass(data.noclass) ;
                    $("#selected_flashcard"+flashcard_id).attr("data-statut",data.statut) ;

                }
            }
        )
    });



    $('body').on('click', '.bottom_flashcard',   function (event) { 


        let flashcard_id = $(this).data("flashcard_id");
        let statut = $(this).data("statut");

 
        if (statut == "show_answer") {  $("#answer"+flashcard_id).removeClass("no_visu_onload"); $("#answer"+flashcard_id).toggle(500);$("#helper"+flashcard_id).hide(500);  }
        if (statut == "show_helper") {  $("#helper"+flashcard_id).removeClass("no_visu_onload"); $("#helper"+flashcard_id).toggle(500);$("#answer"+flashcard_id).hide(500);  }
       
    });



    $('body').on('click', '.publisher',   function (event) {

 
        let flashpack_id = $(this).data("flashpack_id"); 
        let statut = $(this).data("statut");
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

        console.log(event , flashpack_id , statut) ; 
 
        $.ajax(
            { 
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'flashpack_id' : flashpack_id,
                    'statut'       : statut,
                    csrfmiddlewaretoken: csrf_token
                },
                url : "ajax_publish_flashpack" ,

                success: function (data) {
                    $('#publisher'+flashpack_id).removeClass(data.noget).addClass(data.get);
                    $('#publisher'+flashpack_id).attr("data-statut",data.statut);           
                    $('#accueil_visible'+flashpack_id).html("").html(data.publish);
                    $('#flashpack_publisher'+flashpack_id).removeClass(data.noclass).addClass(data.class);
                    $('#accueil_text_color'+flashpack_id).addClass(data.legendclass).removeClass(data.nolegendclass);
                    $('#disc'+flashpack_id).attr("style",data.color).addClass(data.adddisc).removeClass(data.removedisc);


                }
            }
        )
    });





        function publisher_flashpacks($actionner,$target,$targetStatut){

                $actionner.on('click', function (event) {
                    
                let flashpack_id = $(this).attr("data-flashpack_id");
                let statut = $(this).attr("data-statut");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'flashpack_id': flashpack_id,
                            'statut': statut,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: "ajax_publish_list_flashpack" ,
                        success: function (data) {
                            $($target+flashpack_id).attr("data-statut",data.statut);                  
                            $($targetStatut+flashpack_id).removeClass(data.noclass);
                            $($targetStatut+flashpack_id).addClass(data.class);
                            $($targetStatut+flashpack_id).html("").html(data.label);
 

                        }  
                    })
                }); 
            } ;

        publisher_flashpacks( $('.flashpack_publisher') , '#flashpack_publisher' ,'#flashpack_statut' ) ;
 




        // ===============================================================
        // ===============================================================
        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.select_student').on('click' ,  function () {

            let relationtex_id = $(this).attr("data-relationtex_id"); 
            let statut = $(this).attr("data-statut"); 
            let student_id = $(this).attr("data-student_id");

            let is_checked = false ;
            if ($("#select_all_exercices").val()) { 
                is_checked = $("#select_all_exercices").is(":checked") ;
            }
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            

            $("#loading"+relationtex_id).html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>"); 
 



            $.ajax( 
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'relationtex_id': relationtex_id,
                        'student_id'    : student_id,
                        'statut'        : statut,
                        'is_checked'    : is_checked ,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../ajax_individualise",
                    success: function (data) {

                        if (is_checked)
                            {
                                if (student_id == 0)
                                    {  

                                    $('.select_student' ).attr("data-statut",data.statut);                  
                                    $('.select_student' ).removeClass(data.noclass);
                                    $('.select_student' ).addClass(data.class);
                                    }
                                else 
                                    { 
                                    $('.selected_studentExo'+student_id).html(data.html);   
                                    $('.selected_studentExo'+student_id).attr("data-statut",data.statut);                  
                                    $('.selected_studentExo'+student_id).removeClass(data.noclass);
                                    $('.selected_studentExo'+student_id).addClass(data.class);                      
                                    }

                                if (data.indiv_hide) 
                                    { $('#individialise_id_student'+relationtex_id).removeClass("checkbox_no_display");
                                      $('#nb_indiv_id_student'+relationtex_id).html("").html(data.indiv_nb);
                                    }
                                else{
                                    { $('#individialise_id_student'+relationtex_id).addClass("checkbox_no_display");}
                                }

                                $("#loading"+relationtex_id).html("");  
                                $('#selecteur'+relationtex_id).attr("data-statut",data.statut);    
                            }
                        else
                            {
     
                                if (student_id != 0)
                                    {       

                                    $('#student'+relationtex_id+"-"+student_id).attr("data-statut",data.statut);                  
                                    $('#student'+relationtex_id+"-"+student_id).removeClass(data.noclass);
                                    $('#student'+relationtex_id+"-"+student_id).addClass(data.class);
                                    }
                                else 
                                    { 

                                    $('.selected_student'+relationtex_id).attr("data-statut",data.statut);                  
                                    $('.selected_student'+relationtex_id).removeClass(data.noclass);
                                    $('.selected_student'+relationtex_id).addClass(data.class);                      
                                    }

                                if (data.indiv_hide) 
                                    { 
                                        $('#individialise_id_student'+relationtex_id).removeClass("checkbox_no_display");
                                        $('#nb_indiv_id_student'+relationtex_id).html("").html(data.indiv_nb); 
                                    }
                                else{
                                    { $('#individialise_id_student'+relationtex_id).addClass("checkbox_no_display");}
                                }

                                $("#loading"+relationtex_id).html("");  
                                $('#selecteur'+relationtex_id).attr("data-statut",data.statut);    

                            }
                        if (data.alert){ alert("Certains exercices ont fait l'objet d'une réponse par certains élèves. Vous ne pouvez plus les dissocier.");}
                        }
                })
        });







            $('.collapsed').hide() ;
            collapser = 0 ;
            $('.accordion').on('click', function (event) {

                let target = $(this).attr("data-target");

                $(".subflashpack"+target).toggle(500);

                if (collapser %2 == 0) 
                    { 
                        $("#pop"+target).removeClass('fa-chevron-down').addClass('fa-chevron-up');

                        $(".selected_tr").addClass('no_visu_on_load');
                        $("#tr"+target).removeClass('no_visu_on_load').addClass('bg_violet');
                    } 
                else 
                    {
                        $("#pop"+target).removeClass('fa-chevron-up').addClass('fa-chevron-down');

                        $(".selected_tr").removeClass('no_visu_on_load');
                        $("#tr"+target).removeClass('bg_violet');

                    }
                collapser++;                     
             }) ;



        $('.dataTables_wrapper').last().find('.col-sm-6').first().append("<h2 class='thin sacado_color_text'><i class='bi bi-stack'></i> hors dossier </h2> ") ;

 
        // Met en favori un parcours
        $('.selector_favorite').on('click' ,function () {
            let target_id = $(this).attr("data-target_id"); 
            let statut = $(this).attr("data-fav"); 
            let status = $(this).attr("data-status"); 

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'target_id': target_id,
                        'statut': statut,
                        'status': status,

                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_is_favorite",
                    success: function (data) {
                        $('#is_favorite_id'+target_id).html(data.statut);
                        $('#selector_favorite'+target_id).attr("data-fav",data.fav);      
                    }
                }
            )
        });



    $('body').on('change', '.select_all' , function (event) {

        var valeurs = [];
        $(".select_all").each(function() {

            if ($(this).is(":checked"))

                    {   let group_id = $(this).val(); 
                        if (group_id !="")
                            {valeurs.push(group_id);}
                    }

        });

        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        url_ = "../ajax_charge_folders" ;
        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'group_ids': valeurs,                       
                    csrfmiddlewaretoken: csrf_token
                },
                url : url_,
                success: function (data) {

                    folders = data["folders"] ; 
                    $('#cblist').empty("");

                    if (folders.length >0)
                    { for (let i = 0; i < folders.length ; i++) {
                                
                                let folders_id = folders[i][0]; 
                                let folders_name =  folders[i][1] ; 

                                $('#cblist').append('<label for="cb'+Number(folders_id)+'"><input type="checkbox" id="cb'+Number(folders_id)+'" class="select_folders" name="folders" value="'+Number(folders_id)+'" /> '+folders_name+'</label><br/>')
                            }
                    }



                    parcours = data["parcours"] ; 
                    $('#pclist').empty("");

                    if (parcours.length >0)
                    { for (let i = 0; i < parcours.length ; i++) {
                                
                                let parcours_id = parcours[i][0]; 
                                let parcours_name =  parcours[i][1] ; 

                                $('#pclist').append('<label for="cb'+Number(parcours_id)+'"><input type="checkbox" id="cb'+Number(parcours_id)+'" name="parcours" value="'+Number(parcours_id)+'" /> '+parcours_name+'</label><br/>')
                            }
                    }



                    

                }
            }
        )
    });



    $('body').on('change','.select_folders',  function (event) {

        var valeurs = [];
        $('.select_folders').each(function() {

            if ($(this).is(":checked"))

                    {   let folder_id = $(this).val(); 
                        if (folder_id !="")
                            {valeurs.push(folder_id);}
                    }

        });

        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        url_ = "../ajax_charge_parcours" ;
        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'folder_ids': valeurs,                       
                    csrfmiddlewaretoken: csrf_token
                },
                url : url_,
                success: function (data) {

                    parcours = data["parcours"] ; 
                    $('#pclist').empty("");

                    if (parcours.length >0)
                    { for (let i = 0; i < parcours.length ; i++) {
                                
                                let parcours_id = parcours[i][0]; 
                                let parcours_name =  parcours[i][1] ; 

                                $('#pclist').append('<label for="cb'+Number(parcours_id)+'"><input type="checkbox" id="cb'+Number(parcours_id)+'" name="parcours" value="'+Number(parcours_id)+'" /> '+parcours_name+'</label><br/>')
                            }
                    }

                }
            }
        )
    });

        function sorter_exotexs($div_class , $exercise_class ) {

                $($div_class).sortable({
                    cursor: "move",
                    swap: true,    
                    animation: 150,
                    distance: 10,
                    revert: true,
                    tolerance: "pointer" , 
                    start: function( event, ui ) { 
                           $(ui.item).css("box-shadow", "10px 5px 10px gray"); 
                       },
                    stop: function (event, ui) {

                        let flashpack = $("#flashpack").val();
                        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                        var relationtexs = [];
 

                        $($exercise_class).each(function() {

                            let relationtex_id = $(this).data("relationtex_id");
                            relationtexs.push(relationtex_id);
 
                        });

 
                        $(ui.item).css("box-shadow", "0px 0px 0px transparent"); 

                        console.log( 'relationtexs  ' + relationtexs +  '  flashpack' + flashpack )


                        $.ajax({
                                data:   { 'relationtexs': relationtexs ,  'flashpack' : flashpack , csrfmiddlewaretoken: csrf_token  } ,    
                                type: "POST",
                                dataType: "json",                
                                traditional: true,
                                url: "../ajax_sort_exotexs_in_flashpack" 
                            }); 
                        }
                    });
                }

    
        sorter_exotexs('#flashpack_sortable' , ".relationtex_sorter");

});

});

