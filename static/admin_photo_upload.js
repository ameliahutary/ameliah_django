(function($) {
    $(document).ready(function() {
        $('.add-row a').click(function() {
            setTimeout(function() {
                var inlineRows = $('.inline-group .form-row:not(:last)');
                inlineRows.each(function() {
                    var row = $(this);
                    var fileInput = row.find('input[type="file"]');
                    var clone = fileInput.clone();
                    fileInput.after(clone);
                });
            }, 100);
        });
    });
})(django.jQuery);
