define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-bibiotex.js OK");

 
        $('#id_level').on('change', function (event) {
            let id_level = $(this).val();
    
            if ((id_level == "")||(id_level == " ")) { alert("Sélectionner un niveau") ; return false ;}
            let id_subject = $("#id_subject").val();
            let bibliotex_id = $("#bibliotex_id").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            url_ = "../ajax_level_exotex" ;

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'level_id': id_level,
                        'subject_id': id_subject,
                        'bibliotex_id' : bibliotex_id,                        
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : url_,
                    success: function (data) {

                        if ((id_level==9)||(id_level==11)||(id_level==12))  { 
                            $("#is_annale").show(500);
                            $("#keyword_div").addClass("col-lg-2");
                            $("#keyword_div").removeClass("col-lg-3" );
                        }
                        else  { 
                            $("#is_annale").hide(500);
                            $("#keyword_div").addClass( "col-lg-3");
                            $("#keyword_div").removeClass("col-lg-2" );
                        }


                        $('#content_exercises').html(data.html);

                        themes = data["themes"] ; 
                        $('select[name=theme]').empty("");

                        if (themes.length >0)
                        { for (let i = 0; i < themes.length; i++) {
                                    
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



        $('#id_annale').on('change', function (event) {

             if ($(this).is(":checked"))

                {   
                    var is_annale =  'yes' ;
                }
                else
                {   
                    var is_annale =  'no' ;
                }

                let id_level = $("#id_level").val();
                if ((id_level == "")||(id_level == " ")) { alert("Sélectionner un niveau") ; return false ;}
                let id_subject = $("#id_subject").val();
                let bibliotex_id = $("#bibliotex_id").val();
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

                url_ = "../ajax_level_exotex" ;

                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        traditional: true,
                        data: {
                            'level_id'     : id_level,
                            'subject_id'   : id_subject,
                            'bibliotex_id' : bibliotex_id, 
                            'is_annale'    : is_annale ,                    
                            csrfmiddlewaretoken: csrf_token
                        },
                        url : url_,
                        success: function (data) {

                            $('#content_exercises').html(data.html);
                
                        }
                    })
        }); 

     
        function ajax_choice(param0, param1){

                let level_id = param0.val();
                let theme_id = param1.val();
                let bibliotex_id = $("#bibliotex_id").val();
                let subject_id = $("#id_subject").val();

                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

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


                            knowledges = data["knowledges"] ; 

                            if (knowledges.length >0)
                                {
                                $("#knowledges_div").show(500); 
                                $('select[name=knowledges]').empty("");

                                for (let i = 0; i < knowledges.length; i++) { 
                                            
                                            let knowledges_id = knowledges[i][0];
                                            let knowledges_name =  knowledges[i][1]  ;
                                            let option = $("<option>", {
                                                'value': Number(knowledges_id),
                                                'html': knowledges_name
                                            });
                                            $('select[name=knowledges]').append(option);
                                        }
                                }
                                else
                                {
                                            let option = $("<option>", {
                                                'value': 0,
                                                'html': "Aucun contenu disponible"
                                            });
                                    $('select[name=knowledges]').append(option);
                                    $("#knowledges_div").hide(500); 
                                }
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
                    url : "../ajax_my_bibliotexs" ,
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

                        $("#content_exercises").html(data.html) ;

                    }
                }
            )
        });


        $('#keyword').on('keyup', function (event) {

            let level_id = $("#id_level").val();
            let subject_id = $("#id_subject").val();
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

                        $("#content_exercises").html(data.html) ;

                    }
                }
            )
        });


        $('body').on('click', '.show_by_popup' , function (event) {
                let exotex_id = $(this).data("exotex_id");
                let value = $("#this_exotex"+exotex_id).html();
                $(".modal-body").html(value) ; 
            });


        $('body').on('click', '.group_shower' , function (event) {
                let bibliotex_id = $(this).data("bibliotex_id");
                $("#group_show"+bibliotex_id).toggle(500);

            });



        $('body').on('change', '.level_search' , function (event) {

            let level_id   = $("#level_id").val();
            let subject_id = $("#subject_id").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        traditional: true,
                        data: {
                            'level_id'     : level_id,
                            'subject_id'   : subject_id,               
                            csrfmiddlewaretoken: csrf_token
                        },
                        url : "../ajax_list_exotex",
                        success: function (data) {

                            $('#body_search_result').html(data.html);
                
                        }
                    }
                )
            });









        $('body').on('click', '.overlay_show' , function (event) {
                let bibliotex_id = $(this).data("bibliotex_id");
                $("#overlay_show"+bibliotex_id).toggle(500);

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
                        'statut'   : statut,
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

     
        $('#id_knowledges').on('change', function (event) {
                let id_level = $("#id_level").val();
        
                let skill_id =  $("#id_skill").val();
                let bibliotex_id = $("#bibliotex_id").val();
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                let keyword = $("#keyword").val();
                let knowledge_ids = $(this).val();

                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        traditional: true,
                        data: {
                            'skill_id'     : skill_id,
                            'bibliotex_id' : bibliotex_id,  
                            'keyword'      : keyword,     
                            'knowledge_ids': knowledge_ids,    
                            csrfmiddlewaretoken: csrf_token
                        },
                        url : "../ajax_knowledges_exotex" ,
                        success: function (data) {


                            if ((id_level==9)||(id_level==11)||(id_level==12))  { 
                                $("#is_annale").show(500);
                                $("#keyword_div").addClass("col-lg-2");
                                $("#keyword_div").removeClass("col-lg-3" );
                            }
                            else  { 
                                $("#is_annale").hide(500);
                                $("#keyword_div").addClass( "col-lg-3");
                                $("#keyword_div").removeClass("col-lg-2" );
                            }


                            $('#content_exercises').html(data.html);



                        }
                    }
                )
            });




        $('body').on('click' , '.opener' , function () { 
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



        $('body').on('click' , '.opener_k' , function () { 
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

