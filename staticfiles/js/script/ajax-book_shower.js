define(["jquery", "bootstrap"], function ($) {
  $(document).ready(function () {
    console.log("chargement JS ajax-book.js OK");

    $(document).on("click", ".to_projection", function (event) {
      var this_html = $(this).html();
      var this_css_ = $(this).attr("class");
      const this_css = this_css_.replace("to_projection", "");

      var paragraph_id = $(this).data("paragraph_id");
      var this_paragraph_u = $("#this_paragraph" + paragraph_id).attr("class");

      $("#book_shower_page_content").html(this_html);
      $("#book_shower_page_content").removeClass();
      $("#book_shower_page_content").addClass("global_bloc");
      $("#book_shower_page_content").addClass(this_css);
      $(".modal-body").addClass(this_paragraph_u);

      $(".modal-dialog").css("margin-top", "100px");
      $("#book_shower_page_content").css("min-height", "400px");
    });

    var left_height = $(".no_padding_left").height();
    var right_height = $(".no_padding_right").height();

    two_pages_height = Math.max(left_height, right_height);

    $(".no_padding_right").height(two_pages_height);
    $(".no_padding_left").height(two_pages_height);

    $(document).on("change", ".customRange", function (event) {
      var value = $(this).val();
      $("#book_shower_page_content *").css("font-size", value * 12);
      $("#book_shower_page_content").css("line-height", "1.3em");
      $("#book_shower_page_content .bloc_content").css("height", "");
    });

    var init_test = 0;
    $(document).on("change", ".customRangeImage", function (event) {
      var value = $(this).val();

      if (init_test == 0) {
        var height = $("#book_shower_page_content img").height() * 1.2;
        init_test = height;
      } else {
        height = init_test;
      }
      $("#book_shower_page_content img").css("width", "");
      $("#book_shower_page_content img").css("height", height * value);
      $("#book_shower_page_content .bloc_content").css(
        "height",
        height * value + 40
      );
    });

    $(document).on("change", ".customRangeCor", function (event) {
      var value = $(this).val();
      $("#book_shower_correction_content *").css("font-size", value * 12);
      $("#book_shower_correction_content").css("line-height", "1.3em");
      $("#book_shower_correction_content .bloc_content").css("height", "");
    });

    var init_test = 0;
    $(document).on("change", ".customRangeImageCor", function (event) {
      var value = $(this).val();

      if (init_test == 0) {
        var height = $("#book_shower_correction_content img").height() * 1.2;
        init_test = height;
      } else {
        height = init_test;
      }
      $("#book_shower_correction_content img").css("width", "");
      $("#book_shower_correction_content img").css("height", height * value);
      $("#book_shower_correction_content .bloc_content").css(
        "height",
        height * value + 40
      );
    });

    $(document).on(
      "click",
      ".display_correction_complements_div",
      function (event) {
        const source_id = $(this).data("source_id");
        const cor_and_comp = $("#cor_and_comp" + source_id);
        $(".all_cor_and_comp").addClass("no_visu_on_load");
        cor_and_comp.removeClass("no_visu_on_load");
      }
    );

    $(document).on(
      "click",
      ".close_correction_complements_div",
      function (event) {
        const source_id = $(this).data("source_id");
        const cor_and_comp = $("#cor_and_comp" + source_id);
        cor_and_comp.addClass("no_visu_on_load");
      }
    );

    $(document).on(
      "click",
      ".display_correction_bloc_button",
      function (event) {
        let source_id = $(this).data("source_id");
        let type_id = $(this).data("type_id");
        let paragraph_id = $(this).data("paragraph_id");
        let is_correction = $(this).data("is_correction");
        let book_group_id = $(this).data("book_group_id");


        if ($(this).children().first().hasClass("text-secondary")) {
          var status = "off";
        } else {
          var status = "on";
        }

        $("#spinner-" + type_id + "-" + source_id).html(
          "<i class='fa fa-spinner fa-spin'></i>"
        );

        $.ajax({
          type: "POST",
          dataType: "json",
          data: {
            type_id: type_id,
            source_id: source_id,
            is_correction: is_correction,
            status: status,
            book_group_id:book_group_id,
          },
          url: "../../ajax_display_correction_bloc",
          success: function (data) {
            if (type_id == "0") {
              if (is_correction) {
                $("#cc_chapter_cor" + source_id).removeClass(data.nocss);
                $("#cc_chapter_cor" + source_id).addClass(data.css);

                $("#bi-c-circle-fill" + source_id).removeClass(data.nocss);
                $("#bi-c-circle-fill" + source_id).addClass(data.css);

                if (status == "off") {
                  $("#legendcor" + source_id).html("visibles");
                  $("#cc_chapter_cor" + source_id).removeClass("bi-toggle-off");
                  $("#cc_chapter_cor" + source_id).addClass("bi-toggle-on");
                } else {
                  $("#legendcor" + source_id).html("cachés");
                  $("#cc_chapter_cor" + source_id).removeClass("bi-toggle-on");
                  $("#cc_chapter_cor" + source_id).addClass("bi-toggle-off");
                }
                $("#label_cor" + source_id).removeClass(data.nocss);
                $("#label_cor" + source_id).addClass(data.css);

                $(".all_these_blocs_cor").addClass(data.css);
                $(".all_these_blocs_cor").removeClass(data.nocss);
              } else {
                $("#cc_chapter" + source_id).removeClass(data.nocss);
                $("#cc_chapter" + source_id).addClass(data.css);
                $("#label_comp" + source_id).removeClass(data.nocss);
                $("#label_comp" + source_id).addClass(data.css);
                if (status == "off") {
                  $("#cc_chapter" + source_id).removeClass("bi-toggle-off");
                  $("#cc_chapter" + source_id).addClass("bi-toggle-on");
                  $("#legend" + source_id).html("visibles");
                } else {
                  $("#cc_chapter" + source_id).removeClass("bi-toggle-on");
                  $("#cc_chapter" + source_id).addClass("bi-toggle-off");
                  $("#legend" + source_id).html("cachés");
                }
                $("#bi-plus-square-fill" + source_id).removeClass(data.nocss);
                $("#bi-plus-square-fill" + source_id).addClass(data.css);

                $(".all_these_blocs").addClass(data.css);
                $(".all_these_blocs").removeClass(data.nocss);
              }
            } else if (type_id == "1") {
              if (is_correction) {
                $("#cc_page_cor" + source_id).addClass(data.css);
                $("#cc_page_cor" + source_id).removeClass(data.nocss);

                $(".all_these_blocs_cor").addClass(data.css);
                $(".all_these_blocs_cor").removeClass(data.nocss);


                if (status == "off") {
                  $("#cc_page_cor" + source_id).removeClass("bi-toggle-off");
                  $("#cc_page_cor" + source_id).addClass("bi-toggle-on");
                  $(".all_these_blocs_cor").addClass("bi-toggle-on");
                  $(".all_these_blocs_cor").removeClass("bi-toggle-off");
                } else {
                  $("#cc_page_cor" + source_id).removeClass("bi-toggle-on");
                  $("#cc_page_cor" + source_id).addClass("bi-toggle-off");
                  $(".all_these_blocs_cor").addClass("bi-toggle-off");
                  $(".all_these_blocs_cor").removeClass("bi-toggle-on");
                }

              } else {
                $("#cc_page" + source_id).addClass(data.css);
                $("#cc_page" + source_id).removeClass(data.nocss);

                $(".all_these_blocs").addClass(data.css);
                $(".all_these_blocs").removeClass(data.nocss);
                $(".bi-plus-square-fill").addClass(data.csscomp);
                $(".bi-plus-square-fill").removeClass(data.nocsscomp);


                if (status == "off") {
                  $("#cc_page" + source_id).removeClass("bi-toggle-off");
                  $("#cc_page" + source_id).addClass("bi-toggle-on");
                  $(".all_these_blocs").addClass("bi-toggle-on");
                  $(".all_these_blocs").removeClass("bi-toggle-off");

                } else {
                  $("#cc_page" + source_id).removeClass("bi-toggle-on");
                  $("#cc_page" + source_id).addClass("bi-toggle-off");
                  $(".all_these_blocs").addClass("bi-toggle-off");
                  $(".all_these_blocs").removeClass("bi-toggle-on");
                }



              }
            } else if (type_id == "2") {
              if (is_correction) {
                $("#cc_paragraph_cor" + source_id).addClass(data.css);
                $("#cc_paragraph_cor" + source_id).removeClass(data.nocss);

                $(".these_blocs_cor" + paragraph_id).addClass(data.css);
                $(".these_blocs_cor" + paragraph_id).removeClass(data.nocss);

                if (status == "off") {
                  $("#cc_paragraph_cor" + source_id).removeClass("bi-toggle-off");
                  $("#cc_paragraph_cor" + source_id).addClass("bi-toggle-on");
                } else {
                  $("#cc_paragraph_cor" + source_id).removeClass("bi-toggle-on");
                  $("#cc_paragraph_cor" + source_id).addClass("bi-toggle-off");
                }


              } else {
                $("#cc_paragraph" + source_id).addClass(data.css);
                $("#cc_paragraph" + source_id).removeClass(data.nocss);

                $(".these_blocs" + paragraph_id).addClass(data.css);
                $(".these_blocs" + paragraph_id).removeClass(data.nocss);
                $(".bi-plus-square-fill").addClass(data.csscomp);
                $(".bi-plus-square-fill").removeClass(data.nocsscomp);
                if (status == "off") {
                  $("#cc_paragraph" + source_id).removeClass("bi-toggle-off");
                  $("#cc_paragraph" + source_id).addClass("bi-toggle-on");
                } else {
                  $("#cc_paragraph" + source_id).removeClass("bi-toggle-on");
                  $("#cc_paragraph" + source_id).addClass("bi-toggle-off");
                }


              }
            } else if (type_id == "3") {
              if (is_correction) {
                $("#cc_bloc_cor" + source_id).addClass(data.css);
                $("#cc_bloc_cor" + source_id).removeClass(data.nocss);

                if (status == "off") {
                  $("#cc_bloc_cor" + source_id).removeClass("bi-toggle-off");
                  $("#cc_bloc_cor" + source_id).addClass("bi-toggle-on");
                } else {
                  $("#cc_bloc_cor" + source_id).removeClass("bi-toggle-on");
                  $("#cc_bloc_cor" + source_id).addClass("bi-toggle-off");
                }

              } else {
                $("#cc_bloc" + source_id).addClass(data.css);
                $("#cc_bloc" + source_id).removeClass(data.nocss);
                $(".square_fill_bloc"+ source_id).addClass(data.csscomp);
                $(".square_fill_bloc"+ source_id).removeClass(data.nocsscomp);
                if (status == "off") {
                  $("#cc_bloc" + source_id).removeClass("bi-toggle-off");
                  $("#cc_bloc" + source_id).addClass("bi-toggle-on");
                } else {
                  $("#cc_bloc" + source_id).removeClass("bi-toggle-on");
                  $("#cc_bloc" + source_id).addClass("bi-toggle-off");
                }

                
              }
            }
            $("#spinner-" + type_id + "-" + source_id).html("");
          },
        });
      }
    );

    $(document).on("click", ".show_this_bloc_correction", function (event) {
      const bloc_id = $(this).data("bloc_id");
      const this_title_bloc = $("#title_bloc" + bloc_id).html();
      const this_content_html = $(
        "#book_shower_this_correction" + bloc_id
      ).html();

      $("#book_shower_correction_exo").html(this_title_bloc);
      $("#book_shower_correction_content").html(this_content_html);
    });

    $("#stop_fullscreen").hide();
    // fermer le plein écran
    $("#stop_fullscreen").on("click", function () {
      $("#navbarLeft").show(500);
      $("#stop_fullscreen").hide(500);
      $("#start_fullscreen").show(500);
      $("body").css("margin-left", "95px");
      (document.fullScreenElement && null !== document.fullScreenElement) ||
      (!document.mozFullScreen && !document.webkitIsFullScreen)
        ? document.documentElement.requestFullScreen
          ? document.documentElement.requestFullScreen()
          : document.documentElement.mozRequestFullScreen
          ? document.documentElement.mozRequestFullScreen()
          : document.documentElement.webkitRequestFullScreen &&
            document.documentElement.webkitRequestFullScreen(
              Element.ALLOW_KEYBOARD_INPUT
            )
        : document.cancelFullScreen
        ? document.cancelFullScreen()
        : document.mozCancelFullScreen
        ? document.mozCancelFullScreen()
        : document.webkitCancelFullScreen && document.webkitCancelFullScreen();
    });
    // Vue en plein écran
    $("#start_fullscreen").on("click", function () {
      $("#navbarLeft").hide(500);
      $("#stop_fullscreen").show(500);
      $("#start_fullscreen").hide(500);
      $("body").css("margin-left", "0px");
      (document.fullScreenElement && null !== document.fullScreenElement) ||
      (!document.mozFullScreen && !document.webkitIsFullScreen)
        ? document.documentElement.requestFullScreen
          ? document.documentElement.requestFullScreen()
          : document.documentElement.mozRequestFullScreen
          ? document.documentElement.mozRequestFullScreen()
          : document.documentElement.webkitRequestFullScreen &&
            document.documentElement.webkitRequestFullScreen(
              Element.ALLOW_KEYBOARD_INPUT
            )
        : document.cancelFullScreen
        ? document.cancelFullScreen()
        : document.mozCancelFullScreen
        ? document.mozCancelFullScreen()
        : document.webkitCancelFullScreen && document.webkitCancelFullScreen();
    });
  });
});
