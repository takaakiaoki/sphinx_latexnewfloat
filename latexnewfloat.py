""" latexnewfloat.py extension for latex builder to replace 
literal-block environment by
\captionof{literal-block-newfloat}{caption_title} command.
For \captionof command (in capt-of pacakge), the new environment
literal-block-newfloat should be configured by newfloat pagage instead of
original float package.
Usage:
  add following latex preambles for latex_elements['preamble'] in conf.py 
      'preamble': r'''
      % configure new literal-block-newfloat
      \usepackage{newfloat}
      \DeclareFloatingEnvironment[name={Listing}]{literal-block-newfloat}
      % copy from sphinx.sty
      \ifx\thechapter\undefined
          \SetupFloatingEnvironment{literal-block-newfloat}{within=section,placement=h}
      \else
        \SetupFloatingEnvironment{literal-block-newfloat}{within=chapter,placement=h}
      \fi
      \usepackage{capt-of}
'''
Run sphinx with builder name 'latexnewfloat'
    python -m sphinx.__init__ -b latexnewfloat {intpudir} {outputdir}
or
- add entry in makefile
- override original latex builder entry using app.set_translator
"""

from sphinx.writers.latex import LaTeXTranslator
from sphinx.builders.latex import LaTeXBuilder

def setup(app):
    app.add_builder(LaTeXNewFloatBuilder)
    app.set_translator('latexnewfloat', LaTeXNewFloatTranslator)
    return {'version': '0.1'}

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
            self.body.append('\\captionof{literal-block-newfloat}{')
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
