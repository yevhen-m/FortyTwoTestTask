$(document).ready(function() {
    var $st = $('#status');
    var $inputs = $('input, textarea');

    $('#editForm').ajaxForm(
        {
            beforeSubmit: function() {
                $('.error').remove();
                $st.show();
                $st.text('Loading...');
                $inputs.attr('disabled', 'disabled');
            },
            success: function() {
                $st.show();
                $st.text('Successfully changed!');
                $inputs.removeAttr('disabled');
            },
            error: function(response) {
                var errors = JSON.parse(response.responseText);
                $st.show();
                $st.text('Fix all the errors and try again!');
                for (var input_name in errors) {
                    var $input = $('#id_' + input_name);

                    var input_errors = errors[input_name];
                    for (var i=0; i < input_errors.length; i++) {
                        $input.closest('div').prepend('<p class="error">' + input_errors[i] + '</p>');
                    }
                }
                $inputs.removeAttr('disabled');
            }
        }
    );
});
