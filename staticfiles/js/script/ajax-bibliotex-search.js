define(["jquery", "bootstrap"], function ($) {
  $(document).ready(function () {
    console.log("chargement JS ajax-bibiotex.js OK");

    $("#id_level").on("change", function () {
      let id_level = $(this).val();
      let id_subject = $("#id_subject").val();
      if (id_subject == "" || id_subject == " ") {
        alert("Sélectionner un enseignement");
        return false;
      }

      if (id_level == "" || id_level == " ") {
        alert("Sélectionner un niveau");
        return false;
      }
      let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

      url_ = "ajax_search_bibliotex_by_level";
      if ($("#id_annale").is(":checked")) {
        var is_annale = "yes";
      } else {
        var is_annale = "no";
      }
      let keyword = $("#keywords").val();

      if ($("#loading")) {
        $("#loading").html(
          "<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>"
        );
      }

      $.ajax({
        type: "POST",
        dataType: "json",
        traditional: true,
        data: {
          id_level: id_level,
          id_subject: id_subject,
          is_annale: is_annale,
          keyword: keyword,
          csrfmiddlewaretoken: csrf_token,
        },
        url: url_,
        success: function (data) {
          $("#bibliotex_details").html(data.html);
          $("#loading").html();
          themes = data["themes"];
          $("select[name=theme]").empty("");

          if (themes.length > 0) {
            for (let i = 0; i < themes.length; i++) {
              let themes_id = themes[i][0];
              let themes_name = themes[i][1];
              let option = $("<option>", {
                value: Number(themes_id),
                html: themes_name,
              });
              $("select[name=theme]").append(option);
            }
          } else {
            let option = $("<option>", {
              value: 0,
              html: "Aucun contenu disponible",
            });
            $("select[name=theme]").append(option);
          }

          if (id_level == 9 || id_level == 11 || id_level == 12) {
            $("#is_annale").show(500);
            $("#keyword_div").addClass("col-md-6");
            $("#keyword_div").removeClass("col-md-3");
            $("#theme_div").addClass("col-md-6  col-lg-3");
            $("#theme_div").removeClass("col-md-3  col-lg-4");

            $("#level_div").addClass("col-md-4");
            $("#level_div").removeClass("col-md-3");
            $("#subject_div").addClass("col-md-5");
            $("#subject_div").removeClass("col-md-3");
          } else {
            $("#is_annale").hide(500);
            $("#keyword_div").addClass("col-md-3");
            $("#keyword_div").removeClass("col-md-6");
            $("#theme_div").addClass("col-md-3 col-lg-4");
            $("#theme_div").removeClass("col-md-6 col-lg-3");

            $("level_div").removeClass("col-md-4");
            $("#level_div").addClass("col-md-3");
            $("#subject_div").removeClass("col-md-5");
            $("#subject_div").addClass("col-md-3");
          }
        },
      });
    });

    $(document).on("change", "#id_theme", function () {
      if ($("select[name=level]").val() > 0) {
        ajax_choice($("select[name=level]"), $("select[name=theme]"));
      } else {
        alert("Vous devez choisir un niveau.");
        return false;
      }
    });

    function ajax_choice(param0, param1) {
      let level_id = param0.val();
      let theme_id = param1.val();
      let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
      let subject_id = $("#id_subject").val();
      let keyword = $("#keywords").val();
      url = "ajax_search_bibliotex";
      if ($("#id_annale").is(":checked")) {
        var is_annale = "yes";
      } else {
        var is_annale = "no";
      }

      if ($("#loading")) {
        $("#loading").html(
          "<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>"
        );
      }

      $.ajax({
        type: "POST",
        dataType: "json",
        traditional: true,
        data: {
          level_id: level_id,
          subject_id: subject_id,
          keyword: keyword,
          theme_id: theme_id,
          is_annale: is_annale,
          csrfmiddlewaretoken: csrf_token,
        },
        url: url,
        success: function (data) {
          $("#bibliotex_details").html("").html(data.html);
          $("#loading").html();
        },
      });
    }

    $(document).on("keyup", "#keywords", function () {
      const level_id = $("#id_level").val();
      const subject_id = $("#id_subject").val();
      const keyword = $("#keywords").val();
      const theme_id = $("#id_theme").val();
      const csrf_token = $("input[name='csrfmiddlewaretoken']").val();

      console.log("keywords : ", keyword);

      const is_annale = $("#id_annale").is(":checked") ? "yes" : "no";

      if ($("#loading")) {
        $("#loading").html(
          "<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>"
        );
      }

      if (keyword.length > 3) {
        console.log(keyword + " 3 LETTRES");
        $.ajax({
          type: "POST",
          dataType: "json",
          traditional: true,
          data: {
            level_id: level_id,
            subject_id: subject_id,
            keyword: keyword,
            theme_id: theme_id,
            is_annale: is_annale,
            csrfmiddlewaretoken: csrf_token,
          },
          url: "ajax_search_bibliotex",
          success: function (data) {
            $("#bibliotex_details").html(data.html);
            $("#loading").html("");
          },
          error: function (xhr, status, error) {
            console.error("Erreur AJAX:", status, error);
            $("#loading").html(""); // Efface le loader en cas d'erreur
          },
        });
      }
    });

    $(document).on("change", "#id_annale", function (event) {
      if ($(this).is(":checked")) {
        var is_annale = "yes";
      } else {
        var is_annale = "no";
      }

      let id_level = $("#id_level").val();
      if (id_level == "" || id_level == " ") {
        alert("Sélectionner un niveau");
        return false;
      }
      let id_subject = $("#id_subject").val();
      let bibliotex_id = $("#bibliotex_id").val();
      let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
      let keyword = $("#keywords").val();
      url_ = "ajax_search_bibliotex";

      if ($("#loading")) {
        $("#loading").html(
          "<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i>"
        );
      }

      $.ajax({
        type: "POST",
        dataType: "json",
        traditional: true,
        data: {
          level_id: id_level,
          subject_id: id_subject,
          bibliotex_id: bibliotex_id,
          is_annale: is_annale,
          keyword: keyword,
          csrfmiddlewaretoken: csrf_token,
        },
        url: url_,
        success: function (data) {
          $("#bibliotex_details").html("").html(data.html);
          $("#loading").html();
        },
      });
    });

    $(document).on("click", "#duplication_document", function (event) {
      var document_id = $(this).data("document_id");
      var document_title = $(this).data("document_title");

      $("#this_document_id").val(document_id);
      $("#this_document_title").html(document_title);
      $("#this_document_label").html(document_title);
    });

    $(document).on("click", "#duplicate_button_action", function () {
      event.preventDefault();
      my_form = document.querySelector("#duplicate_form");
      var form_data = new FormData(my_form);

      let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

      $.ajax({
        type: "POST",
        dataType: "json",
        traditional: true,
        data: form_data,
        url: "exercise_bibliotex_duplicate",
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
