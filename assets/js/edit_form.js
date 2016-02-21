$(document).ready(function() {
    var $st = $('#status');

    $('#editForm').ajaxForm(
        {
            beforeSubmit: function() {
                // disable inputs
            },
            success: function() {
                $st.show();
                $st.text('Successfully changed!');
            },
            error: function() {
                $st.show();
                $st.text('There was an ERROR!');
            }
        }
    );
});
