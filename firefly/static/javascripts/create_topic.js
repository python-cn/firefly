define(['jquery', 'sweetAlert', 'select2', 'listItems'], function(
  $, sweetAlert, select2, EffecktListItems) {
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
      var _this = this;
      this.$toggleDiv = $('.toggle-preview');
      this.$cancel = $('.cancel');
      this.$toggler = $('.toggler');
      this.$createButton = $('.create');

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

      this.$createButton.click(function(e) {
        _this.create();
      });

      _this.initCategories();
    },

    initCategories: function() {
      $("select.category-combobox").select2({
        placeholder: 'Categories...',
        ajax: {
          url: '/api/categories',
          dataType: 'json',
          delay: 0,
          data: function (params) {
            return {name: params.term}
          },
          processResults: function (data, params) {
            var result = {results: []};
            if (!data.status) {
              result.results = data.categories;
            }
            return result;
          },
          cache: true
        },
        escapeMarkup: function (markup) { return markup; },
        minimumInputLength: 0,
        templateResult: function (category) {
          if (!category.name) { return 'Loading...'; }
          var markup = '<div>' + category.name;
          if (category.description) {
            markup += '<br>' + category.description;
          }
          markup += '</div>';
          return $(markup)
        },
        templateSelection: function (category) {
          return category.name;
        }
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

    create : function(){
      var title = $('#reply-title').val();
      var _this = this;
      var params, content = [];
      var category = $('#reply-category').val();
      var items = EffecktListItems();

      $('.CodeMirror-code pre span[style]').each(
        function () {
          var text = $(this).text();
          content.push(text);
        }
      );

      if (!title.length) {
        sweetAlert({
          title: "标题没有内容",
          type: "error"
        });
        return
      }
      if (!(category && category.length)) {
        sweetAlert({
          title: "请选择分类",
          type: "error"
        });
        return
      }
      if (!content.length) {
        sweetAlert({
          title: "正文内容太少",
          type: "error"
        });
        return
      }
      params = {
        'title': title,
        'content': content.join('\n'),
        'category': category
      };
      $.ajax({
        type: 'POST',
        url: '/create/topic',
        traditional: true,
        data: params,
        dataType: "json",
        success: function(res) {
          if (!res.ok) {
            _this.closeModal();
            items.addListItem(res.html, $('.topic-list-item:first'));
          }
        }
      });
    }
  };
  return createTopic;
});
