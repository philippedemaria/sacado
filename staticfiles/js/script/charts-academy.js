define(['jquery','bootstrap_popover', 'bootstrap','chart'], function ($) {
$(document).ready(function () {
 
 
        console.log("---- NEW test ajax-accueil.js ---") ;  

 

         // *************************************************************
        // chart.js
        // *************************************************************
        var marksCanvas   = document.getElementById("marksChart");
        var scoreswRadar      = document.getElementById("scoreswRadar").value;
        var waitingsRadar      = document.getElementById("waitingsRadar").value;

        var liste_score_w_n = [] ; 
        liste_score_w = scoreswRadar.split("-");
        liste_score_w.forEach( (item) =>{ 
            item_int = parseInt(item);
            if (!isNaN(item_int))
                {liste_score_w_n.push(item_int);}
        });


        var marksData = {
            labels: waitingsRadar.split("-") ,
            datasets: [{
                label : "Attendus",
                backgroundColor: "rgb(245,127,197,0.6)",
                data:  liste_score_w_n,
            }]
        };

        var radarChart = new Chart(marksCanvas, {
          type: 'radar',
          data: marksData
        });





        var barChart = document.getElementById("barChart");
        var scoresbarSet = document.getElementById("scoresbarSet").value;
        var datebar      = document.getElementById("datebarSet").value;

        var liste_score_b_n = [] ; 
        liste_score_b = scoresbarSet.split("-");
        liste_score_b.forEach( (item) =>{ 
            item_int = parseInt(item);
            if (!isNaN(item_int))
                {liste_score_b_n.push(item_int);}
        });

 

        var marksDatas = {
            labels: ["Non acquis", "En cours", "A renforcer", "Acquis"],
            datasets: [{
                label : datebar ,
                backgroundColor: ["rgb(254,176,169,0.6)", "rgb(254,244,176,0.6)","rgb(130,197,181,0.6)","rgb(41,153,126,0.6)"],
                data: liste_score_b_n,
                    }] ,           
                options: {
                    responsive: true,
                    label: { display: false }, 
                    title: {display: false},
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
            },

        };

        var radarChart = new Chart(barChart, {
          type: 'bar',
          data: marksDatas
        });

        // *************************************************************
        // *************************************************************
        // *************************************************************



    });
});
 
