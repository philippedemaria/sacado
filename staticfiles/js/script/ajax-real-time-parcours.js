define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 
        console.log(" ajax-real-time-parcours charg!é! "); 
 

        $(".imagefile").on('mouseover', function (event) {
                 $(this).parent().find(".th_real_time_label").addClass("th_real_time_label_hover") ;
                 })

        $(".imagefile").on('mouseout', function (event) {
                 $(this).parent().find(".th_real_time_label").removeClass("th_real_time_label_hover") ;
                 })

 
        let parcours_id = $("#parcours_id").val();


        $("body").on('change', ".this_student_rt", function (event) {

            from_id = $(this).data("from_id") ; 
            PostMessage(from_id) ;
        })




        $("#real_time_div").on('mouseover',   function (event) {
            $(this).animate({height: "100%", }, 750 ) ;
        })


        $("#this_chat_box").on('mouseover',   function (event) {
            $("#real_time_div").animate({height: "100%", }, 750 ) ;
        })

        $("#real_time_div").on('mouseleave',   function (event) {
            $(this).animate({height: "40px", }, 650 ) ;
        })



        function PostMessage(id){  //id = destinataire du message
            socket.send(JSON.stringify(
               {"command":"teacher_message",
                 "to" : id,
                "message": $("#champ"+id).val() }));
                 document.getElementById("champ"+id).value = ""; 
            };



        $("body").on('change', "#entreechat", function (event) {

            socket.send(JSON.stringify(
                {"command":"teacher_message_general",
                 "message": $("#entreechat").val() }));
                 document.getElementById("entreechat").value = "";          
             
        }) ;


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
            //console.log("situation terminee "+ok+","+a+","+t);
            if (t==0) {t=1;a=0;};
            ctx=canvas.getContext("2d");
            if (ok) {ctx.fillStyle="#00FF00";} else {ctx.fillStyle="#FF0000";}
            ctx.fillRect(a*largeur/t,0,largeur/t,hauteur);
            ctx.stroke();
          }
 
         $("body").on('click', ".write_to_student", function (event) {
                 $(this).parent().find(".this_student_rt").toggle() ;
                 })    

          // Correctly decide between ws:// and wss://
          var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
          console.log("test de connexion : " + ws_scheme );
          var ws_path = ws_scheme + '://' + window.location.host + "/qcm/tableau/";
          console.log("test de connexion : " + ws_path );
          window.socket = new WebSocket(ws_path); // window pour rendre globale la variable

          socket.onopen = function () {
              console.log("Connected to socket");
              socket.send(JSON.stringify({
              "command":"teacher_join", 
              "parcours": parcours_id ,
              "students":"{% for student in  students %}{{student.user.id}}|{% endfor %}"}));
          };


                    // Handle incoming messages
          socket.onmessage = function (message) {
                 // Decode the JSON
                 var data = JSON.parse(message.data);
                 // Handle errors
                 if (data.error) {
                   return;
                   }


                 if (data.type=="autojoin")
                 // connexion du prof
                  {
                      console.log("connexion du prof ok; groupe="+data.salle);
                  }
                 else if (data.type=="connexion")
                  { //console.log("connexion d'un eleve");
                   ligne=document.getElementById("tr_student_"+data.from)
                   $("#tr_student_"+data.from).find("td:first").addClass("live");
                   if (ligne.childNodes[1].innerHTML.search("<p><input")==-1)
                        {ligne.childNodes[1].innerHTML=ligne.childNodes[1].innerHTML+
                   "<i class='bi bi-chat-dots write_to_student pull-right'></i>"+
                   "<p><input type=\"text\" id='champ"+data.from+"' data-from_id="+data.from+
                   " placeholder='message privé' required class='this_student_rt no_visu_on_load' /></p>";
                       }
                   //ligne[1].innerHTML=data.message;
                  }
                  else if (data.type=="message") {
                    console.log(data.from+" a envoyé un message");
                    var t=document.getElementById("chat");             
                    t.innerHTML = t.innerHTML + "<div class='this_chat_block'>@"+ data.name+"<br/>"+ data.message+"</div>";
                            
                    }// Deconnexion  

                  else if (data.type=="déconnexion") {
                       //console.log(data.from+" s'est déconnecté");
                    ligne=document.getElementById("tr_student_"+data.from);
                    //console.log("type table : "+ligne.nodeName);
                    ligne.childNodes[1].innerHTML=data.name;
                      }
                  else if (data.type=="ExoDebut") {
                        //console.log(data.from+" a initié l'exo " +data.ide);
                        var canvas=document.getElementById(data.ide+"|"+data.from);
                        barreVierge(canvas);
                      }
                  else if (data.type=="SituationFinie"){
                      //console.log(data.from+" a termine une situation" +data.numexo);
                      var canvas=document.getElementById(data.ide+"|"+data.from)
                      barrePrecis(canvas,data.numexo,data.resultat,data.situation);
                    }
              }


        // Helpful debugging

            socket.onclose = function () {
                        console.log("Disconnected from chat socket");
                    };
 

    });
});
