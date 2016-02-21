$(document).ready(function () {
    setInterval(function() {
        updateRequests();
    }, 3000);

    var focused = true;
    var title = document.title;
    var recieved_data;

    $(window).blur(function () {
        focused = false;
    });
    $(window).focus(function () {
        focused = true;
        document.title = title;
        // We haven't recived data yet
        if (recieved_data === undefined) return;

        $('#requests').empty();
        for (var i = 0; i < recieved_data.length; i++) {
            var method = recieved_data[i].fields.method;
            var path = recieved_data[i].fields.path;
            var query = recieved_data[i].fields.query;
            var timestamp = recieved_data[i].fields.timestamp;
            var id = recieved_data[i].pk;
            $('#requests').append('<p data-id="' + id + '">' + method + ' ' + path + ' ' + query + ' ' + timestamp + '</p>');
        }
        });

    function updateRequests() {
        $.get(
            '/requests/', {
                'id': $('p').data('id'),
                'store': false
            },
            function(data) {
                if (data.new_requests !== 0 && !focused) {
                    document.title = '{' + data.new_requests + '} ' + title;
                }
                recieved_data = JSON.parse(data.requests);
            }
        );
    }
});
