from AST import *
from Parser import *


lg = Lexer()
lg.add("EQUALS", "=")
lg.add("OP", "[-+*/^]")
lg.add("NUM", "[-]?[0-9]*[.]?[0-9]+")
lg.add("BRACKET", "[()\[\]]")
lg.add("IDENT", "[a-zA-Z_][a-zA-Z_0-9]*")
lg.add("EOL", ";")
lg.add("COMMA", ",")

pr = Parser()

# f(x) = (x + 5, (x - 1) * 6 + 1)
# point = f(sin(-10))
# a = pi/4

code = """
a = a * (b / c) * (d / e) * f - 1;
z = 1 / 6 + 3 * pi / 5 * 7 / 4/ 4;
"""

tokens = lg.lex(code) + [Token("EOF", "")]
asts = pr.parse(tokens)

class Evaluator:
    def __init__(self):
        self.vars = {}
        
    def evaluate(self, stmt):
        if type(stmt) is Assighnment:
            pass
  
  
import json

print(" ".join([t.name for t in tokens]) )

ev = Evaluator()

for ast in asts:
    print(ast)
    ast = ast.simplify()
    print(ast)
    print(json.dumps(ast.tree(), sort_keys=False, indent=4))