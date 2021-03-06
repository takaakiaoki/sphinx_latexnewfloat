r""" latexnewfloat.py extension for latex builder to replace 
literal-block environment by \captionof{LiteralBlockNewFloat}{caption_title} command.

For \captionof command (in capt-of pacakge), the new environment
LiteralBlockNewFloat should be configured by newfloat pagage instead of
original float package.
needspace package is required, and  \literalblockneedspace and \literalblockcaptionaboveskip
are introduced in order to control pagebreak around caption.

Usage:
  add following latex preambles for latex_elements['preamble'] in conf.py
      'preamble': r'''
      % declare new LiteralBlockNewFloat. You may change `name` option
      \DeclareFloatingEnvironment{LiteralBlockNewFloat}
      % confiure additional options
      \SetupFloatingEnvironment{LiteralBlockNewFloat}{name=Listing,placement=h,fileext=loc}
      % change within option in similar to literal-block in sphinx.sty
      \ifx\thechapter\undefined
          \SetupFloatingEnvironment{LiteralBlockNewFloat}{within=section}
      \else
        \SetupFloatingEnvironment{LiteralBlockNewFloat}{within=chapter}
      \fi
      % if the left page space is less than \literalblockneedsapce, insert page-break
      \newcommand{\literalblockneedspace}{5\baselineskip}
      % margin before the caption of literal-block
      \newcommand{\literalblockcaptionaboveskip}{0.5\baselineskip}
      '''
  Run sphinx with builder name 'latexnewfloat'
    python -m sphinx.__init__ -b latexnewfloat {intpudir} {outputdir}
  or
  - add entry in makefile
  - you may also override original latex builder entry using app.set_translator
"""

from sphinx.writers.latex import LaTeXTranslator
from sphinx.builders.latex import LaTeXBuilder

def setup(app):
    app.add_builder(LaTeXNewFloatBuilder)
    app.set_translator('latexnewfloat', LaTeXNewFloatTranslator)
    # uncomment if you want to override stadnard latex builder
    # app.set_translator('latex', LaTeXNewFloatTranslator)

    app.add_latex_package('newfloat')
    app.add_latex_package('capt-of')
    app.add_latex_package('needspace')

    return {'version': '0.3'}

# inherited from LaTeXBuilder
class LaTeXNewFloatBuilder(LaTeXBuilder):
    name = 'latexnewfloat'

# inherited from LaTeXTranslator
class LaTeXNewFloatTranslator(LaTeXTranslator):
    def __init__(self, document, builder):
        LaTeXTranslator.__init__(self, document, builder)
        # flag whether caption is under container[litelal_block=True] node
        self.in_container_literal_block = 0

    def visit_caption(self, node):
        self.in_caption += 1
        if self.in_container_literal_block:
            self.body.append('\\needspace{\\literalblockneedspace}')
            self.body.append('\\vspace{\\literalblockcaptionaboveskip}')
            self.body.append('\\captionof{LiteralBlockNewFloat}{')
        else:
            self.body.append('\\caption{')

    def visit_container(self, node):
        if node.get('literal_block'):
            self.in_container_literal_block += 1
            ids = ''
            for id in self.next_literal_ids:
                ids += self.hypertarget(id, anchor=False)
            if node['ids']:
                ids += self.hypertarget(node['ids'][0])
            self.next_literal_ids.clear()
            self.body.append('\n')
            self.context.append(ids + '\n')

    def depart_container(self, node):
        if node.get('literal_block'):
            self.in_container_literal_block -= 1
            self.body.append(self.context.pop())
