define(['jquery', 'bootstrap','moment', 'fullcalendar'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-schedule-dashboard.js OK");

 

				$(".calendar").fullCalendar({
 
 
					monthNames: ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet',
                              'Août','Septembre','Octobre','Novembre','Décembre'],
                    monthNamesShort: ['Janv.','Févr.','Mars','Avr.','Mai','Juin','Juil.','Août','Sept.','Oct.','Nov.','Déc.'],
                    dayNames: ['Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi'],
                    dayNamesShort: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],

	                firstDay:1, // Lundi premier jour de la semaine
	                buttonText: {
	                      today:    'Aujourd\'hui',
	                      month:    'Mois',
	                      week:     'Semaine',
	                      day:      'Jour'
	                  },
					 
      				events: '/schedule/events_json',
	               

				}) ;
				
			}); 

})

			
           