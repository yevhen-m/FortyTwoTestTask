$(document).ready(function() {
    // bind 'myForm' and provide a simple callback function
    $('#editForm').ajaxForm(function() {
        alert("Thank you for your comment!");
    });
});
