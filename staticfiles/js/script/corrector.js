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

  
                  $("#more").on('click', function (e) {

		                   	toggle_div($(this),$("#more_text"),e)
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
                  $(".comment").on('click', function (e) {
                      	$(".comment").addClass("btn-default").removeClass("btn-primary");
                     	$(this).addClass("btn-primary").removeClass("btn-default");   
                      	e.preventDefault();
                  }) 
 
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
//// Cette fonction agit avec les boutons dans la zone de correction
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
        function annote(toggle,event,type){ 

                  	// décale l'abscisse selon la position du clic de la souris
                  	abscisse = event.offsetX ; // - 412

                  	// décale l'ordonnée selon la hauteur du clic de la souris
                    ordonnee = event.offsetY - 15   ; //  - 82
 
                    // récupération du numéro du toggle
                    nb = toggle.attr("data-nb");

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

                    // Affichage du tpe de div selon l'appel du toggle
                    if (type < 2)
	                    {
	                     	myDiv = "<div id='"+fa+""+nb+"' style='position:absolute;left:"+abscisse+"px; top:"+ordonnee+"px;z-index:99;'><i class='fa fa-"+fa+" text-"+color+"'></i><a href='#' class='pull-right gray remove'><i class='fa fa-trash' style='font-size:9px'></i></a></div>" 
	                    }
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

	                      	myDiv = "<div id='"+fa+""+nb+"' style='position:absolute;left:"+abscisse+"px; top:"+ordonnee+"px;z-index:99;color:"+color+"'>"+text+"<a href='#' class='pull-right gray remove'><i class='fa fa-trash' style='font-size:9px'></i></a></div>"   
	                    }
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

	                      	myDiv = "<div id='"+fa+""+nb+"' style='position:absolute;left:"+abscisse+"px; top:"+ordonnee+"px;z-index:99'><i class='fa fa-window-minimize' style='color:"+color+"'></i><i class='fa fa-window-minimize' style='color:"+color+"'></i><i class='fa fa-window-minimize' style='color:"+color+"'></i><a href='#' class='pull-right gray remove'><i class='fa fa-trash' style='font-size:9px'></i></a></div>"   
	                    }
	                // Ajout de myDiv à la div via son id #corrector
                    $('#corrector').append(myDiv) ;

	                // Rend la nouvelle div draggable
                    $("#"+fa+""+nb).draggable();

	                // Associe un nouveau nb au bouton de création toggle 
                    nb++;

                    if (type == 2)
	                    {
 							
 							$('.comment').attr("data-nb",nb);
	                    }
	                else
	                    {
 							toggle.attr("data-nb",nb);
	                    }    

                  } 


        function create_clone(e){   

	            var clone = $("#templateDiv").clone();

	            // Modifie l'id du clone
	            nbClone = $("#templateDiv").attr("data-nbclone");
	            clone[0].id = "#templateDiv"+nbClone ;

	            // Rend le clone draggabe  
	            clone.draggable();
	            clone.appendTo("#corrector");
	            // Enlève le style "display","block" au clone
	            clone.find('remove').css("display","block");
	            // Ajout de la classe et de la position
	            clone.addClass("annotation").attr("style",'left:'+e.offsetX+'px; top:'+e.offsetY+'px;') ;

	            // Associe le numéro du clone                        
	            nbClone++ ;
	            $("#templateDiv").attr("data-nbclone",nbClone);
	            clone.find('.textarea_div').focus();

	            // Empeche l'appel du lien par la balise button
	          	e.preventDefault();
				}


////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////   Crée une div d'écriture ou une annotation
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

                    else if ($(".comment").hasClass("btn-primary")) { 

                    	// Choisit le bon commentaire
						selector = $("#comments_div").find(".btn-primary");
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

                     $(this).parent().remove();  

                    });
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////   Enlève les contours de la div une fois le clic perdu
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

                $("#level_selected_id").on('change', function () { 
                    let level_selected_id = $(this).val();

                    let data_url = $(this).attr("data-url"); 
                    if (data_url == "yes") { url =  'qcm/ajax/parcours_default' ; } else { url =  'ajax/parcours_default' ; } 
                    let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

                    $.ajax({
                        url: url ,
                        type: "POST",
                        data: {
                            'level_selected_id': level_selected_id,
                            csrfmiddlewaretoken: csrf_token,    
                        },
                        dataType: 'json',
                        success: function (data) {
                            $("#parcours_shower").html(data.html);


                        }
                    });
                  });



    });
});