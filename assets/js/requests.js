$(document).ready(function () {
    setInterval(function() {
        updateRequests();
    }, 5000);

    var focused;
    var title = document.title;

    $(window).blur(function () {
        focused = false;
    });
    $(window).focus(function () {
        focused = true;
        document.title = title;
    });

    function updateRequests() {
        $.get(
            '/requests/', {
                'id': $('p').data('id'),
                'store': false
            },
            function(data) {
                if (data.new_requests !== 0 && !focused) {
                    document.title = title + ' {' + data.new_requests + '}';
                }
            }
        );
    }
});
