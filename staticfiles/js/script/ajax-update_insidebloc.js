define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-insidebloc.js OK");


            $(document).on('change', "#id_paragraph", function () {
 
                let id_paragraph = $("#id_paragraph").val();
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

                console.log(id_paragraph)

     
                $.ajax({
                    url: '../../../book/ajax_insidebloc',
                    type: "POST",
                    data: {
                        'id_paragraph': id_paragraph,
                        csrfmiddlewaretoken: csrf_token,    
                    },
                    dataType: 'json',
                    success: function (data) {

                        console.log(data)

                        blocs = data.blocs ; 
                        
                        if (blocs.length >0)
                        { for (let i = 0; i < blocs.length; i++) {
                                    
                                    let bloc_id = blocs[i][0];
                                    let bloc_name =  blocs[i][1]  ;
                                    let option = $("<option>", {
                                        'value': Number(bloc_id),
                                        'html': bloc_name
                                    });
                                    $('select[name=insidebloc]').append(option);
                                }
                        }
                        else
                        {
                                    let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                    });
                            $('select[name=insidebloc]').append(option);
                        }


                        
                    } 

                }); 

            });



            $(document).on('change', "#id_theme", function () {
 
                let id_theme = $("#id_theme").val();
                let id_level = $("#id_level").val();
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

                $.ajax({
                    url: '../../../book/ajax_knowledge_inbloc',
                    type: "POST",
                    data: {
                        'id_theme': id_theme,
                        'id_level': id_level,
                        csrfmiddlewaretoken: csrf_token,    
                    },
                    dataType: 'json',
                    success: function (data) {

                        knowledges = data.knowledges ; 
                        
                        if (knowledges.length >0)
                        { for (let i = 0; i < knowledges.length; i++) {
                                    
                                    let knowledge_id = knowledges[i][0];
                                    let knowledge_name =  knowledges[i][1]  ;
                                    let option = $("<option>", {
                                        'value': Number(knowledge_id),
                                        'html': knowledge_name
                                    });
                                    $('select[name=knowledge]').append(option);
                                }
                        }
                        else
                        {
                                    let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                    });
                            $('select[name=knowledge]').append(option);
                        }


                        
                    } 

                }); 

            });


  

    });

});

