from Lexer import *
from AST import *

# Pr -> {S EOL}+
# S -> id = E | IDENT(id {, id}*) = E
# E -> T { [+-] T }*
# T -> F { [*/] F }*
# P -> P { [^] P }*
# P -> num | [-]IDENT | (E) | IDENT(E {, E}*)

lg = Lexer()
lg.add("EQUALS", "=")
lg.add("OP", "[-+*/^]")
lg.add("NUM", "[-]?[0-9]*[.]?[0-9]+")
lg.add("BRACKET", "[()\[\]]")
lg.add("IDENT", "[a-zA-Z_][a-zA-Z_0-9]*")
lg.add("EOL", ";")
lg.add("COMMA", ",")


# f(x) = (x + 5, (x - 1) * 6 + 1)
# point = f(sin(-10))
# a = pi/4

code = """
a = a * (b / c) * (d / e) * f - 1;
z=1;
"""

tokens = lg.lex(code) + [Token("EOF", "")]
print(" ".join([t.name for t in tokens]) )

nextToken = None

def scanNextToken():
    global tokens, nextToken
    nextToken = tokens[0]
    tokens = tokens[1:]

def parseProgram():
    stmts = []
    while nextToken.name != "EOF":
        a = parseS()
        stmts.append(a)
        if (nextToken.name != "EOL"):
            break
        else:
            scanNextToken()

    return stmts

def parseS():

    if nextToken.name == "IDENT":
        name = nextToken.text
        scanNextToken()
        if nextToken.name == "EQUALS":
            scanNextToken()
            a = Var(name)
            b = parseE()
            return Assighnment(a, b)

        elif nextToken.text == "(":
            scanNextToken()
            args = []
            while nextToken.name == "IDENT":
                args.append(Var(nextToken.text))
                scanNextToken()
                if nextToken.name == "COMMA":
                    continue
                elif nextToken.text == ")":
                    scanNextToken()
                    if nextToken.name == "EQUALS":
                        scanNextToken()
                        expr = parseE()
                        return Func(name, args, expr)

                else:
                    break

def parseE():
    a = parseT()
    exprs = [a]
    while nextToken.name == "OP":
        if nextToken.text == "+":
            scanNextToken()
            a = parseT()

        elif nextToken.text == "-":
            scanNextToken()
            a = Mult([Num(-1.0), parseT()])

        else:
            break

        exprs.append(a)
    if len(exprs) > 1:
        return Add(exprs)
    elif len(exprs) == 1:
        return exprs[0]
    return None

def parseT():
    a = parseF()
    numer = [a]
    denum = []
    while nextToken.name == "OP":
        if nextToken.text == "*":
            scanNextToken()
            a = parseF()
            numer.append(a)

        elif nextToken.text == "/":
            scanNextToken()
            a = parseF()
            denum.append(a)

        else:
            break

    if len(denum) == 0:
        return Mult(numer) if len(numer) > 1 else numer[0]

    return Div(Mult(numer) if len(numer) > 1 else numer[0], Mult(denum) if len(denum) > 1 else denum[0])

def parseF():
    a = parseP()
    while nextToken.text == "^":
        scanNextToken()
        b = parseP()
        a = Power(a, b)

    return a


def parseP():
    if nextToken.name == "NUM":
        a = Num(float(nextToken.text))
        scanNextToken()
        return a
    elif nextToken.text == "(" :
        scanNextToken()
        a = parseE()
        if nextToken.text == ")":
            scanNextToken()
            return a
        elif nextToken.name == "COMMA":
            scanNextToken()
            b = parseE()
            if nextToken.text == ")":
                scanNextToken()
                return Pair(a, b)
    elif nextToken.name == "IDENT":
        name = nextToken.text
        scanNextToken()
        if nextToken.text == "(":
            scanNextToken()
            args = [parseE()]
            while nextToken.name == "COMMA":
                scanNextToken()
                args.append(parseE())

            if nextToken.text == ")":
                scanNextToken()
                return Call(name, args)

        else:
            return Var(name)

#
#     elif nextToken.text == "(" :
#         scanNextToken()
#         a = parseE()
#         if nextToken.text == ")":
#             scanNextToken()
#             return a
#         elif nextToken.name == "COMMA":
#             scanNextToken()
#             b = parseE()
#             if nextToken.text == ")":
#                 scanNextToken()
#                 return Pair(a, b)
#
#     elif nextToken.text == "[":
#         scanNextToken()
#         vals = [parseE()]
#         while nextToken.name == "COMMA":
#             scanNextToken()
#             vals.append(parseE())
#         if nextToken.text == "]":
#             scanNextToken()
#             return Array(vals)

import json
scanNextToken()
prgrm = parseProgram()
for stmt in prgrm:
    print(stmt)
    print(json.dumps(stmt.tree(), sort_keys=False, indent=4))
    print(stmt.simplify())
