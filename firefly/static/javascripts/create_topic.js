define(['jquery'], function($) {
    function createTopic() {
        if (!(this instanceof createTopic)) {
            return new createTopic();
        }
        this.$inner = $('.textarea-wrapper');
        this.$outer = $('.preview-wrapper');
        this.$modal = $('#reply-control');

        this._init();
    }

    createTopic.prototype = {
        constructor: createTopic,
        _init: function() {
            var self = this;
            this.$toggleDiv = $('.toggle-preview');
            this.$cancel = $('.cancel');
            this.$toggler = $('.toggler');

            this.$toggleDiv.click(function(e) {
                self.previewToggle();
            });

            this.$toggler.click(function(e) {
                e.preventDefault();
                self.close();
            });

            this.$cancel.click(function(e) {
                self.close();
            });
        },

        close: function(){
            this.$modal.addClass('hide');
        },

        open: function(){
            this.$modal.removeClass('hide');
        },

        previewToggle: function(){
            this.$modal.toggleClass('hide-preview');
            if (this.$modal.hasClass('hide-preview') === true) {
                this.$toggleDiv.html('显示预览 »');
            } else {
                this.$toggleDiv.html('« 关闭预览');
            }
        }
    };

    return createTopic;
});
