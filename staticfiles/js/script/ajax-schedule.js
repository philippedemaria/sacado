define(['jquery', 'bootstrap','moment', 'fullcalendar'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-schedule.js OK");


 		        $("#alldaydiv").show();
		        $('#is_allday').on('change', function () { 
		            $("#alldaydiv").toggle(500);
		        });

 				$('.update_event_modal').on('click', function () { 
					$('#show_event').modal('hide');
					});



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
					select: function(event) {
	 						$("#new_event").modal('show');
 							$("#id_start").val(event.date_limit.format());
 							$("#id_end").val(event.date_limit.format());
					    },
      				events: '/schedule/events_json',
	                eventDrop: function(event, delta, revertFunc) {

						if (!confirm(event.exercise.knowledge.name + " est déplacé au " + event.date_limit.format()+". Etes-vous sûr de ce changement ?")) {
						      revertFunc();
						    }
						else
						    {
							let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
							$.ajax(
					                {
					                    type: "POST",
					                    dataType: "json",
					                    data: {
					                       'event_id': event.id,
					                       'start_event': event.date_limit.format(),
					                        csrfmiddlewaretoken: csrf_token
					                    },
					                    url: "shift_event" ,
					                    success: function (data) {
		 									console.log("OK");
					                    }
					                }
					            )
						    }

						  },
					eventClick: function(event, element) {


            			let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

							$.ajax(
					                {
					                    type: "POST",
					                    dataType: "json",
					                    data: {
					                       'event_id': event.id,
					                        csrfmiddlewaretoken: csrf_token
					                    },
					                    url: "show_event" ,
					                    success: function (data) {
					                    $("#formulaire").html("").append(data.html); 
					                    }
					                }
					            );

					    $("#show_event").modal('show');
 	
					  }
				}) ;


				$('.event_div').hide();
 
 


 









				
	}); 

})

			
           