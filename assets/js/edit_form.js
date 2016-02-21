$(document).ready(function() {
    var $st = $('#status');

    $('#editForm').ajaxForm(
        {
            beforeSubmit: function() {
                $('.error').remove();
            },
            success: function() {
                $st.show();
                $st.text('Successfully changed!');
            },
            error: function(response) {
                var errors = JSON.parse(response.responseText);
                console.log(errors);
                $st.show();
                $st.text('There was an ERROR!');
                for (var input_name in errors) {
                    var $input = $('#id_' + input_name);

                    var input_errors = errors[input_name];
                    for (var i=0; i < input_errors.length; i++) {
                        $input.closest('div').prepend('<p class="error">' + input_errors[i] + '</p>');
                    }
                }
            }
        }
    );
});
