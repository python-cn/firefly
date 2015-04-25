define(['jquery', 'mousetrap'], function($, Mousetrap) {
  function bindKeyboard(Login) {
    // Go to personal page
    Mousetrap.bind('g i', function() { console.log('go to personal page'); });
    // Bring up this help dialog
    Mousetrap.bind('?', function() {
      var currentUrl = window.location.pathname;
      var $close = $('.js-facebox-close');
      var $facebox = $('.facebox');
      var $faceboxOverlay = $('.facebox-overlay');
      $facebox.removeClass('hide');
      $close.click(function(e) {
        closeHelp();
      });
      $.ajax({
        method: 'GET',
        url: '/keyboard',
        async: false,
        data: {url: currentUrl},
        success: function (res) {
          $('.shortcuts').html(res);
        }
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
      closeHelp();
      Login.signupShow();
    });
    // Open login window
    Mousetrap.bind('l l', function() {
      closeHelp();
      Login.signinShow();
    });
    // Logout
    Mousetrap.bind('l t', function() {
      closeHelp();
      console.log('logout');
    });
    // Close register/login window
    Mousetrap.bind('l c', function() {
      Login.close();
    });
    // Close dialog
    Mousetrap.bind('esc', function() {
      closeHelp();
      Login.close();
    });
  }

  function closeHelp() {
    var $facebox = $('.facebox');
    var $faceboxOverlay = $('.facebox-overlay');
    $facebox.addClass('hide');
    $faceboxOverlay.removeClass('facebox-overlay-active').addClass('hide');
  }
  return bindKeyboard;
})
