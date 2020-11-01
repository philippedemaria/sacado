define(['jquery','bootstrap_popover', 'bootstrap','ui', 'ui_sortable'  ], function ($) {
    
    $(document).ready(function () {

        $("#sortable-row").sortable();      
         //$('[data-toggle="popover"]').popover();

    // enregistrement de l'ordre des items dont l'ordre est réarrangable
    function saveOrder() {
        var selectedLanguage = new Array();
        $('ul#sortable-row li').each(function () {
            selectedLanguage.push($(this).attr("id"));
        });
        document.getElementById("row_order").value = selectedLanguage;
    }



    function AjaxsaveOrder() {
        var selectedLanguage = new Array();
        $('ul#sortable-ligne li').each(function () {
            selectedLanguage.push($(this).attr("id"));
        });
        var xhr = getXhr();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                leselect = xhr.responseText;
            }
        };
        xhr.open("POST", "./sql/questionAction.php?a=4", true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send("row_order=" + selectedLanguage);
    }

    });

});