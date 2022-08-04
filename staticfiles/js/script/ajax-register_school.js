$(document).ready(function () {
 
 
    console.log("---- NEW test ajax-register.js ---") ;  
 
  // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#country_id').on('change', function (event) {

            let country_id = $(this).val();

            console.log(country_id) ;
            
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'country_id': country_id,                      
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "/school/chargeschools",
                    success: function (data) {

                        schools = data["schools"];
                        $('select[name=school]').empty("");
                        if (school.length >0)
                        { for (let i = 0; i < schools.length; i++) {
                                    
                                let schools_id = schools[i][0];
                                let schools_name =  schools[i][1]  ;
                                let option = $("<option>", {
                                    'value': Number(schools_id),
                                    'html': schools_name
                                });
                                $('select[name=school]').append(option);
                            }
                        }
                        else
                        {
                            let option = $("<option>", {
                                'value': 0,
                                'html': "Aucun contenu disponible"
                                });
                            $('select[name=school]').append(option);
                        }


                    }
                }
            )
        });

});

 
