define(['jquery',  'bootstrap', 'websocket' ], function ($) {
    $(document).ready(function () {
 
        console.log(" ajax-real-time-parcours chargé "); 
 

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




        function PostMessage(id){  //id = destinataire du message
            console.log("entree dans postMesssage");
            console.log( id ,  $("#champ"+id).val() );
            socket.send(JSON.stringify(
               {"command":"teacher_message",
                 "to" : id,
                "message": $("#champ"+id).val() }));
                console.log("message envoyé");
                 document.getElementById("champ"+id).value = ""; 
            };



        $("body").on('change', "#entreechat", function (event) {

            console.log("entree dans postMesssageGeneral");
            socket.send(JSON.stringify(
                {"command":"teacher_message_general",
                 "message": $("#entreechat").val() }));
                 console.log("message général envoyé"); 
                 document.getElementById("entreechat").value = "";          
             
        }) ;



 
    
 

          // Correctly decide between ws:// and wss://
          var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
          var ws_path = ws_scheme + '://' + window.location.host + "/qcm/tableau/";
          console.log("tentative connexion to " + ws_path);
          window.socket = new WebSocket(ws_path); // window pour rendre globale la variable
          socket.onopen = function () {
              console.log("Connected to socket");
              socket.send(JSON.stringify({
              "command":"teacher_join", 
              "parcours": parcours_id ,
              "students":"{% for student in  students %}{{student.user.id}}|{% endfor %}"}));
              console.log("commande teacher join envoyée");
          };


 

 

                    // Handle incoming messages
           socket.onmessage = function (message) {
           // Decode the JSON
           console.log("Got websocket message " + message.data);
           var data = JSON.parse(message.data);
           // Handle errors
           if (data.error) {
             alert(data.error);
             return;
             }

            console.log(data) ; 



           if (data.type=="autojoin")
           // connexion du prof
            {
                console.log("connexion du prof ok");
            }
           else if (data.type=="connexion")
            {console.log("connexion d'un eleve");
             ligne=document.getElementById("tr_student_"+data.from)
             console.log("type table : "+ligne.nodeName)
             $("#tr_student_"+data.from).find("td:first").addClass("live");
             ligne.childNodes[1].innerHTML=ligne.childNodes[1].innerHTML+
             "<p><input type=\"text\" id='champ"+data.from+"' data-from_id="+data.from+" placeholder='message privé' required class='this_student_rt' /></p>";

             //ligne[1].innerHTML=data.message;
            }
            else if (data.type=="message") {
              console.log(data.from+" a envoyé un message");
              var t=document.getElementById("chat");             
              t.innerHTML = t.innerHTML + "<p style='color:red'>"+ data.name+"</p><p style='text-align:right'>"+ data.message+"</p>";
                      
              }// Deconnexion  
            // else if (data.type=="déconnexion") {
            //     console.log(data.from+" s'est déconnecté");
                //$("#room-" + data.leave).remove();
            //      var t=document.getElementById(data.de);
            //      t.textContent=data.last_name+ "(Déconnecté)";
            //     }
            //    }


            else if (data.type=="déconnexion") {
                 console.log(data.from+" s'est déconnecté");
              ligne=document.getElementById("tr_student_"+data.from);
              console.log("type table : "+ligne.nodeName);
              ligne.childNodes[1].innerHTML=data.name;
                }
        }


        // Helpful debugging

            socket.onclose = function () {
                        console.log("Disconnected from chat socket");
                    };
 

    });
});