define(['jquery','bootstrap_popover',  'bootstrap',  'toggle' ], function ($) {
    // fonctions pour gérer l'apparition d'un élément quand on clique sur un checkbox (ou toggle) todo:vérifier les anciennces et si elles servent encore
 
    $(document).ready(function () { 
    
    function makeItemAppear($toggle, $item) {
        $toggle.change(function () {
            if ($toggle.is(":checked")) {
                $item.hide(500);
            } else {
                $item.show(500);
            }
        });
    }

  

   // $('[data-toggle="popover"]').popover();

  

    function hiddenItem($toggle, $item) {
        $toggle.change(function () {
            if ($toggle.is(":checked")) {
                $item.show(500);
            } else {
                $item.hide(500);
            }
        });
    }

 
    });

});