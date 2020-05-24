define(['jquery', 'bootstrap','moment', 'fullcalendar'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-schedule-group.js OK");




				$(".calendar").fullCalendar({
	                header: {
		                      left: 'prev,next today',
		                      center: 'title',
		                      right: 'month,agendaWeek,agendaDay'
	                  		},
					editable: true,
                 	selectable: true,
                 	selectHelper: true,
					eventLimit : true,
					eventStartEditable : true, 
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
      				events: '/group/events_json_group',
				}) ;




				
	}); 

})

			
           