define(['jquery', 'mousetrap'], function($, Mousetrap) {
    function bindKeyboard(Login) {
        // Go to personal page
        Mousetrap.bind('g i', function() { console.log('go to personal page'); });
        // Bring up this help dialog
        Mousetrap.bind('?', function() {
            var currentUrl = window.location.pathname,
                $close = $('.js-facebox-close'),
                $facebox = $('.facebox'),
                $faceboxOverlay = $('.facebox-overlay');
            $facebox.removeClass('hide');
            $close.click(function(e) {
                $facebox.hide();
                $faceboxOverlay.removeClass('facebox-overlay-active').addClass('hide');
            });
            $.ajax({
                method: 'GET',
                url: '/keyboard',
                async: false,
                data: {url: currentUrl}
            })
                .done(function (res){
                    $('.shortcuts').html(res);
                });
            $faceboxOverlay.removeClass('hide').addClass('facebox-overlay-active');
            var $seeAll = $('.js-see-all-keyboard-shortcuts');
            $seeAll.click(function(e) {
                $('.js-hidden-pane').removeClass('js-hidden-pane');
                $(this).parent().remove();
            });
        });
        // Open register window
        Mousetrap.bind('l r', function() {
            Login.signupShow();
        });
        // Open login window
        Mousetrap.bind('l l', function() {
            Login.signinShow();
        });
        // Logout
        Mousetrap.bind('l t', function() {
            console.log('logout');
        });
        // Close register/login window
        Mousetrap.bind('l c', function() {
            Login.close();
        });

    }
    return bindKeyboard;
})
