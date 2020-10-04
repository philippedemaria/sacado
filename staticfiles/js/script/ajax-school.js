define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-school.js OK");

        

 




        $("input:checkbox.select_radio").on('click', function (event) {

            let counter = $(this).attr("data-counter");

            $("input:checkbox.choice"+counter).not($(this)).removeAttr("checked");

            $(this).attr("checked", $(this).attr("checked"));    

        });











    });
 
});

