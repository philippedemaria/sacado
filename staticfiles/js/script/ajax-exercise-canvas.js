define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-exercise-canvas.js OK");

 

  ///////////////////////////////////////////////////////
 

        $("#text_zone").on('click', function (){ 
            $("#text_zone_div").removeClass("not_allowed_display");
            $("#canvas_zone_div").addClass("not_allowed_display");
            $(this).removeClass("btn-default").addClass("btn-primary");
            $("#canvas_zone").addClass("btn-default").removeClass("btn-primary");
        })

        $("#canvas_zone").on('click', function (){ 
            $("#text_zone_div").addClass("not_allowed_display");
            $("#canvas_zone_div").removeClass("not_allowed_display");
            $(this).removeClass("btn-default").addClass("btn-primary");
            $("#text_zone").addClass("btn-default").removeClass("btn-primary");
        })

        ///////////////////////////////////////////////////////
        var canvas    = document.getElementById("myCanvas");
        var ctx       = canvas.getContext('2d');
        canvas.width  = 800 //window.innerWidth - 200 ;
        canvas.height = 800 //window.innerHeight - 200;
        var color_code= 0;

        // Couleur
        $("#colorpicker").on("change", function(){    
            ctx.strokeStyle = $(this).val() ;
            color_code++; 
        });
        // Epaisseur de trait
        $("#thickness").on("change", function(){    
            ctx.lineWidth = $(this).val() ;
        });


        var actions = JSON.parse(document.getElementById('this_answer').textContent) ;

        if ( actions == "" ) 
            {
                var actions = "CanvasStyle=" ;
            }

        

        // Effacer tout le canvas
        $("#clear").on("click", function(){    
            ctx.fillStyle = "white";
            ctx.fillRect(0,0,canvas.width,canvas.height);
            actions = "CanvasStyle=" ;
            save_canvas(actions)
        });




        // Ecrire dans le canvas
        $("#myCanvas").on("mouseover", function(){    
            paint('true') ;
        });


        // Effacer une partie
        $("#erasor").on("click", function(){    
            paint('false') ;
        });





        function paint(flag){

            $("#myCanvas").mousedown(function(event){ 
                    ctx.beginPath();

                    $("#myCanvas").mousemove(function(event){
                        
                        var init_x = event.clientX - 136;
                        var init_y = event.clientY - 171 ; 

                        ctx.lineTo(init_x,init_y);
 
                        if (flag =="false"){
                            ctx.strokeStyle = "white" ;
                            actions = actions +"!"+init_x+","+init_y+",w"; //w pour white donc on efface.
                        }
                        else
                        {
 
                            if (color_code == 1) 
                            {
                                color_code--; 
                                actions = actions +"!"+ctx.strokeStyle+","+init_x+","+init_y ;
                                
                            }
                            else
                            { 
                                actions = actions +"!,"+init_x+","+init_y;
                            }

                        }

                        ctx.stroke();

                    })


                    $("#myCanvas").mouseup(function(event){
                        
                        $("#myCanvas").unbind("mousemove");
                        flag = "true" ;
                        actions = actions +"=";
                        ctx.closePath();
                        save_canvas(actions)
                    })

            })

        }


        function save_canvas(actions){

            let customexercise_id = $("#customexercise_id").val();
            let parcours_id       = $("#parcours_id").val();
            let csrf_token        = $("input[name='csrfmiddlewaretoken']").val();
            
            $.ajax({
                type: 'POST',
                url: "../../ajax_save_canvas",
                data: { "actions" : actions ,
                        'customexercise_id': customexercise_id,
                        'parcours_id': parcours_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                dataType: 'json',
                success: function(data) {
                    console.log('Save successfully !');
                }
            });
 
        }
      


        new_color = "#000000" ;
        if (actions !="") {


            segments = actions.split("=");
            segments.forEach( position );


            function position(item) {


                positions = item.split("!") ;
                ctx.strokeStyle = "#000000" ;
        
                ctx.beginPath();
                positions.forEach(create_draw);
                ctx.stroke();
                ctx.closePath(); 


                    function create_draw(itemize,index) {
            
                            if (index > 0) // empeche la récupération de la balise d'entrée
            
                             { 
                                coords = itemize.split(",");
            
                                if (coords[0] != "") 
                                    { new_color = coords[0]; }
            
                                ctx.strokeStyle = new_color ;
      
                                 ctx.lineTo(coords[1],coords[2]);
 
                            }
                        
                        }
        
                }



            }












});

});

