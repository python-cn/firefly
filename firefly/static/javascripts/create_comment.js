define(['jquery', 'sweetAlert'], function($, sweetAlert) {
  function createComment() {
    if (!(this instanceof createComment)) {
      return new createComment();
    }
    this.$inner = $('.textarea-wrapper');
    this.$outer = $('.preview-wrapper');
    this.$modal = $('#reply-control');

    this._init();
  }

  createComment.prototype = {
    constructor: createComment,
    _init: function() {
      var _this = this;
      this.$toggleDiv = $('.toggle-preview');
      this.$cancel = $('.cancel');
      this.$toggler = $('.toggler');
      this.$replyButton = $('.reply');

      this.$toggleDiv.click(function(e) {
        _this.previewToggle();
      });

      this.$toggler.click(function(e) {
        e.preventDefault();
        _this.closeModal();
      });

      this.$cancel.click(function(e) {
        _this.closeModal();
      });

      this.$replyButton.click(function(e) {
        _this.reply();
      });
    },

    closeModal: function(){
      this.$modal.addClass('hide');
    },

    openModal: function(callback){
      this.$modal.removeClass('hide');
      if (typeof callback !== 'undefined') {
        callback();
      }
    },

    previewToggle: function(){
      this.$modal.toggleClass('hide-preview');
      if (this.$modal.hasClass('hide-preview') === true) {
        this.$toggleDiv.html('显示预览 »');
      } else {
        this.$toggleDiv.html('« 关闭预览');
      }
    },

    reply : function(){
      var _this = this;
      var params, text, content = [];
      $('.CodeMirror-code pre span[style]').each(
        function () {
          text = $(this).text();
          content.push(text);
        }
      );

      if (!content.length) {
        sweetAlert({
          title: "正文内容太少",
          type: "error"
        });
        return
      }
      params = {
        'ref_id': $('.reply-to').data('comment-id'),
        'content': content.join('\n')
      };
      $.ajax({
        type: 'POST',
        url: '/create/comment',
        traditional: true,
        data: params,
        dataType: "json",
        success: function(res) {
          if (!res.ok) {
            sweetAlert({
              title: "发表成功"
            });
            _this.closeModal();
            location.reload();
          }
        }
      });
    }
  };

  return createComment;
});
