define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-book.js OK");
 

        $(".get_the_title").on('click', function (event) {
            let title = $(this).data("title");
            $("#new_chapter  #rename_chapter").val(title);
            $("#is_update").val(1);
            $("#pk_chapter_id").val( $(this).data("chapter_id") );
        }); 



        $(document).on('click', "#submit_add_chapter" , function (event) {

            var pk_book_id      = $(this).data('book_id');
            var name_chapter     = $("#add_chapter").val();
 
 
            var csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax({
                    data: { 
                        'book_id': pk_book_id,
                        'name_chapter': name_chapter ,
                        'csrf_token': csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../ajax_add_chapter" ,
                    traditional: true,
                    success: function (data) {

                        $("#droppable_sommary").append(data.html);
                        $('#book_add_new_chapter').modal('hide');
   
                    }
                }); 
        }); 






        $(document).on('click', "#submit_rename_parcours" , function (event) {

            var pk_chapter_id      = $("#pk_chapter_id").val();
            var rename_chapter     = $("#rename_chapter").val();

            if ($("#is_rename_parcours").is(":checked")){
                var is_rename_parcours = "yes";
            } else {
                var is_rename_parcours = "no";
            }
        
            var csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax({
                    data: { 
                        'chapter_id': pk_chapter_id ,
                        'rename_chapter': rename_chapter ,
                        'is_rename_parcours': is_rename_parcours ,

                        'csrf_token': csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../ajax_rename_chapter" ,
                    traditional: true,
                    success: function (data) {

                        $("#this_parcours_title"+pk_chapter_id).text(data.html);
                        $('#book_new_chapter').modal('hide');
                    }
                }); 
        }); 












        $(document).on('click', ".get_inside_chapter_div" , function (event) {

            var book_id    = $(this).data("book_id");
            var chapter_id = $(this).data("chapter_id");
            var csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax({
                    data: { 
                        'book_id': book_id ,
                        'chapter_id': chapter_id ,
                        'csrf_token': csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../get_inside_chapter_div" ,
                    traditional: true,
                    success: function (data) {

                        $("#dropzone").html(data.html);
                        $(".book_chapters_in_menu").removeClass("book_chapters_in_menu_selected");
                        $("#chapter"+chapter_id).addClass("book_chapters_in_menu_selected");
                        $(".get_inside_chapter_div").removeClass("color_white");
                        $("#this_parcours_title"+chapter_id).addClass("color_white");

                    }
                }); 
        }); 






        function sorter_chapter($div_class , $exercise_class ) {

            $($div_class).sortable({
            	placeholder: "book_chapter_high_light_sorter", 
            	axis: 'y' ,
                start: function( event, ui ) { 
                       $(ui.item).css("background-color", "gray");
                   }, 
                stop: function (event, ui) {

                    var valeurs = [];

                    $($exercise_class ).each(function() {
                        let chapter_id = $(this).attr("data-chapter_id"); 
                        valeurs.push(chapter_id);
                    });

                    $(ui.item).css("background-color", "transparent");

    
                    this_url =  "../../sorter_book_chapter"  ;                   
  
                    $.ajax({
                            data:   { 'valeurs': valeurs    } ,   
                            type: "POST",
                            dataType: "json",
                            url: this_url,
                            traditional: true,
							success: function (data) {

							 	var n = 1 ;
								$(".book_chapter_number").each(function() {
								        $(this).text(n+". "); n++; 
								    });
							    }
                        }); 
                    }
                });

            }

        sorter_chapter('#droppable_sommary',".sorter_chapter") ;



  
        $("#collapse_menu_button").on('click', function (event) {


        	if ($("#sort_chapter").hasClass("summary_collapse")){ 

             	$("#book_all_main_page").removeClass("book_main_page_uncollapse");

            	$("#collapse_menu_button").html("<i class='bi bi-box-arrow-in-left'></i>");

			  	$("#sort_chapter" ).removeClass('summary_collapse') ;
                $("#id_book_main_page" ).removeClass('book_main_page_expand');

        	} else{

			  	$("#sort_chapter" ).addClass('summary_collapse');

			  	$("#book_all_main_page" ).addClass('book_main_page_uncollapse');

            	$("#collapse_menu_button").html("<i class='bi bi-box-arrow-right'></i>");

                $("#id_book_main_page" ).addClass('book_main_page_expand');



        	} 

        });

 


        $(document).on('click', ".ajax_delete_chapter" , function (event) {

			if (confirm('Êtes-vous sûr de vouloir supprimer ce chapitre ?')) {

            var chapter_id = $(this).data("chapter_id");
            var csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax({
                    data: { 
                    	'chapter_id': chapter_id ,  
                    	'csrf_token': csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../ajax_delete_chapter" ,
                    traditional: true,
					success: function (data) {

						$("#chapter"+chapter_id).remove();
					}
                }); 
        	}
        }); 

 

        function sorter_document( document_id ,  section_id ) {

            $(".book_main_page_section").sortable({ 
            	connectWith: ".book_main_page_section" , 
            	items      : ".book_main_page_section_document_detail" , 

                start: function( event, ui ) { 
                       $(ui.item).css("background-color", "#F7F7F7");
                   }, 
                stop: function (event, ui) {

                	var over_section_id = $(ui.item).parent().data("over_section_id");  

                    var valeurs = [];
                    $( ".book_main_page_section_document_detail" ).each(function() {
                        let doc_id = $(this).data("document_id"); 
                        valeurs.push(doc_id);
                    });

                    $(ui.item).css("background-color", "transparent");

                    this_url =  "../../../book/sorter_book_document"  ;  

                    $.ajax({
                            data:   { 
                            	'valeurs': valeurs  , 
                            	'over_section_id' : over_section_id ,  
                            	'section_id': section_id,
                            	'document_id' : document_id , 
                            	} ,   
                            type: "POST",
                            dataType: "json",
                            url: this_url,
                            traditional: true,
							success: function (data) {
								$("#this_document"+document_id).attr('data-section_id',data.section_id);
							}
                        }); 
                    }
                });
            }




        $(document).on('mousedown', ".book_main_page_section_document_detail" , function (event) {

            var section_id  = $(this).data("section_id");
            var document_id = $(this).data("document_id");
        	sorter_document(document_id , section_id) ;

        })







 

            $("#dropzone_chrono_concept").sortable({ 
                distance : 10,
                start: function( event, ui ) { 
                       $(ui.item).css("background-color", "#F7F7F7");
                   }, 
                stop: function (event, ui) {
                    var valeurs = [];
                    $( ".book_main_page_section_document_type" ).each(function() {
                        let doc_id = $(this).data("document_id"); 
                        valeurs.push(doc_id);
                    });

                    $(ui.item).css("background-color", "white");

                    this_url =  "../../sorter_book_chrono_document"  ;  

                    $.ajax({
                            data:   { 
                                'valeurs': valeurs  , 
                                 } ,   
                            type: "POST",
                            dataType: "json",
                            url: this_url,
                            traditional: true,
                            success: function (data) {
                                var i = 1;
                                $(".forlooper").each(function() {
                                     $(this).html(i); 
                                     i++;

                                });
                            }

                        }); 
                    }
                }) 



        $(document).on('click', ".show_this_document" ,  function (event) {

            let document_id = $(this).data("document_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();


            $.ajax({
                    data: { 
                    	'document_id': document_id ,  
                    	'csrf_token': csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../../book/show_book_document" ,
                    traditional: true,
					success: function (data) {

						$("#show_modal_document_title").html(data.title);
						$("#show_modal_document_body").html(data.body);
                        $("#show_this_document").css("padding-right","0px!important")	;	
                        $("#this_document_is_done").attr("data-document_id", document_id);
                        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
					}
                }); 
        }); 



        $(".update_this_document").on('click', function (event) {

            let document_id = $(this).data("document_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();


            $.ajax({
                    data: { 
                    	'document_id': document_id ,  
                    	'csrf_token': csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../update_book_document" ,
                    traditional: true,
					success: function (data) {

						$("#update_modal_document_body").html(data.body);

						$('#id_is_share').bootstrapToggle();  
						$('#id_is_publish').bootstrapToggle();  

					}
                }); 
        }); 



        $(document).on('click', ".get_this_chapter_inside_modal" , function (event) {

            let chapter_id = $(this).data("chapter_id");
            $("#chapter_id_inside_modal").val(chapter_id);
        }); 




        $(document).on('click', ".section_up_and_del" , function (event) {

            let section_id = $(this).data("section_id");
            let title      = $("#section_title"+section_id).text();

            $("#update_form_sec #id_title").val(title);
            $("#update_form_sec #section_id").val( section_id );
        }); 


        $(".selector_section_color").on('click', function (event) {
            $(".selector_section_color").addClass("opacity_color") ;   
            let color = $(this).data("color");
            $(this).removeClass("opacity_color") ; 
            $("#new_form_sec  #id_color").val("#"+color);
        }); 

        $(".selector_section_color_update").on('click', function (event) {
            $(".selector_section_color_update").addClass("opacity_color") ;   
            let color = $(this).data("color");
            $(this).removeClass("opacity_color") ;
            $("#update_form_sec  #id_color").val("#"+color);
        }); 



        $(document).on('click', ".publish_section",function (event) {

            let section_id = $(this).data("section_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if ($(this).parent().next().hasClass("opacity_color")){

                $(this).html("<i class='bi bi-eye'></i>") ;
                $(this).parent().next().removeClass("opacity_color");


            } else {

                $(this).html("<i class='bi bi-eye-slash'></i>") ;
                $(this).parent().next().addClass("opacity_color");
            }
            

            $.ajax({
                    data: { 
                        'section_id': section_id ,  
                        'csrf_token': csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../../book/publish_book_section" ,
                    traditional: true
                }); 
        }); 



        $(document).on('click', ".publish_book" ,  function (event) {

            let document_id = $(this).data("document_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if ($(this).hasClass("is_published")){

 
                $(this).removeClass("is_published");

            } else {

 
                $(this).addClass("is_published");
            }
            

            $.ajax({
                    data: { 
                        'document_id': document_id ,  
                        'csrf_token': csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../publish_book_document" ,
                    traditional: true
                }); 
        }); 




        $(document).on('click', "#this_document_is_done" , function (event) {

            let document_id = $(this).data("document_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax({
                    data: { 
                        'document_id': document_id ,  
                        'csrf_token': csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../../book/book_document_is_done" ,
                    traditional: true,
                    success: function (data) {

                        $("#span_this_document_is_done"+document_id).html(data.html)
                        $('#show_this_document').modal('hide');
                    }
                }); 
        });

 
 
        $(document).on('click', "#new_section_modal_creator" , function (event) {

                let title = $("#new_form_sec #id_title").val();
                let color = $("#new_form_sec #id_color").val();
                let chapter_id = $("#new_form_sec #chapter_id_inside_modal").val();
                
                $.ajax({
                        data: { 
                            'title': title , 
                            'color': color , 
                            'chapter_id' : chapter_id ,
                        } ,   
                        type: "POST",
                        dataType: "json",
                        url: "../../../book/create_book_section" ,
                        traditional: true,
                        success: function (data) {

                            $("#dropzone").append(data.html)
                            $('#chapter_new_section').modal('hide');
                        }
                    });

        });


 
        $(document).on('click', "#save_section" , function (event) {

                let section_id = $("#update_form_sec #section_id").val();
                let title = $("#update_form_sec #id_title").val();
                let color = $("#update_form_sec #id_color").val();
                $.ajax({
                        data: { 
                            'section_id': section_id , 
                            'title': title , 
                            'color': color , 
                        } ,   
                        type: "POST",
                        dataType: "json",
                        url: "../../../book/update_book_section" ,
                        traditional: true,
                        success: function (data) {
                            $("#book_main_page_section"+section_id).css('border-color', data.color);
                            $("#book_main_page_section_title"+section_id).css('background-color', data.color);
                            $("#section_title"+section_id).text(data.title);                         
                            $('#update_section').modal('hide');
                        }
                    });

        });


 
        $(document).on('click', ".delete_section" , function (event) {


            if (confirm('Êtes-vous sûr de vouloir supprimer cette section ?')) {
                 let section_id = $(this).data("section_id");

                $.ajax({
                        data: { 
                            'section_id': section_id ,    
                        } ,   
                        type: "POST",
                        dataType: "json",
                        url: "../../../book/delete_book_section" ,
                        traditional: true,
                        success: function (data) {

                            $("#book_main_page_section"+section_id).remove();       
                            $("#delete_section").modal('hide');         
                        }
                    });
              }  
 
        });






        $(document).on('click', "#create_a_new_document_button" , function (event) {
  			$("#create_a_new_document").show("slow");
  			$("#get_this_existing_document").hide("slow");
  			$(this).addClass("btn-primary");
  			$(this).removeClass("btn-default");
  			$("#get_an_existing_document").removeClass("btn-primary");
        });


        $(document).on('click', "#get_an_existing_document" , function (event) {
  			$("#get_this_existing_document").show("slow");
  			$("#create_a_new_document").hide("slow");
  			$(this).addClass("btn-primary");
  			$(this).removeClass("btn-default");
  			$("#create_a_new_document_button").removeClass("btn-primary");
        });


        $(document).on('keyup', "#form_new_document #id_title" , function (event) {
            $("#qf_part #id_title").val($(this).val())
        });


        function make_it_appears(div){
  			$(".disappear_div").hide("slow");        	
        	$(div).show("slow");
        }

        // doctypes = ["content","file","url","exercise","quizz","question","bibliotex","exotex","flashcard","flashpack"]

        $(document).on('click', "#show_text_part" , function (event) {
  			make_it_appears("#text_part");
  			$("#doctype").val(0);
            $("#new_qf_document").addClass("no_visu_on_load") ;
            $("#new_document").removeClass("no_visu_on_load") ;
        });


        $(document).on('click', "#show_link_part" , function (event) {
  			make_it_appears("#link_part");
  			$("#doctype").val(2);
            $("#new_qf_document").addClass("no_visu_on_load") ;
            $("#new_document").removeClass("no_visu_on_load") ; 
        });

        $(document).on('click', "#show_file_part" , function (event) {
  			make_it_appears("#file_part");
  			$("#doctype").val(1);
            $("#new_document").removeClass("no_visu_on_load") ;
            $("#new_qf_document").addClass("no_visu_on_load") ;
        });

        $(document).on('click', "#show_qf_part" , function (event) {
            make_it_appears("#qf_part");
            $("#doctype").val(9);
            $("#new_qf_document").removeClass("no_visu_on_load") ;
            $("#new_document").addClass("no_visu_on_load") ;
        });



        $(document).on('click', ".selector_book_section_document" , function (event) {

        	var section_id = $(this).data("section_id");
  			$("#book_section_id").val(section_id);
            $("#book_section_id_get").val(section_id);
            var chapter_id = $(this).data("chapter_id");
            $("#book_chapter_id").val(chapter_id);
            var section_title = $(this).data("section_title");  
            $("#this_document_section_title").text(section_title);

        });





            $("#dropzone").sortable({ 
            	connectWith: "#dropzone" , 
            	items      : ".book_main_page_section" , 
            	axis       : "y" ,
                stop: function (event, ui) {
 

                    var valeurs = [];
                    $( ".book_main_page_section" ).each(function() {
                        let doc_id = $(this).data("over_section_id"); 
                        valeurs.push(doc_id);
                    });

                    this_url =  "../../../book/sorter_book_section"  ;  

                    $.ajax({
                            data:   { 
                            	'valeurs': valeurs  ,    
                            	 } ,   
                            type: "POST",
                            dataType: "json",
                            url: this_url,
                            traditional: true,
                        }); 
                    }
                });

 

	        $(document).on('click', ".selector_existant_book_document_choice" , function (event) {

	            let chapter_id = $("#book_chapter_id").val();
	            let type       = $(this).data("type");
	            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
	            let level_id   = $("#book_level_id").val();
	            let subject_id = $("#book_subject_id").val();


	            $(".selector_existant_book_document_choice").removeClass("book_chapters_in_menu_selected");

	            $(this).addClass("book_chapters_in_menu_selected");
				$(this).removeClass("existant_book_document_choice");

                $("#show_document_by_type").html("<i class='fa fa-spinner fa-spin fa-4x'></i>");


	            $.ajax({
	                    data: { 
	                    	'type': type ,  
                            'n'   : 1,
	                    	'chapter_id' : chapter_id,
	                    	'level_id'   : level_id,
	                    	'subject_id' : subject_id,
	                    	'csrf_token' : csrf_token 
	                    } ,   
	                    type: "POST",
	                    dataType: "json",
	                    url: "../../../book/get_type_book_document" ,
	                    traditional: true,
						success: function (data) {

							$("#show_document_by_type").html(data.html);

						}
	                }); 
        	}); 




            $(document).on('click', ".modify_number_display" , function (event) {

                let chapter_id = $("#book_chapter_id").val();
                let type       = $(this).data("type");
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                let level_id   = $("#book_level_id").val();
                let subject_id = $("#book_subject_id").val();
                let n          = $(this).data("n");

                $("#show_document_by_type").html("<i class='fa fa-spinner fa-spin fa-4x'></i>");

                $.ajax({
                        data: { 
                            'type': type ,  
                            'chapter_id' : chapter_id,
                            'level_id'   : level_id,
                            'subject_id' : subject_id,
                            'n' : n,
                            'csrf_token' : csrf_token 
                        } ,   
                        type: "POST",
                        dataType: "json",
                        url: "../../../book/get_type_book_document" ,
                        traditional: true,
                        success: function (data) {

                            $("#show_document_by_type").html(data.html);

                        }
                    }); 
            }); 







            $(document).on('click', "#insert_document_into_this_section" , function (event) {

                    var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                    var section_id = $("#book_section_id_get").val();
                    var level_id   = $("#book_level_id").val();
                    var subject_id = $("#book_subject_id").val();
                    var valeurs = [];
                    var type_doc;
                    $(".select_document_into_section").each(function() {

                        if ($(this).is(":checked"))
                                {   
                                    var values = $(this).val(); 
                                    if (values !="")
                                        {  
                                            document_id = values.split("-")[0];
                                            type_doc = values.split("-")[1]; 
                                            valeurs.push(document_id);
                                        }
                                }
                    });
 
                    $.ajax({
                            data: { 
                                'valeurs'    : valeurs,
                                'type_doc'   : type_doc,
                                'level_id'   : level_id,
                                'section_id' : section_id,                                
                                'subject_id' : subject_id,
                                'csrf_token' : csrf_token 
                            } ,   
                            type: "POST",
                            dataType: "json",
                            url: "../../../book/insert_document_into_section" ,
                            traditional: true,
                            success: function (data) {

                                $("#chapter_new_document").modal('hide'); 

                                $("#book_main_page_body"+section_id).append(data.html)
                            }
                        }); 
                }); 







	        $(document).on('click', ".get_this_document" , function (event) {


	            let type        = $(this).data("type");
	            let document_id = $(this).data("document_id");
	            let section_id  = $(this).data("section_id");
	            let chapter_id  = $(this).data("chapter_id");
	            let book_id     = $(this).data("book_id");
	            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

	            $(this).parent().parent().remove();


	            $.ajax({
	                    data: { 
	                    	'type'       : type ,  
	                    	'document_id': document_id,
	                    	'chapter_id' : chapter_id,
	                    	'book_id'    : book_id,
	                    	'section_id' : section_id,
	                    	'csrf_token' : csrf_token 
	                    } ,   
	                    type: "POST",
	                    dataType: "json",
	                    url: "../../get_this_document_to_chapter" ,
	                    traditional: true,
						success: function (data) {

							$("#book_main_page_section"+data.section_id).html(data.html);

						}
	                }); 
        	}); 





});

});

 