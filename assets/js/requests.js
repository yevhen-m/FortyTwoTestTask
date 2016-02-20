$(document).ready(function () {
    setInterval(function() {
        updateRequests();
    }, 3000);

    var focused;

    $(window).blur(function () {
        focused = false;
    });
    $(window).focus(function () {
        focused = true;
    });
});
