(function ($) {
    "use strict";

    jQuery(document).ready(function ($) {
        $(document).on('submit', '#contact_form', function (e) {
            e.preventDefault();
            var name = $('#name').val();
            var email = $('#email').val();
            var message = $('#message').val();

            if (name && email && message) {
              
                        $('#contact_form').children('.email-success').remove();
                        $('#contact_form').prepend('<span class="row alert alert-success email-success">پیام شما با موفقیت ارسال شد</span>');
                        $('#name').val('');
                        $('#email').val('');
                        $('#message').val('');
                        $('.email-success').fadeOut(3000);
                    
                
            } else {
                $('#contact_form').children('.email-success').remove();
                $('#contact_form').prepend('<span class=" row alert alert-danger email-success">کل فیلد ها را پرکنید</span>');
                $('.email-success').fadeOut(3000);
            }

        });
    })

}(jQuery));