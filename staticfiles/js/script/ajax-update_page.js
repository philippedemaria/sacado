define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-book.js OK");

    
        $("#new_chapter_button").on('click', function (event) {
            $("#modal_title").html("Nouveau chapitre");
            $("#is_update").val(0);
        }); 


        $("#id_typebloc").on('change', function (event) {

            var t = $(this).find(':selected').text(); 

            $("#book_new_bloc #id_title").val(t);
        }); 





        $(".this_updater_paragraph").on('click', function (event) {

            let paragaph_id = $(this).data("paragaph_id");
            let paragraph_number = $("#paragraph_number"+paragaph_id).val();
            let paragraph_title = $("#paragraph_title"+paragaph_id).val();

            $("#id_parag").val(paragaph_id);
            $("#number_parag").val(paragraph_number);
            $("#title_parag").val(paragraph_title);
        }); 


        $("#type_de_page").on('change', function (event) {

            var type_page = $(this).val();
            var book_id = $(this).data("book_id");
            var page_id = $(this).data("page_id");

            $.ajax({
                    data: { 
                        'type_page' : type_page ,
                        'book_id'   : book_id ,
                        'page_id'   : page_id 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../type_de_page" ,
                    traditional: true,
                    success:function(data){

                       $("#top_page").attr('class', '');
                       $("#top_page").addClass(data.css);
                       $("#top_page_title").html(data.title);

                    }
                }); 
        }); 


        $("#book_update_submitter_paragraph").on('click', function (event) {

            var paragaph_id      = $("#id_parag").val();
            var paragraph_number = $("#number_parag").val();
            var paragraph_title  = $("#title_parag").val();
            let csrf_token       = $("input[name='csrfmiddlewaretoken']").val();


            $.ajax({
                    data: { 
                        'paragaph_id'      : paragaph_id ,  
                        'paragraph_number' : paragraph_number ,  
                    	'paragraph_title'  : paragraph_title ,  
                    	'csrf_token'       : csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../update_paragraph" ,
                    traditional: true,
					success: function (data) {

						$("#paragraph_number"+paragaph_id).html(paragraph_number);
						$("#paragraph_title"+paragaph_id).html(paragraph_title);				
					}
                }); 
        }); 

        $(".update_this_document").on('click', function (event) {

            let document_id = $(this).data("document_id");
            let csrf_token  = $("input[name='csrfmiddlewaretoken']").val();


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



        $(".section_up_and_del").on('click', function (event) {

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



        $(".publish_section").on('click', function (event) {

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
                    url: "../../publish_book_section" ,
                    traditional: true
                }); 
        }); 



        $(".publish_book").on('click', function (event) {

            let document_id = $(this).data("document_id");
            let csrf_token  = $("input[name='csrfmiddlewaretoken']").val();

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




        $(".is_done_document").on('click', function (event) {

            let document_id = $(this).data("document_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if ($(this).hasClass("is_done")){
                $(this).removeClass("is_done");
            } else {
                $(this).addClass("is_done");
            }
            
            $.ajax({
                    data: { 
                        'document_id': document_id ,  
                        'csrf_token': csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../book_document_is_done" ,
                    traditional: true
                }); 
        });

 


 
        $(".delete_section").on('click', function (event) {

			if (confirm('Êtes-vous sûr de vouloir supprimer cette section ?')) {

	            let section_id = $(this).data("section_id");
	            $.ajax({
	                    data: { 
	                    	'section_id': section_id ,    
	                    } ,   
	                    type: "POST",
	                    dataType: "json",
	                    url: "../../delete_book_section" ,
	                    traditional: true,
						success: function (data) {

							$("#this_section_in_modal"+section_id).remove();	
							$("#section"+section_id).remove();	
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
                this_url =  "../../sorter_book_section"  ;  
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

            let chapter_id = $(this).data("chapter_id");
            let type       = $(this).data("type");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            let level_id   = $("#book_level_id").val();
            let subject_id = $("#book_subject_id").val();

            $(".selector_existant_book_document_choice").removeClass("book_chapters_in_menu_selected");
            $(this).addClass("book_chapters_in_menu_selected");
			$(this).removeClass("existant_book_document_choice");

            $.ajax({
                    data: { 
                    	'type': type ,  
                    	'chapter_id' : chapter_id,
                    	'level_id'   : level_id,
                    	'subject_id' : subject_id,
                    	'csrf_token' : csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../get_type_book_document" ,
                    traditional: true,
					success: function (data) {

						$("#show_document_by_type").html(data.html);
					}
                }); 
        	}); 



        $(document).on('click', ".get_this_document" , function (event) {

            let type        = $(this).data("type");
            let document_id = $(this).data("document_id");
            let section_id  = $(this).data("section_id");
            let chapter_id  = $(this).data("chapter_id");
            let book_id     = $(this).data("book_id");
            let csrf_token  = $("input[name='csrfmiddlewaretoken']").val();

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


        $("#course_page_main").sortable({ 
            connectWith: "#course_page_main" , 
            items      : ".bloc_sorter" , 
            axis       : "y" ,
            distance: 0 ,
            stop: function (event, ui) {

                var this_paragraph_id = $(ui.item).data("paragraph_id");
                var this_bloc_id      = $(ui.item).data("bloc_id");
                var paragraph_id = $(ui.item).parent().parent().data("paragraph_id");

                var valeurs = [];
                $( ".bloc_sorter" ).each(function() {
                    let bloc_id = $(this).data("bloc_id"); 
                    valeurs.push(bloc_id);
                });
 

                this_url =  "../../sorter_book_page_bloc"  ;  
                $.ajax({
                        data:   { 
                            'this_paragraph_id': this_paragraph_id  , 
                            'this_bloc_id': this_bloc_id  , 
                            'paragraph_id': paragraph_id  , 
                             'valeurs': valeurs  ,                               
                             } ,   
                        type: "POST",
                        dataType: "json",
                        url: this_url,
                        traditional: true,
                    }); 
                }
            });



        $(document).on('mousedown', ".book_main_page_section_document_move", function (event) {

            var section_id = $(this).data("section_id");
            var document_id =$(this).data("document_id");

            sorter_document(document_id , section_id) ;
 
        })




    });

});

 