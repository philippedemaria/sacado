define(['jquery',  'bootstrap' ], function ($) {
  $(document).ready(function () {
    //console.log(" ajax-real-time-parcours chargé.. "); 
    $(".imagefile").on('mouseover', function (event) {
        $(this).parent().find(".th_real_time_label").addClass("th_real_time_label_hover") ;
        })

    $(".imagefile").on('mouseout', function (event) {
        $(this).parent().find(".th_real_time_label").removeClass("th_real_time_label_hover") ;
        })

    var is_open = 0 ;
    $("#this_chat_box").on('click',   function (event) {
       if (is_open%2==0){ $("#real_time_div").animate({height: "100%", }, 750 ) ;}
       else { $("#real_time_div").animate({height: "40px", }, 650 ) ;}
       is_open++;
       })

    function PostMessage(id){  //id = destinataire du message
       socket.send(JSON.stringify(
          {"command":"messageProf",
			"dest" : "e",
           "to"     : id,
           "payload": $("#champ"+id).val() }));
       document.getElementById("champ"+id).value = ""; 
       }
       
       
    // gestion des chats eleves/prof
    var parcours_id = $("#parcours_id").val();
    //  
    $("body").on('change', ".this_student_rt", function (event) {
        from_id = $(this).data("from_id") ; 
        PostMessage(from_id) ;
        })

    $("body").on('change', "#entreechat", function (event) {
        socket.send(JSON.stringify(
          {"command" : "messageProfGeneral",
		  "dest":"a",
          "payload" : $("#entreechat").val() }));
         document.getElementById("entreechat").value = "";          
        }) ;
    $("body").on('click', ".write_to_student", function (event) {
         $(this).parent().find(".this_student_rt").toggle() ;
         })    
   
    function barreVierge(canvas){  //affichage d'une barre grise  
       var largeur=80;
       var hauteur=12;
       ctx=canvas.getContext("2d");
       ctx.fillStyle="#A0A0A0";
       ctx.fillRect(0,0,largeur,hauteur);
       ctx.stroke();
       }
          
    function barrePrecis(canvas,a,ok,t){  //affichage d'un seul rectangle
        var largeur=80;
        var hauteur=12;
        if (t==0) {t=1;a=0;};
        ctx=canvas.getContext("2d");
        if (ok) {ctx.fillStyle="#00FF00";} else {ctx.fillStyle="#FF0000";}
        ctx.fillRect(a*largeur/t,0,largeur/t,hauteur);
        ctx.stroke();
        }
 
       // debut gestion socket
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/qcm/tableau/";
    socket = new WebSocket(ws_path); 
    
    // à l'ouverture du socket : connexion du prof
    socket.onopen = function () {
		console.log("connexion du prof");
        socket.send(JSON.stringify({
        "command":"connexionProf", 
        "dest":"ca",
        "parcours": parcours_id ,
        "students":"{% for student in  students %}{{student.user.id}}|{% endfor %}"}));
         };
	 
    // gestion messages entrants
    socket.onmessage = function (message) {
       var data = JSON.parse(message.data);
       if (data.error) {return;}
       //if (data.type=="autojoin")  // connexion du prof
       //    {console.log("connexion du prof ok");}
       else if (data.type=="connexionEleve"){ // connexion eleve
           console.log("connexion de l'eleve ",data.from," sur l'exo :", data.ide, " de type ",data.typexo);
           ligne=document.getElementById("tr_student_"+data.from);
           $("#tr_student_"+data.from).find("td:first").addClass("live");
           if (ligne.childNodes[1].innerHTML.search("<p><input")==-1){
               //insertion de l'icone chat-dots si le champ de chat est absent
               ligne.childNodes[1].innerHTML=ligne.childNodes[1].innerHTML+
                       "<i class='bi bi-chat-dots write_to_student pull-right selector_image_from_ajax'></i>"+
                       "<p><input type=\"text\" id='champ"+data.from+"' data-from_id="+data.from+
                       " placeholder='message privé' required class='this_student_rt no_visu_on_load' /></p>";
              }
	       			   
		   if (data.typexo=="ggb"){// l'elève commence un exo ggb		  
              var canvas=document.getElementById(data.ide+"|"+data.from);
		      barreVierge(canvas);
			  }
	       else if (data.typexo=="python" || data.typexo=="tapu"){ 
		      var divCase=document.getElementById(data.ide+"|"+data.from);
			  var iconeInitiale=divCase.childNodes[0].outerHTML;
			  divCase.childNodes[0].outerHTML='<i class="fa fa-sm fa-eye text-success selector_image_from_ajax"></i>';
				   
			  AfficheProd=function(){
				 if (divCase.children.length==1){//pas encore de champ dans la case
				    if (data.typexo=="python") {
					   prod=document.createElement("textarea");
				 	   prod.rows=20;
					   prod.cols=40;
					   prod.readonly="readonly";}
					else {
						prod=document.createElement("iframe");
						prod.width=200;
						prod.height=300;
						}
				    divCase.appendChild(prod);
				 }
				 else {divCase.childNodes[1].style.display="initial";}
				 divCase.childNodes[0].outerHTML='<div></div>';
				 divCase.childNodes[0].innerHTML='<i class="fa fa-sm  fa-sync text-info selector_image_from_ajax" title="Rafraichir"></i>\
&nbsp;&nbsp;&nbsp;&nbsp;<i class="fa fa-sm fa-times text-danger selector_image_from_ajax" title="Fermer"></i>';
					    
			     divCase.childNodes[0].onclick=function(){};
			     
			     // gestion bouton raffraichissement : on demande au client eleve sa production
				 divCase.childNodes[0].firstChild.onclick=function(){
					 socket.send(JSON.stringify(
                          {"command":"requestProd",
							"dest"   : "e",
                            "to"     : data.from,
                            "ide"    : data.ide}));
				 }
				 divCase.childNodes[0].firstChild.dispatchEvent(new Event("click"));
				 // gestion bouton close
				 divCase.childNodes[0].lastChild.onclick=function(){
				    if (divCase.children.length>=2)  {divCase.childNodes[1].style.display="None";}
					divCase.childNodes[0].outerHTML='<i class="fa fa-sm fa-eye text-success selector_image_from_ajax"></i>';
					divCase.childNodes[0].onclick=AfficheProd;  
				};
					  
		     } // fin afficheProd 
		      divCase.childNodes[0].onclick=AfficheProd;
           }; // fin traitement python/tapu
		
					      
		  }  // fin traitement connexion eleve
	   else if (data.type=="sendProd"){
		  // reception d'une production python/tapu par un eleve
		  var divCase=document.getElementById(data.ide+"|"+data.from);
		  if (divCase.children.length==2){ //l'element contenant existe bien
			  if (data.typexo=="python") {divCase.childNodes[1].innerHTML=data.payload;}
			  if (data.typexo=="tapu") {divCase.childNodes[1].contentDocument.childNodes[0].childNodes[1].innerHTML=data.payload;}
		  }
	   }
				 
	   else if (data.type=="sendExercise"){ // l'elève a validé son exo et l'a envoyé à la bdd
		   console.log("sendExercise");
		   divCase=document.getElementById(data.ide+"|"+data.from); //la div de la case du tableau
		   divCase.childNodes[0].outerHTML='<i class="fa fa-sm fa-eye text-primary selector_image_from_ajax"></i>';
		   divCase.childNodes[0].onclick=function(){
			   if (divCase.children.length==1){// il n'y a pas de zone deja creee
				     if (data.typexo=="python") {
					     prod=document.createElement("textarea");
				 	     prod.rows=20;
					     prod.cols=40;
					     prod.readonly="readonly";
					 }
				     else {
						 prod=document.createElement("iframe");
						 prod.width=200;
						 prod.height=300;
					 }
					 divCase.appendChild(prod);
					 }
					   
			   if (data.typexo=="python") {divCase.childNodes[1].innerHTML=data.payload;}
			   else if (data.typexo=="tapu") {divCase.childNodes[1].contentDocument.childNodes[0].childNodes[1].innerHTML=data.payload;}
			   divCase.childNodes[0].onclick=function(){
				   if (divCase.childNodes[1].style.display=="none") {divCase.childNodes[1].style.display="initial"}
				   else divCase.childNodes[1].style.display="none";
				   }
			   }  //fin fonction onclick sur oeil bleu 
			}
	   else if (data.type=="deconnexionEleve"){
		   ligne=document.getElementById("tr_student_"+data.from);
	       $("#tr_student_"+data.from).find("td:first").removeClass("live");
           a=ligne.childNodes[1].innerHTML.split("<i class");
	       ligne.childNodes[1].innerHTML=a[0];
	       divCase=document.getElementById(data.ide+"|"+data.from); //la div de la case du tableau
	       if ((data.typexo=="python" || data.typexo=="tapu") && 
	               divCase.childNodes[0].outerHTML != '<i class="fa fa-sm fa-eye text-primary"></i>')
	               {// exo python/tapu, il n'y a pas l'oeil bleu : l'élève n'a pas validé son exo, on met un oeil gris
					divCase=document.getElementById(data.ide+"|"+data.from);
					divCase.childNodes[0].outerHTML='<i class="fa fa-sm fa-eye text-default"></i>';
					if (divCase.children.length>=2) {divCase.childNodes[1].style.display="none";}
		           }
           }
       else if (data.type=="messageEleve"){
           console.log(data.from+" a envoyé un message");
           var t=document.getElementById("chat");             
           if (t !=null) 
               {t.innerHTML = t.innerHTML + "<div class='this_chat_block'># "+ data.name+"<br/>"+ data.payload+"</div>";
               }
		   }
       else if (data.type=="ExoDebut"){
           console.log(data.from+" a initié l'exo " +data.ide);
           var canvas=document.getElementById(data.ide+"|"+data.from);
	       barreVierge(canvas);
           }
       else if (data.type=="SituationFinie"){
            //console.log(data.from+" a termine une situation" +data.numexo);
            var canvas=document.getElementById(data.ide+"|"+data.from)
            barrePrecis(canvas,data.payload.numexo,data.payload.resultat,data.payload.situation);
            }
    }  // fin gestion des messages
	
	//   fermeture du socket en cas de changement de page
	window.onbeforeunload=function(){
	    console.log("fermeture socket");
	    socket.close();
	};
        // Helpful debugging
	socket.onclose = function () {
       console.log("Disconnected from chat socket");
    };
 

    });
});
