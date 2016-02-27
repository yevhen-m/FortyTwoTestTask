$(document).ready(function () {
    setInterval(function() {
        getRequests();
    }, 1000);

    var title = document.title;
    var data_received = true;
    var focused = true;
    var recieved_data;
    var new_requests;

    $(window).blur(function () {
        focused = false;
    });

    $(window).focus(function () {
        document.title = title;
        focused = true;
        new_requests = 0;
    });

    function updateRequests(recieved_data) {
        $('#requests_table').empty();

        for (var i = 0; i < recieved_data.length; i++) {
            var method = recieved_data[i].fields.method;
            var path = recieved_data[i].fields.path;
            var query = recieved_data[i].fields.query;
            var timestamp = recieved_data[i].fields.timestamp;
            var priority = recieved_data[i].fields.priority;
            var id = recieved_data[i].pk;
            $('#requests').append('<p data-id="' + id + '">' + method + ' ' + path + ' ' + query + ' ' + timestamp + '</p>');
            $('#requests_table').append('<tr class="request" data-id="' + id + '">' +
                                        '<td>' + method + '</td>' +
                                            '<td>' + path + '</td>' +
                                                '<td>' + query + '</td>' +
                                                    '<td>' + timestamp + '</td>' +
                                                        '<td>' + priority + '</td>' +
                                                            '</tr>');
        }
    }

    function getRequests() {
        if (!data_received) return;
        // When we get data, so we want to ensure, that data has been recieved
        // before we get it again
        data_received = false;

        $.ajax({
            type: 'GET',
            url: '/requests/',
            data: {
                'id': $('tr.request').data('id'),
                'store': false
            },
            success: function(data) {
                if (data.new_requests !== 0 && !focused) {
                    // Increment new requests counter in the title of unfocused page
                    new_requests += data.new_requests;
                    document.title = '(' + new_requests + ') ' + title;
                }
                var recieved_data = JSON.parse(data.requests);
                // Update the page content with recieved requests
                updateRequests(recieved_data);
                // We can get more requests, cause we have updated the content of the page
                data_received = true;
            },
            error: function() {
                data_received = true;
            }
        });
    }
});
