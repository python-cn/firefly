from __future__ import absolute_import
# coding=utf-8
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


class Renderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre class="hljs"><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)


renderer = Renderer()
Markdown = mistune.Markdown(renderer=renderer)
