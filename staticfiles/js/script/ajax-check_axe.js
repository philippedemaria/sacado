define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () { 
        console.log("chargement JS ajax-check_axe.js  OKK");

 
    // ****************************************************************************************************************************************
    // Gestion des slides dans la vue élève
    // ****************************************************************************************************************************************
    var this_slideBox = $('.this_slider ul');
    var slideWidth = 700 ;
    var slideQuantity = $('.this_slider ul').children('li').length;
    var currentSlide = 1 ;
    this_slideBox.css('width', slideWidth*slideQuantity);
    var nb_variables = $('#nb_variables').length; 

    //setTimeout( function() { set_var_value(1) }, 1000);


    $('.nav_start').on('click', function(){ 

            var pxValue = currentSlide * slideWidth ; 
            this_slideBox.animate({
                'left' : -pxValue
            });
            currentSlide++ ;
    });

//*************************************************************************************************************  
// Récupération des réponses
//************************************************************************************************************* 

    $(document).on('change', ".selected_answer" , function () { 

        let csrf_token     = $("input[name='csrfmiddlewaretoken']").val();
        let is_correct     = $(this).data("is_correct") ;
        let loop           = $(this).data("loop") ;
        let choice_id      = $(this).val() ;
        let list_choices   = [] ;   
             
        if ($(this).is(":checked"))
        {
            list_choices.push(choice_id) ;
        }
        else{

            idx = list_choices.indexOf(  choice_id ) ;
            if(idx>-1)
            { list_choices.splice(idx, 1) ;}
        }
        $("#nav_start"+loop).attr("data-choice_ids",list_choices);;
        $("#nav_start"+loop).attr("data-is_correct",is_correct);
    });


//*************************************************************************************************************  
// Classement sur axe
//*************************************************************************************************************  


            var tab=document.getElementById("tableau");
            var xoffset   = tab.offsetTop;
            var yoffset   = tab.offsetLeft;
            var xmin      = parseFloat($("#xmin").val().replace(",","."));
            var xmax      = parseFloat($("#xmax").val().replace(",","."));
            var tick      = parseFloat($("#tick").val().replace(",","."));
            var subtick   = parseFloat($("#subtick").val().replace(",","."));
            var precision = parseFloat($("#precision").val().replace(",","."));
            var topz      = $(".loop0").length ;   // le niveau de la couche la plus haute

            var axe = document.getElementById("axe");
              //dessin des graduations de l'axe

            function placeValeur(x,v) {   
               // position en pixels, en fonction de la valeur x
               x_axe=Math.round((x - xmin )/( xmax - xmin ) * axe.offsetWidth);

               // creation du label : le texte de la valeur à afficher
               if (v){ 
               label=document.createElement("div");
               label.textContent=x.toString();
               label.style.position="absolute";
               label.style.top  = "-40px";
               axe.appendChild(label);
               label.style.text_align="center";
               label.style.left = x_axe-label.offsetWidth/2+"px";
                }
               // le "tick" = la graduation 
               let tick= document.createElement("div");
               tick.style.position="absolute";
               tick.style.background='#5f8cff';
                if (v)
                    {
                        tick.style.top  = '-10px' ;
                        tick.style.height= '12px' ;
                    }
                else {
                        tick.style.top  = '-5px' ;
                        tick.style.height= '7px' ;
                }


               tick.style.width="0px";
               tick.style.border="1px solid #5f8cff";
               tick.style.left = x_axe+"px";
               axe.appendChild(tick); 
            }


            function dessineGraduations(){

                for (var x = xmin ; x < xmax ; x = x + tick ) 
                    { 
                    placeValeur(x,1) 
                }
                for (var x = xmin ; x < xmax ; x = x + subtick ) 
                    { 
                    placeValeur(x,0) 
                }

                placeValeur( xmax ,1);
            }

            dessineGraduations();

            cartes=Array();
            var xcarte=Array()
            var ycarte=Array()

            for (i=0;i< topz ;i++) { 

                c=document.getElementById("carte"+i.toString());
                if (i==0) {var rect = c.getBoundingClientRect();}
                c.style.top = 140+yoffset + (i)*50 + "px";
                c.style.left =xoffset + (i)*50 + "px";
                c.style.zIndex=i;
                cartes.push(c);
                AssociationEvnt(cartes[i]);
            }



            function AssociationEvnt(carte) {
              var X=0, Y=0,dernierX = 0, dernierY = 0;
              carte.onmousedown = (e) => dragMouseDown(carte,e);
              //carte.onmouseout  =  (e)=> closeDragElement(carte)
              // clic droit : on détache la carte de l'axe
              carte.oncontextmenu = (e)=> {
                   if (carte.childNodes.length>=3) {carte.removeChild(carte.childNodes[2])}
                   carte.childNodes[1].innerHTML="";
               }
              }

              function dragMouseDown(carte,e) {
                e = e || window.event;
                e.preventDefault();
                // get the mouse cursor position at startup:
                carte.style.zIndex=topz;
                topz=topz+1;
              
                dernierX = e.clientX;
                dernierY = e.clientY;
                carte.onmouseup = (e) => closeDragElement(carte);
                // call a function whenever the cursor moves:
                carte.onmousemove = (e) => elementDrag(carte,e);
              }

              function elementDrag(carte,e) {
                nc=parseInt(carte.id.substring(5));
                e = e || window.event;
                e.preventDefault();
                // calculate the new cursor position:
                X = dernierX - e.clientX;
                Y = dernierY - e.clientY;
                dernierX = e.clientX;
                dernierY = e.clientY;
                // set the element's new position:
                carte.style.top = Math.min(tableau.offsetHeight,   Math.max (  axe.offsetTop+10,(carte.offsetTop - Y)     )   ) + "px";
                w=carte.offsetWidth/2;  
                carte.style.left = Math.max(axe.offsetLeft-w, Math.min (axe.offsetWidth+axe.offsetLeft-w, carte.offsetLeft - X) ) + "px";
                v=carte.childNodes[1];
                    
                valeur=( xmin +(carte.offsetLeft+w-axe.offsetLeft)/axe.offsetWidth*( xmax - xmin ));
                valeur = Math.round( valeur/ precision ) * (precision)  ;
                if (v.innerHTML==""){
                    verticale=document.createElement("div");
                    verticale.style.position="absolute";
                    verticale.style.top=axe.offsetTop-carte.offsetTop;
                    verticale.style.height=carte.offsetTop-axe.offsetTop;
                    verticale.style.left=w;
                    verticale.style.background='#b295ff';
                    verticale.style.border="1px solid #b295ff";
                    carte.appendChild(verticale);
                }
                else 
                   {
                    carte.lastChild.style.top=axe.offsetTop-carte.offsetTop;
                    carte.lastChild.style.height=carte.offsetTop-axe.offsetTop;
                }
                if (precision<1){ nb_c = -1*Math.floor(Math.log10(precision)) ; v.innerHTML=valeur.toFixed(nb_c); }
                else { v.innerHTML=valeur;}
                
              }

              function closeDragElement(carte) {
                // stop moving when mouse button is released:
                carte.onmouseup = null;
                carte.onmousemove = null;
              }


            $(document).on('click', ".show_axe_correction" , function (event) {
         
                    event.preventDefault();

                    let loop           = $(this).data("loop") ;

                    let valeurs = [] ;
                    for (let i=0 ; i < $(".carte").length ; i++)
                    {
                        valeurs.push( $("#valeur"+i).text() );
                    }


                    event.preventDefault();   
                    my_form = document.querySelector("#all_types_form");
                    var form_data = new FormData(my_form); 
         
                    let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
                    let supportfile_id = $(this).data("supportfile_id") ;

                    form_data.append("supportfile_id" , supportfile_id); 
                    form_data.append("valeurs" , valeurs);
                    form_data.append("loop" , loop); 
                    form_data.append("csrfmiddlewaretoken" , csrf_token); 

                    $.ajax(
                        {
                            type: "POST",
                            dataType: "json",
                            traditional : true,
                            data: form_data,
                            url: "../../check_axe_answers",
                            success: function (data) {
                                $("#score").val(data.score);
                                $("#numexo").val(data.numexo);
                                $("#score_span").html(data.score);
                                $("#numexo_span").html(data.numexo);
                                //********** Gestion de la div de solution ********************
                                $("#show_correction"+loop).show(500);
                                $("#this_correction_text"+loop).html(data.this_correction_text);
                                $("#message_correction"+loop).html(data.msg);
                                //*************************************************************
                                MathJax.Hub.Queue(["Typeset",MathJax.Hub]);    
                            },
                        cache: false,
                        contentType: false,
                        processData: false
                        }
                    )
                 });



    });

});

 
