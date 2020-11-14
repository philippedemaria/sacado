define(['jquery','bootstrap','bcPicker'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS corrector.js OK");

////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
///// INIT
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
                $(".tools").hide();
                $(".remove").hide();

                 
			    $('iframe').each(function(){
			        var url = $(this).attr("src");
			        $(this).attr("src",url+"?wmode=opaque");
			    });

////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
///// Gestion des annonations après leur enregistrement dans la base de données
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
               
////////////////////////////////////////////////////////////////////////////////////////////////////////////	
// classe est une classe donnée une fois l'annotation enregistrée dans la base de données
////////////////////////////////////////////////////////////////////////////////////////////////////////////
                $( ".classe" ).draggable({
							    classes: {
							      "ui-draggable": "move"
							    }
							  });  


                // Permet de déplacer une annotation après son enregistrement dans la base de donnée
				$( ".classe" ).on('mouseup', function(){	

									attr_id = $(this).attr("id");
									style = $(this).attr("style");
									html = $(this).html();
									save_annotation(attr_id, style,  "classe" , html ) ;
									}); 
 


////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
///// Affecte la classe primary au bouton quand cliqué
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
                function toggle_div(toggle,target,e){

                	change_color(toggle,"",e);

                      if (toggle.hasClass("btn-default")) {
                      		target.hide(500);                         	
                      }
                      else{
                      		target.show(500);                         	
                      }
                }


                function change_color(toggle,tool,e){

					if (toggle.hasClass("btn-default")) 
							{
			                    $("button").removeClass("btn-primary").addClass("btn-default");  
			                    $("#trash").removeClass("btn-danger").addClass("btn-default");  
			                    toggle.addClass("btn-primary").removeClass("btn-default");
			                    $(".tools").hide(500);
			                	$(".remove").css("color",'transparent'); 
			                    e.preventDefault();
							}
					else
					{
						toggle.addClass("btn-default").removeClass("btn-primary");
	                    $(".tools").hide(500);
	                	$(".remove").css("color",'transparent'); 
	                    e.preventDefault();
					}


                  }  

                  $("#text_writer").on('click', function (e) { 
                     change_color($(this),$("#text_tools"),e);
                  }) 
                  $("#paint_brush").on('click', function (e) { 
                      change_color($(this),$("#paint_tools"),e);
                      $("#paint_tools").show(500);                            
                  }) 
                  $("#wrong").on('click', function (e) {
                      change_color($(this),"",e);
                  }) 
                  $("#right").on('click', function (e) {
                      change_color($(this),"",e);
                  }) 
                  $("#line").on('click', function (e) {
                      change_color($(this),"",e);
                  }) 
 
                  $("#save").on('click', function (e) {
                      change_color($(this),"",e);
                  })


                  $("#comments").on('click', function (e) {

	                   	toggle_div($(this),$("#comments_div"),e)
	                })


                  $("#trash").on('click', function (e) {  

					if ($("#corrector").find(".gray").length == 0) 
						{ 
							alert("Tout est effacé, vous ne pouvez pas sélectionner l'outil poubelle.");
						}
					else
						{
							if ($("#trash").hasClass("btn-default")) 
							{ 
			                    $("#trash").addClass("btn-danger").removeClass("btn-default");
			                	$(".remove").css("color",'red').css("display",'block');  
			                }
			                else{
			                    $("#trash").addClass("btn-default").removeClass("btn-danger");
			                	$(".remove").css("color",'transparent').css("display",'block');

			                }
						}

                    e.preventDefault();
                  }) 


/////////////////////////    Cas particulier   /////////////////////////////////////////////////////////////


   				$("body").on('click', '#delete_appreciation', function (e) { 

 					if($("#delete_appreciation").hasClass("btn-default")) {  // Le bouton supprimer une appréciation devient rouge
						$(this).addClass("btn-danger").removeClass("btn-default");
                     	$(".comment").addClass("btn-danger").removeClass("btn-primary").removeClass("btn-default");
                    }
                    else
                    {
						$(this).addClass("btn-default").removeClass("btn-danger");
                     	$(".comment").addClass("btn-default").removeClass("btn-primary").removeClass("btn-danger");
                    }
                     	
                    $("#modifier_appreciation").addClass("btn-default").removeClass("btn-primary");

                   e.preventDefault();
                });




   				$("body").on('click', '#modifier_appreciation', function (e) { 

 					if($("#modifier_appreciation").hasClass("btn-default")) {  // Le bouton supprimer une appréciation devient rouge
 						$(".comment").addClass("btn-primary").removeClass("btn-default").removeClass("btn-danger");
                     	$(this).addClass("btn-primary").removeClass("btn-default");
                    }
                    else
                    {
						$(this).addClass("btn-default").removeClass("btn-primary");
                     	$(".comment").addClass("btn-default").removeClass("btn-primary").removeClass("btn-danger");
                    }
                     	
                    $("#delete_appreciation").addClass("btn-default").removeClass("btn-danger");

                   e.preventDefault();
                });


/////////////////////////    Cas particulier   /////////////////////////////////////////////////////////////
                  $("#my_appreciations").on('click', '.comment', function (e) {  

	                  	if ($("#modifier_appreciation").hasClass("btn-primary") )  // Modification enregistrement
	                  	{ 

	                      	$(".comment").addClass("btn-default").removeClass("btn-primary");
	                     	$(this).addClass("btn-primary").removeClass("btn-default");   
	                     	$("#modifier_appreciation").addClass("btn-default").removeClass("btn-primary");

							value = $(this).attr("data-text");

	                      	$("#id_comment").val(value);

	 						selected = $(this).attr("id");

	 						comment_id = selected.substring(7,selected.length);

	                      	$("#modif_appreciation").val(comment_id);
	                      	$("#add_my_appreciation").html("").html("Modifier");
	                  	}

	                  	else if ($(this).hasClass("btn-danger") )
	                  	{
	                  		 
	                  		if (!confirm('Vous souhaitez supprimer cette appréciation : ' + $(this).attr("data-text") + ' ?')) return false;

	 						selected = $(this).attr("id");
	 						comment_id = selected.substring(7,selected.length);

	                  		delete_appreciation(comment_id);
	                  	}
	                  	else // Ajout enregistrement
	                  	{
	                      	$(".comment").addClass("btn-default").removeClass("btn-primary");
	                     	$(this).addClass("btn-primary").removeClass("btn-default");   
	                     	$("#modifier_appreciation").addClass("btn-default").removeClass("btn-primary");

	                  	}
	                    e.preventDefault();
                  }) 
 
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////      Création des annontations  
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
        function annote(toggle,event,type){ 

                  	// décale l'abscisse selon la position du clic de la souris
                  	var abscisse = event.pageX - 420; // - 412

                  	// décale l'ordonnée selon la hauteur du clic de la souris

                    var ordonnee = event.pageY - 90   ; //  - 82

 
                    // récupération du numéro du toggle
                    var nb = toggle.attr("data-nb");

                    // Caractéristiques à afficher suivant le toggle
                    if(type == 0) 
                    	{ 
	                      	fa = "times" ; 
	                      	color = "danger" ; 
                      	} 

                    else if (type ==1) 
                      	{  
                      		fa = "check" ; 
                      		color = "success" ;  
                      	}


                    // Poubelle Effaceur
					var erase = "<a href='#' class='pull-right gray remove'><i class='fa fa-trash' style='font-size:9px'></i></a>";

					// style de la div
					var style = "position:absolute;left:"+abscisse+"px; top:"+ordonnee+"px;z-index:99;" ;

                    var classe = "classe" ;

			//////////////////////////////////////
			////// Création des annotations //////
			//////////////////////////////////////

	                // Check ok times
                    if (type < 2)
	                    {
	                    	// studentcontent ne contient pas a possibilité d'effacer.
	                    	studentcontent = "<i class='fa fa-"+fa+" text-"+color+"'></i>" ;
			            	content = studentcontent+erase;
	                    }
	                // Conmmentaire pré écrit par l'enseignant 
                    else if  (type == 2)
	                    {
	                    	// Récupération du texte et de ses caractéristiques
	                    	fa = "commentaire"
	                      	text = toggle.attr("data-text");
	                      	color = toggle.attr("data-color");
	                    	// Si pas de couleur choisie on ajoute du noir
	                      	if (!color) 
	                      		{
	                      			color = "#000";
	                      		}

                       		extra_style = "font-size:14px;font-weight:700;" ;

                       		style = style+extra_style ;
			            	style = style+"color:"+color ;
	                    	// studentcontent ne contient pas a possibilité d'effacer.
			            	studentcontent = text;
			            	content =  studentcontent+erase ;

			            	classe = classe + " annotation"

	                    }
	                // Soulignement
                    else if  (type == 3)
	                    {
	                    	// Récupération du texte et de ses caractéristiques
	                    	fa = "line"
	                      	color = toggle.attr("data-color");
	                    	// Si pas de couleur choisie on ajoute du noir
	                      	if (!color) 
	                      		{
	                      			color = "#000";
	                      		}

 							fa_line = "<i class='fa fa-window-minimize' style='color:"+color+"'></i>";
	                    	// studentcontent ne contient pas a possibilité d'effacer.
							studentcontent = fa_line+fa_line+fa_line
			            	content =  studentcontent+erase ;	

	                    }
	                // id de la div
			        var attr_id = fa+""+nb ;
	                // La div crée dans le HTML
	                var myDiv = "<div id='"+attr_id+"' style='"+style+"'>"+content+"</div>"  
                    
	                // Ajout de myDiv à la div via son id #corrector
                    $('#corrector').append(myDiv) ;

	                // Rend la nouvelle div draggable
                    $("#"+fa+""+nb).draggable();

	                // Associe un nouveau nb au bouton de création toggle 
                    nb++; // nb est le nombre d'annotations sur la page

                    if (type == 2)
	                    {
 							$('.comment').attr("data-nb",nb);
	                    }
	                else
	                    {
 							toggle.attr("data-nb",nb);
	                    }

	                // Action de l'AJAX

                    save_annotation( attr_id, style,  classe,  content, studentcontent) ;	  
                  } 





////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////// Clone la div textuelle
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
        function create_clone(e){ 
              	// décale l'abscisse selon la position du clic de la souris
              	var abscisse = event.pageX - 420; // - 412

              	// décale l'ordonnée selon la hauteur du clic de la souris
                var ordonnee = event.pageY - 120   ; //  - 82

              	// clone de la div clonée
	            var clone = $("#templateDiv").clone();

	            // Modifie l'id du clone
	            var nbClone = $("#templateDiv").attr("data-nbclone");
	            clone[0].id = "#templateDiv"+nbClone ;

	            // Rend le clone draggabe  
	            clone.draggable();
	            clone.appendTo("#corrector");
	            // Enlève le style "display","block" au clone
	            clone.find('remove').css("display","block");
	            // Ajout de la classe et de la position
	            clone.addClass("annotation").attr("style",'left:'+abscisse+'px; top:'+ordonnee+'px;') ;

	            // Associe le numéro du clone                        
	            nbClone++ ;
	            $("#templateDiv").attr("data-nbclone",nbClone);
	            clone.css({"font-size":"14px", "font-weight": 700});
	            clone.find('.textarea_div').focus();
	            // Empeche l'appel du lien par la balise button
	          	e.preventDefault();
				}
 



				$(document).on("keyup", ".textarea_div", function() {

					attr_id = $(this).parent().parent().parent().attr("id") ; 
					style = $(this).parent().parent().parent().attr("style") ;
					classe = "classe"
					text_value = $(this).val() ;
					style = style+"position:absolute;"
					style_textarea = $(this).attr("style") ;

					studentcontent =  "<a href='#' class='pull-right gray remove' ><i class='fa fa-trash fa-xs'></i></a><div class='annotationheader' ><i class='fa fa-arrows-alt fa_white'></i></div><div class='row'><div class='col-xs-12 col-md-12 col-lg-12'><textarea rows='2' cols='30' class='textarea_div' style='"+style_textarea+"' >"+text_value+"</textarea></div></div> "; 


				    save_textarea_div_content(attr_id, style,  classe, studentcontent) ;

				})
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////   Appels des fonctions de création
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
                $("#corrector").on('click', function (e) { 

 					if ($("#trash").hasClass("btn-danger")) { 
                      	
                      	if ($("#corrector").find(".gray").length == 0) 
                      		{ 
                      			$("#trash").addClass("btn-default").removeClass("btn-danger");
                      		}

                    	}
                    else if($("#text_writer").hasClass("btn-primary")) {

							if ( ($("#corrector").find(".textarea_div").val() != "") || ($("#templateDiv").attr("data-nbclone")==0)) { create_clone(e); }

                      	}

                    else if ($("#right").hasClass("btn-primary")) { 

                      	annote($("#right"),e,1) ;

                    	}

                    else if ($("#line").hasClass("btn-primary")) { 

                      	annote($("#line"),e,3) ;

                    	}
                    else if ($("#wrong").hasClass("btn-primary")) {  

                        annote($("#wrong"),e,0) ;

                    	}



                });


   				$("body").on('click', '#corrector', function (e) { 

 					if($(".comment").hasClass("btn-primary")) {  // commentaire d'un enseignant pré écrit

                    	// Choisit le bon commentaire
						selector = $("#my_appreciations").find(".btn-primary");
 						selected = $("#"+selector.attr("id"));

 						annote(selected,e,2) ;

                    	}
                });

////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////   Supprime la div cliquée
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
                 $("#corrector").on('click', '.remove', function () {
                 	attr_id = $(this).parent().attr("id") ; 

	                    $(this).parent().remove();
	                     erase_annotation(attr_id) ; 


                    });

////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////    
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////

  


////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////   Color Picker text
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
                    $('#bcPicker1').bcPicker();

                    $('.bcPicker-palette').on('click', '.bcPicker-color', function(){
                      var color = $(this).css('background-color');
                      var hex_color = $.fn.bcPicker.toHex(color) ;
                      $(".textarea_div").css("color", hex_color);
                      $(".comment").attr("data-color", hex_color);
                      $(".line").attr("data-color", hex_color);
                      $(this).parent().parent().find('.bcPicker-picker').css('background-color',hex_color);
                      $(this).parent().parent().find('.bcPicker-palette').toggle();
                    })
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////   AJAX
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////

            function save_annotation(attr_id, style,  classe, studentcontent ) {  

                    let answer_id = $("#answer_id").val() ; 
                    let custom = $("#custom").val() ; // 0 si relationship et 1 si customexercise
                    let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

 

                    url =  '../../../ajax_save_annotation' ;

                    $.ajax({
                        url: url ,
                        type: "POST",
                        data: {
                            'attr_id': attr_id,
                            'style': style,
                            'classe': 'classe',
                            'studentcontent': studentcontent,
                            'answer_id': answer_id,
                            'custom': custom,
                            csrfmiddlewaretoken: csrf_token,    
                        },
                        dataType: 'json',
                        success: function (data) {
                            console.log("enregistré");
                            
                        }


                    });

                }




                function erase_annotation(attr_id) { 

                    let answer_id = $("#answer_id").val() ; 
                    let custom = $("#custom").val() ; // 0 si relationship et 1 si customexercise
                    let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

                    url =  '../../../ajax_remove_annotation' ;

                    $.ajax({
                        url: url ,
                        type: "POST",
 						data: {
                            'attr_id': attr_id,
                            'answer_id': answer_id,
                            'custom': custom,
                            csrfmiddlewaretoken: csrf_token,    
                        },
                        dataType: 'json',
                        success: function (data) {
                            console.log("effacé");
                        }
                    });

                }

 


		        function save_textarea_div_content(attr_id, style, classe, studentcontent) { 

		            let answer_id = $("#answer_id").val() ; 
		            let custom = $("#custom").val() ; // 0 si relationship et 1 si customexercise
		            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

		            url =  '../../../ajax_save_annotation' ;

		            $.ajax(
		                {
		                    type: "POST",
		                    dataType: "json",
		                    data: {
		                            'attr_id': attr_id,
		                            'style': style,
		                            'classe': 'classe',
		                            'studentcontent': studentcontent,
		                            'answer_id': answer_id,
		                            'custom': custom,
		                            csrfmiddlewaretoken: csrf_token,   
		                    },
		                    url: url ,
		                    success: function (data) {
		                            console.log("enregistré");
		                    }
		                }
		            )
		        } 


		        function delete_appreciation(comment_id) { 

 
		            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

		            url =  '../../../ajax_remove_my_appreciation' ;

		            $.ajax(
		                {
		                    type: "POST",
		                    dataType: "json",
		                    data: {
		                            'comment_id': comment_id,
		                            csrfmiddlewaretoken: csrf_token,   
		                    },
		                    url: url ,
		                    success: function (data) {
		                    	$("#comment"+comment_id).remove();		                         
		                    }
		                }
		            )
		        }



////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////   Ajouter une appréciation personnelle dans sa liste
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
                 $("#add_my_appreciation").on('click', function () {
                 	 
	 					let comment = $("#id_comment").val() ; 
			            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
			            let comment_id = $("#modif_appreciation").val() ; 
	 

			            $.ajax(
			                {
			                    type: "POST",
			                    dataType: "json",
			                    data: {
			                            'comment': comment,
			                            'comment_id': comment_id,
			                            csrfmiddlewaretoken: csrf_token,   
			                    },
			                    url: '../../../ajax_create_or_update_appreciation' ,
			                    success: function (data) {

			                    	if (comment_id)
			                    	{
			                    		$("#comment"+comment_id).html(comment) ;
			                    		$("#comment"+comment_id).attr("data-text",comment) ;		                    		
			                    	}
			                    	else
			                        {
			                    	$("#my_appreciations").append(data.html) ;
			                    	$("#comments_div").show(500) ;
			                    	}

			                    	$("#modif_appreciation").val("");	
			  	                    $("#add_my_appreciation").html("").html("Sauvegarder");
									$("#id_comment").val("") ; 
                            		if($('#empty_annotation') ) { $('#empty_annotation').hide(500); }
			                    }
			                })


                    });
 


    });
});