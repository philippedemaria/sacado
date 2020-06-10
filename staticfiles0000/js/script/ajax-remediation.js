define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-remediation.js OK");

 
            $("#file").hide(500);
 
            function makeItemAppear($toggle, $item, $item2) {
                    $toggle.change(function () {
                        if ($toggle.is(":checked")) {
                            $item.show(500);
                            $item2.hide(500);
                        } else {
                            $item.hide(500);
                            $item2.show(500);
                        }
                    });
                }
   

            makeItemAppear($("#type_choice"), $("#file"), $("#video"));

    });
});