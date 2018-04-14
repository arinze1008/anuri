/**
 * Created by Arinze on 11/14/2016.
 */
$(document).ready(function() {
// JQuery code to be added in here.
    $('#agents').click(function(){
        $.ajax({
            type: "GET",
            url: "/popup/agents/",
            success: function(data) {
                $("#agent_html").empty();
                for (i = 0; i < data.length; i++) {
                    $('.agent_html').append(
                        '<div class="col-md-3">' +
                        '<img src="/static/img/contentimage.png">' +
                        '<span class="text-center link-label2">' + data[i] + '</span></div>'
                    );
                }
            }
        });
    });

    $('.clickable-row').click(function(){
        var id = $(this).data('id');
        $('#id_ticket_id').val(id);
        $('.id_last_note').hide();
        $( ".incidence_report_area" ).fadeIn(1000, function(){
          $.ajax({
              type: "GET",
              url: "/dispatcher/incidence_detail/",
              data: {
               'id': id
               },
              success: function(data) {
                $(".old_acount_detail").empty();
                  for (x in data) {
                    $('.acount_detail').append(
                        // '<tbody>' +
                          '<tr>' +
                            '<th>'+ x +'</th>' +
                            '<td>'+ data[x]  +'</td>' +
                          '</tr>'
                        // '<tbody>'
                    );
                  }
              },
          });
        });
    });

$('.myhistory').click(function(){
    var id = $(this).data('id');
    $('.id_last_note').show();
    $( ".incidence_report_area" ).fadeIn(1000, function(){
      $.ajax({
          type: "GET",
          url: "/dispatcher/dispatch_detail/",
          data: {
           'id': id
           },
          success: function(data) {
          $(".old_acount_detail").empty();
            for (x in data) {
              $('.acount_detail').append(
                  // '<tbody>' +
                    '<tr>' +
                      '<th>'+ x +'</th>' +
                      '<td>'+ data[x]  +'</td>' +
                    '</tr>'
                  // '<tbody>'
              );
                $('.id_last_note').val(data[x]['Dispatcher Note']);
            }
        },
      });
    });

});
    $('#spy').click(function(){
        var toexten = $('#spy').data('toexten');
        var fromexten = $('#spy').data('fromexten');

        $.ajax({
            type: "GET",
            url: "/popup/spy",
            data: { fromexten: fromexten, toexten: toexten },
            beforeSend: function () {
                 $('#myModalLabel').html('<span style="color:green; text-align: center ">Call Spying ...</span>')
                   $('#myModal').modal('show')
                       .find($('.modal-body'))
                       .html('<div >' +'<img src="/static/img/spy.png">'
                       +'<span class="text-center ">' +'You can now listen' + '</span></div>');
            },
            success: function(data) {
                 $('#myModal').modal('hide')
            },

        });
    });

    $('#whisper').click(function(){
        var toexten = $('#whisper').data('toexten');
        var fromexten = $('#whisper').data('fromexten');

        $.ajax({
            type: "GET",
            url: "/popup/whisper",
            data: { fromexten: fromexten, toexten: toexten },
            beforeSend: function () {
                 $('#myModalLabel').html('<span style="color:green; text-align: center ">Call Whispering ...</span>')
                   $('#myModal').modal('show')
                       .find($('.modal-body'))
                       .html('<div >' +'<img src="/static/img/spy.png">'
                       +'<span class="text-center ">' +'You can now listen' + '</span></div>');
            },
            success: function(data) {
                 $('#myModal').modal('hide')
            },

        });
    });

    $('#barge').click(function(){
        var toexten = $('#barge').data('toexten');
        var fromexten = $('#barge').data('fromexten');

        $.ajax({
            type: "GET",
            url: "/popup/barge",
            data: { fromexten: fromexten, toexten: toexten },
            beforeSend: function () {
                 $('#myModalLabel').html('<span style="color:green; text-align: center ">Call Barging ...</span>')
                   $('#myModal').modal('show')
                       .find($('.modal-body'))
                       .html('<div >' +'<img src="/static/img/spy.png">'
                       +'<span class="text-center ">' +'You can now listen' + '</span></div>');
            },
            success: function(data) {
                 $('#myModal').modal('hide')
            },

        });
    });

    // $('.coll').click(function(){
    //     alert('cjkdskd');
    //     alert(toexten);
    //     // $.ajax({
    //     //     type: "GET",
    //     //     url: "/popup/hang_up",
    //     //     data: { toexten: toexten },
    //     //     beforeSend: function () {
    //     //          $('#myModalLabel').html('<span style="color:green; text-align: center ">Hanging Up ...</span>')
    //     //            $('#myModal').modal('show')
    //     //                .find($('.modal-body'))
    //     //                .html('<div >'+'<span class="text-center ">' +'Call ending' + '</span></div>');
    //     //     },
    //     //     success: function(data) {
    //     //          $('#myModal').modal('hide')
    //     //     },
    //     //
    //     // });
    // });

    $('#hangup').click(function(){
        var chan = $('#id_channel').val();

        $.ajax({
            type: "GET",
            url: "/popup/hangup",
            data: { chan: chan },
            beforeSend: function () {
                 $('#myModalLabel').html('<span style="color:green; text-align: center ">Hanging Up ...</span>')
                   $('#myModal').modal('show')
                       .find($('.modal-body'))
                       .html('<div >'+'<span class="text-center ">' +'Call ending' + '</span></div>');
            },
            success: function(data) {
                 $('#myModal').modal('hide')
            },

        });
    });

    $('#transfer').click(function(){
        var channel = $('#id_channel').val();
        var context = $('#id_channel').val();
        var priority = $('#id_channel').val();
        alert(channel)
        $.ajax({
            type: "GET",
            url: "/popup/transfer",
            success: function(data) {
                    $(".modal-body").empty()
                    for (x in data) {
                         $('#myModalLabel').html('<span style="color:green; text-align: center ">Transfer to Agent ...</span>')
                          $('#myModal').modal('show')
                           .find($('.modal-body')).append(
                                '<a href="#" class ="coll" data-chan=' + channel + ' data-con=' + context +' '+
                                'data-prior=' + priority + ' data-totransfer=' + data[x]["Name"] + '>'+ '<ul class="innerImage"><li>' +
                                '<div class="quick-info boxed bg-blue" data-totransfer=' + data[x]["Name"] + '>' + "Agent " + '<span>'+ data[x]['Name'] + '</span>'+ '</div></li></ul></a>'
                            );
                    }
            },

        });
    });

     var $modal = $(".modal-body");
        $modal.on('click', '.coll', function(){
            var channel = $(this).data('con');
            alert(channel)
            $.ajax({
                type: "GET",
                // url: "/popup/transfer",
                // data: { toexten: toexten },
                success: function() {
                    location.reload(false);
                },

            });

        });
    // $("#id_status").change(function() {
    //     alert("jkdkdk")
    //      var res = $('option:selected', this).text();
    //      if (res == "On-Hold"){
    //          $('.respondent').hide();
    //          $('.myreason').show();
    //      }
    //     else if(res == "Dispatched"){
    //          $('.respondent').show();
    //          $('.myreason').hide();
    //      }
    //     else{
    //          $('.respondent').hide();
    //          $('.myreason').hide();
    //      }
    // });

    $("#id_role").change(function() {
         var res = $('option:selected', this).text();
         $('.agency').hide();
         if (res == "Dispatcher"){
             $('.agency').show();
         }

    });
        
    // $("#id_review_period").change(function() {
    //      var hoax = $('option:selected', this).text();
    //      $('.hoax').hide();
    //      if (hoax == "Days"){
    //          $('.hoax').show();
    //      }
    //
    // });
});
