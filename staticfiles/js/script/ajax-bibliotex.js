define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-bibiotex.js OK");

  
        $("#publication_div").hide();
 

            makeDivAppear($("#id_is_publish"), $("#publication_div"));


            function makeDivAppear($toggle, $item) {
                    $toggle.change(function () {
                         $item.toggle();
                    });
                }
 

        $('#enable_correction_div').hide();
        $("#enable_correction").click(function(){ 
            $('#enable_correction_div').toggle(500);
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
 



                    }
                }
            )
        });



        $('#id_level').on('change', function (event) {
            let id_level = $(this).val();
    
            if ((id_level == "")||(id_level == " ")) { alert("Sélectionner un niveau") ; return false ;}
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            url_ = "ajax_chargethemes" ;

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
            let bibliotex_id = $("#bibliotex_id").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            console.log(subject_id  ) ;
            url= "../ajax_level_exotex" ; 


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
                        'bibliotex_id': bibliotex_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: url,
                    success: function (data) {
 
                        $('#content_exercises').html("").html(data.html);
                        $("#loader").html(""); 
                        
                        }
                }
            )
        }






        $('.click_this_level').on('click', function (event) {

            let level_id = $(this).data("level_id");
            let subject_id = $(this).data("subject_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

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
                    url : "ajax_my_bibliotexs" ,
                    success: function (data) {

                        $("#my_biblio").html(data.html) ;

                    }
                }
            )


        });




    $('#id_skill').on('change', function (event) {

        let level_id = $("#id_level").val();
        let subject_id = $("#id_subject").val();
        let theme_id = $("#id_theme").val();
        let skill_id = $(this).val();
        let bibliotex_id = $("#bibliotex_id").val();
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 

        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'level_id'  : level_id,
                    'subject_id': subject_id,  
                    'skill_id'  : skill_id,   
                    'theme_id': theme_id, 
                    'bibliotex_id': bibliotex_id,
                    csrfmiddlewaretoken: csrf_token
                },
                url : "../ajax_level_exotex" ,
                success: function (data) {

                    $("#my_biblio").html(data.html) ;

                }
            }
        )
    });


    $('#keyword').on('keyup', function (event) {

        let level_id = $("id_level").val();
        let subject_id = $("id_subject").val();
        let skill_id =  $("#id_skill").val();
        let keyword = $(this).val();
        let theme_id = $("#id_theme").val();
        let bibliotex_id = $("#bibliotex_id").val();
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'level_id'  : level_id,
                    'subject_id': subject_id,  
                    'skill_id'  : skill_id,   
                    'keyword'   : keyword, 
                    'theme_id': theme_id,
                    'bibliotex_id': bibliotex_id,
                    csrfmiddlewaretoken: csrf_token
                },
                url : "../ajax_level_exotex" ,
                success: function (data) {

                    $("#my_biblio").html(data.html) ;

                }
            }
        )
    });

 
    $('body').on('click', '.action_print_tex' , function (event) {
            let relationtex_id = $(this).data("relationtex_id");
            let value = $("#tex_"+relationtex_id).html();
            $("#print_tex_body").html(value);

        });

 
    $('body').on('click', '.group_shower' , function (event) {
            let bibliotex_id = $(this).data("bibliotex_id");
            $("#group_show"+bibliotex_id).toggle(500);

        });


    $('body').on('click', '.bibliotex_shower' , function (event) {
            let bibliotex_id = $(this).data("bibliotex_id");
            $("#bibliotex_show"+bibliotex_id).toggle(500);

        });


 


    $('body').on('click', '.overlay_show' , function (event) {
            let bibliotex_id = $(this).data("bibliotex_id");
            $("#overlay_show"+bibliotex_id).toggle(500);

        });




        $('body').on('click', '.expand_video', function () {

            var exotex_id = $(this).data("exotex_id");  
            var content = $("#content"+exotex_id).html();
            var label = '<label for="customRange3" class="form-label">Taille de police</label><input type="range" value="3" class="form-range" min="3" max="5.5" step="0.5" id="customRange" style="width:200px">' ; 

            $("body").append('<div class="projection_div"  id="projection_div" style="font-size:3rem" ><span class="pull-right closer_projection_div" style="font-size:20px" ><i class="fa fa-times fa-2x"></i></span>'+label+'<hr/>'+content+'</div>'); 
       
            $(window).scrollTop(position);
        });


        $('body').on('click', ".closer_projection_div", function () {
             $("#projection_div").remove();
        });


        $('body').on('change', "#customRange", function (e) {
            size  = $("#customRange").val() ; 
            $("#projection_div").attr("style","font-size:"+size+"rem");
        });




    $('body').on('change', '.selector_exotex' , function (event) {

 
        let bibliotex_id = $("#bibliotex_id").val();
        let exotex_id = $(this).data("exotex_id");
        let statut = $(this).data("statut");
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'bibliotex_id': bibliotex_id, 
                    'exotex_id'   : exotex_id,
                    csrfmiddlewaretoken: csrf_token
                },
                url : "../ajax_set_exotex_in_bibliotex" ,
                success: function (data) {

                    $("#selected_exotex"+exotex_id).addClass(data.class) ;
                    $("#selected_exotex"+exotex_id).removeClass(data.noclass) ;
                    $("#selected_exotex"+exotex_id).attr("data-statut",data.statut) ;


                }
            }
        )
    });



    $('body').on('click', '.action_exotex',   function (event) {

        let relationtex_id = $(this).data("relationtex_id");
        let action = $(this).data("action");
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

        if (action == "print") { url = "../ajax_print_exotex" ; label ="print_exotex" ; }
        else if (action == "results") { url = "../ajax_results_exotex" ; label ="results_exotex" ;  }
        else if (action == "print_bibliotex") { url = "../ajax_print_bibliotex"  ; label ="print_bibliotex" ; }
        else if (action == "students") { url = "../ajax_individualise_exotex" ; label ="individualise_exotex" ;  }
        else if (action == "print_bibliotex_out") { url = "ajax_print_bibliotex"  ; label ="print_bibliotex" ; }
 

        $("#"+label+"_id").val(relationtex_id) ;

        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'relationtex_id'   : relationtex_id,
                    csrfmiddlewaretoken: csrf_token
                },
                url : url ,
                success: function (data) {
                    
                    $("#"+label+"_title").html(data.title) ;
                    $("#"+label+"_body").html(data.html) ;
                }
            }
        )
    });



    $('body').on('click', '.publisher',   function (event) {

 
        let bibliotex_id = $(this).data("bibliotex_id"); 
        let statut = $(this).data("statut");
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

        console.log(event , bibliotex_id , statut) ; 
 
        $.ajax(
            { 
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'bibliotex_id' : bibliotex_id,
                    'statut'       : statut,
                    csrfmiddlewaretoken: csrf_token
                },
                url : "ajax_publish_bibliotex" ,

                success: function (data) {
                    $('#publisher'+bibliotex_id).removeClass(data.noget).addClass(data.get);
                    $('#publisher'+bibliotex_id).attr("data-statut",data.statut);           
                    $('#accueil_visible'+bibliotex_id).html("").html(data.publish);
                    $('#bibliotex_publisher'+bibliotex_id).removeClass(data.noclass).addClass(data.class);
                    $('#accueil_text_color'+bibliotex_id).addClass(data.legendclass).removeClass(data.nolegendclass);
                    $('#disc'+bibliotex_id).attr("style",data.color).addClass(data.adddisc).removeClass(data.removedisc);


                }
            }
        )
    });





        function publisher_bibliotexs($actionner,$target,$targetStatut){

                $actionner.on('click', function (event) {
                    
                let bibliotex_id = $(this).attr("data-bibliotex_id");
                let statut = $(this).attr("data-statut");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'bibliotex_id': bibliotex_id,
                            'statut': statut,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: "ajax_publish_list_bibliotex" ,
                        success: function (data) {
                            $($target+bibliotex_id).attr("data-statut",data.statut);                  
                            $($targetStatut+bibliotex_id).removeClass(data.noclass);
                            $($targetStatut+bibliotex_id).addClass(data.class);
                            $($targetStatut+bibliotex_id).html("").html(data.label);
 

                        }  
                    })
                }); 
            } ;

        publisher_bibliotexs( $('.bibliotex_publisher') , '#bibliotex_publisher' ,'#bibliotex_statut' ) ;
 




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

                $(".subbibliotex"+target).toggle(500);

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




        $('.dataTables_wrapper').last().find('.col-sm-6').first().append("<h2 class='thin sacado_color_text'><i class='fa fa-th-list'></i> hors dossier </h2> ") ;

 



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

                        let bibliotex = $("#bibliotex").val();
                        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                        var relationtexs = [];
 

                        $($exercise_class).each(function() {

                            let relationtex_id = $(this).data("relationtex_id");
                            relationtexs.push(relationtex_id);
 
                        });

 
                        $(ui.item).css("box-shadow", "0px 0px 0px transparent"); 

                        console.log( 'relationtexs  ' + relationtexs +  '  bibliotex' + bibliotex )


                        $.ajax({
                                data:   { 'relationtexs': relationtexs ,  'bibliotex' : bibliotex , csrfmiddlewaretoken: csrf_token  } ,    
                                type: "POST",
                                dataType: "json",                
                                traditional: true,
                                url: "../ajax_sort_exotexs_in_bibliotex" 
                            }); 
                        }
                    });
                }

    
        sorter_exotexs('#bibliotex_sortable' , ".relationtex_sorter");

});

});

