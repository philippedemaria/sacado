define(["jquery", "bootstrap"], function ($) {
  $(document).ready(function () {
    console.log("chargement JS ajax-parcours_shared.js OK");

    $("select[name=theme]").on("change", function (event) {
      if ($("select[name=level]").val() > 0) {
        ajax_choice($("select[name=level]"), $("select[name=theme]"));
      } else {
        alert("Vous devez choisir un niveau.");
        return false;
      }
    });

    $("select[name=level]").on("change", function (event) {
      ajax_choice($("select[name=level]"));
    });

    function ajax_choice(param0) {
      if (param0.val() > 0) {
        var level_id = param0.val();
      } else {
        var level_id = 0;
      }

      let subject_id = $("#id_subject").val();
      let keywords = $("#keywords").val();
      let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

      $("#loader").html("<i class='fa fa-spinner fa-pulse fa-10x fa-fw'></i>");

      let listing = "no";
      if ($("#listing")) {
        if ($("#listing").is(":checked")) {
          listing = "yes";
        } else {
          listing = "no";
        }
      }

      $.ajax({
        type: "POST",
        dataType: "json",
        traditional: true,
        data: {
          subject_id: subject_id,
          level_id: level_id,
          keywords: keywords,
          listing: listing,
          csrfmiddlewaretoken: csrf_token,
        },
        url: "../../ajax_all_folders",
        success: function (data) {
          $("#courses_details").html("").html(data.html);
          $("#loader").html("").hide();
          $("#before_choice").hide();
          $("#after_choice").show();
          if (listing == "yes") {
            $("#listing").prop("checked", true);
          } else {
            $("#listing").prop("checked", false);
          }
        },
      });
    }

    $("#keywords").on("keyup", function (event) {
      ajax_choice($("select[name=level]"), $("select[name=theme]"));
    });

    $("#listing").on("change", function (event) {
      ajax_choice($("select[name=level]"), $("select[name=theme]"));
    });

    $(document).on("click", "#duplication_document", function (event) {
      var document_id = $(this).data("document_id");
      var document_title = $(this).data("document_title");

      $("#this_document_id").val(document_id);
      $("#this_document_title").html(document_title);
      $("#this_document_label").html(document_title);
    });

    $(document).on("click", "#duplicate_button_action", function () {
      my_form = document.querySelector("#duplicate_form");
      var form_data = new FormData(my_form);

      let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

      $.ajax({
        type: "POST",
        dataType: "json",
        traditional: true,
        data: form_data,
        url: "../../duplicate_folder",
        success: function (data) {
          alert(data.validation);
        },
        cache: false,
        contentType: false,
        processData: false,
      });
    });
  });
});

/* code réalisé par Philippe Demaria - tout droit réservé */
/* code pour sacado */
