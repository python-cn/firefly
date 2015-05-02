require(['jquery', 'components/markdown-it', 'components/markdown-it-footnote',
         'components/highlight.pack', 'components/emojify',
         'create_comment', 'components/codemirror/lib/codemirror',
         'components/codemirror/mode/overlay', 'components/codemirror/mode/xml/xml',
         'components/codemirror/mode/markdown/markdown', 'components/codemirror/mode/gfm/gfm',
         'components/codemirror/mode/javascript/javascript', 'components/codemirror/mode/css/css',
         'components/codemirror/mode/django/django', 'components/codemirror/mode/jinja2/jinja2',
         'components/codemirror/mode/python/python', 'components/codemirror/mode/sass/sass',
         'components/codemirror/mode/ruby/ruby', 'components/codemirror/mode/shell/shell',
         'components/codemirror/mode/tornado/tornado', 'components/codemirror/mode/sql/sql',
         'components/codemirror/mode/yaml/yaml', 'components/codemirror/mode/yaml/yaml',
         'components/codemirror/mode/htmlmixed/htmlmixed'],
        function($, markdownit, markdownitFootnote, hljs, emojify, createComment, CodeMirror){
          var languageOverrides = {
            js: 'javascript',
            html: 'xml',
            py: 'python',
            rb: 'ruby',
            scss: 'sass',
            yml: 'yaml',
            sh: 'shell',
            md: 'markdown'
          },
              comment = new createComment();

          emojify.setConfig({
            img_dir: '/static/pics/emoji'
          });
          var md = markdownit({
            highlight: function(code, lang){
              if(languageOverrides[lang]) lang = languageOverrides[lang];
              if(lang && hljs.getLanguage(lang)){
                try {
                  return hljs.highlight(lang, code).value;
                }catch(e){}
              }
              return '';
            }
          }).use(markdownitFootnote);

          function update(e){
            var val = e.getValue();
            var out = document.getElementById('wmd-preview');
            var old = out.cloneNode(true);
            out.innerHTML = md.render(val);
            emojify.run(out);
            var allold = old.getElementsByTagName("*");
            if (allold === undefined) {
              return;
            }
            var allnew = out.getElementsByTagName("*");
            if (allnew === undefined) {
              return;
            }
            for (var i = 0, max = Math.min(allold.length, allnew.length); i < max; i++) {
              if (!allold[i].isEqualNode(allnew[i])) {
                out.scrollTop = allnew[i].offsetTop;
                return;
              }
            }
          }

          function updateReplyMeta(cloak) {
            var userName = cloak.find('.username a').text(),
                imgSrc = cloak.find('.topic-avatar img').attr('src'),
                commentId = cloak.data('comment-id'),
                orderId = cloak.data('order-id'),
                $replyTo = $('.reply-to');

            $replyTo.find('a').text('post ' + orderId);
            $replyTo.find('img').attr('src', imgSrc);
            $('.reply-to').find('span').last().text(userName);
            $replyTo.attr('data-comment-id', commentId);
          }

          $('.create').click(function(e) {
            e.preventDefault();
            var $cloak = $(this).closest('.post-cloak');
            comment.openModal(function() {
              $('.CodeMirror').remove();
              $('#wmd-preview').html('');
              var editor = CodeMirror.fromTextArea(document.getElementById('wmd-input'), {
                mode: 'gfm',
                lineNumbers: false,
                matchBrackets: true,
                lineWrapping: true,
                theme: 'base16-light'
              });

              // update reply meta
              updateReplyMeta($cloak);

              editor.on('change', update);
              document.addEventListener('drop', function(e){
                e.preventDefault();
                e.stopPropagation();
                var theFile = e.dataTransfer.files[0];
                var theReader = new FileReader();
                theReader.onload = function(e){
                  editor.setValue(e.target.result);
                };
                theReader.readAsText(theFile);
              }, false);
            });
          });
        });
