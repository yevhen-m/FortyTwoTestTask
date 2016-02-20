$(document).ready(function () {
    setInterval(function() {
        updateRequests();
    }, 5000);

    var focused;

    $(window).blur(function () {
        focused = false;
    });
    $(window).focus(function () {
        focused = true;
    });

    function updateRequests() {
        $.get('/requests', {'id': 1},
              function(data) {
                  console.log(data);
              }
             );
    }
});
