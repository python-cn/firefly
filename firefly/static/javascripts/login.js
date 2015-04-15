define(['jquery'], function($) {
    function Login() {
        if (!(this instanceof Login)) {
            return new Login();
        }
        this.$modal = $('#login-modal');
        this.$signin = $('.signin');
        this.$signup = $('.signup');

        this._init();
    }

    Login.prototype = {
        constructor: Login,
        _init: function() {
            var self = this;
            this.$signupButton = $('.sign-up-button');
            this.$signinButton = $('.login-button');

            this.$signupButton.click(function(e) {
                self.signupShow();
            });

            this.$signinButton.click(function(e) {
                self.signinShow();
            });

            this.$modal.find('.close').click(function(e) {
                $('#login-modal').addClass('hide');
                this.$signup.off('keyup');
            });
        },

        signinShow: function(){
            this.$modal.removeClass('hide');
            this.$signin.removeClass('hide');
            this.$signup.addClass('hide');
            this.$signup.off('keyup');
        },

        signupShow: function(){
            var self = this;
            this.$modal.removeClass('hide');
            this.$signin.addClass('hide');
            this.$signup.removeClass('hide');
            this.$signup.on('keyup', self.registerEnable);
        },

        registerEnable: function(){
            var EmptyInut = $(this).find('input').filter(
                function() { return $(this).val() == ""; }),
                $registerBtn = $('#signupBtn');
            if (EmptyInut.length) {
                $registerBtn.attr('disabled', 'disabled');
            } else {
                $registerBtn.removeAttr('disabled');
            }
        },
    };
    Login();
    //    return Login;
});
