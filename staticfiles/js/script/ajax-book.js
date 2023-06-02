define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-book.js OK");

    
        $("#new_chapter_button").on('click', function (event) {

            $("#modal_title").html("Nouveau chapitre");
            $("#is_update").val(0);
 
        }); 




        $(".get_the_title").on('click', function (event) {

            let title = $(this).data("title");
            $("#modal_title").html("Modification du titre du chapitre");
            $("#new_chapter  #id_title").val(title);
            $("#is_update").val(1);

            $("#pk_update").val( $(this).data("pk") );
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



        $(".book_main_page_section_document_eraser").on('click', function (event) {

			if (confirm('Êtes-vous sûr de vouloir supprimer ce document ?')) {

            let document_id = $(this).data("document_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax({
                    data: { 
                    	'document_id': document_id ,  
                    	'csrf_token': csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../delete_book_document" ,
                    traditional: true,
					success: function (data) {

						$("#this_document"+document_id).remove();
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

                    this_url =  "../../sorter_book_document"  ;  

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




        $(".book_main_page_section_document_detail").on('mousedown', function (event) {

            var section_id = $(this).data("section_id");
            var document_id =$(this).data("document_id");

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



        $(".show_this_document").on('click', function (event) {

            let document_id = $(this).data("document_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();


            $.ajax({
                    data: { 
                    	'document_id': document_id ,  
                    	'csrf_token': csrf_token 
                    } ,   
                    type: "POST",
                    dataType: "json",
                    url: "../../show_book_document" ,
                    traditional: true,
					success: function (data) {

						$("#show_modal_document_title").html(data.title);
						$("#show_modal_document_body").html(data.body);
                        $("#show_this_document").css("padding-right","0px!important")	;					
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

 