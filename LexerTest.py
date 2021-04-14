from Lexer import *

lg = Lexer()
lg.add("EQUALS", "=")
lg.add("OP", "[+-/*]")
lg.add("NUM", "[+-]?[0-9]*[.]?[0-9]+")
lg.add("LB", "[(]")
lg.add("RB", "[)]")
lg.add("IDENT", "[a-zA-Z_]+")

code = "x = -101sin(y) + 10 / 50"
print(lg.lex(code))