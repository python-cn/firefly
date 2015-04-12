require.config({
    baseUrl: '/static/javascripts/components',
});

require(['jquery', 'markdown-it', 'markdown-it-footnote', 'highlight.pack', 'emojify', '../create_topic',
         'codemirror/lib/codemirror', 'codemirror/mode/overlay', 'codemirror/mode/xml/xml',
         'codemirror/mode/markdown/markdown', 'codemirror/mode/gfm/gfm', 'codemirror/mode/javascript/javascript',
         'codemirror/mode/css/css', 'codemirror/mode/django/django', 'codemirror/mode/jinja2/jinja2',
         'codemirror/mode/python/python', 'codemirror/mode/sass/sass', 'codemirror/mode/ruby/ruby',
         'codemirror/mode/shell/shell', 'codemirror/mode/tornado/tornado', 'codemirror/mode/sql/sql',
         'codemirror/mode/yaml/yaml', 'codemirror/mode/yaml/yaml', 'codemirror/mode/htmlmixed/htmlmixed',
         '../login'],
        function($, markdownit, markdownitFootnote, hljs, emojify, createTopic, CodeMirror){
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
                topic = new createTopic();

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

            $('#create-topic').click(function(e) {
                e.preventDefault();
                topic.openModal(function() {
                    $('.CodeMirror').remove();
                    $('#wmd-preview').html('');
                    var editor = CodeMirror.fromTextArea(document.getElementById('wmd-input'), {
                        mode: 'gfm',
                        lineNumbers: false,
                        matchBrackets: true,
                        lineWrapping: true,
                        theme: 'base16-light'
                    });
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

            /* 提交表单 */
        });
