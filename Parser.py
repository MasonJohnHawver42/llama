from Lexer import *

# P -> {S EOL}+
# S -> id = E | IDENT(id {, id}*) = E | E
# E -> T { [+-] T }*
# T -> F { [*/] F }
# F -> num | IDENT | (E) | ?[num]IDENT(E {, E}*) | (E, E) | [E {, E}*]

lg = Lexer()
lg.add("EQUALS", "=")
lg.add("OP", "[+*/-]")
lg.add("NUM", "[-]?[0-9]*[.]?[0-9]+")
lg.add("BRACKET", "[()\[\]]")
lg.add("IDENT", "[a-zA-Z_][a-zA-Z_0-9]*")
lg.add("EOL", "\n")
lg.add("COMMA", ",")


# f(x) = (x + 5, (x - 1) * 6 + 1)
# point = f(sin(-10))
# a = pi/4

code = """
f(x) = (x + 5, (x - 1) * 6 + 1)
point = f(sin(-10))
a = pi/4
point * [[cos(a), -sin(a)],
        [sin(a),  cos(a)]]
"""

tokens = lg.lex(code) + [Token("EOL", ""), Token("EOF", "")]
print(" ".join([t.name for t in tokens]) )

for i, t in enumerate(tokens):
    if t.name == "EOL":
        if tokens[i+1].name not in ["IDENT", "EOF"]:
            tokens.remove(t)

print(" ".join([t.name for t in tokens]) )

class Add:
    def __init__(self, le, re):
        self.right = re
        self.left = le

    def eval(self):
        return self.left.eval() + self.right.eval()

    def tree(self):
        return {"add" : [self.left.tree(), self.right.tree()]}

    def __str__(self):
        return "({} + {})".format(str(self.left), str(self.right))

class Sub:
    def __init__(self, le, re):
        self.right = re
        self.left = le

    def eval(self):
        return self.left.eval() - self.right.eval()

    def tree(self):
        return {"sub" : [self.left.tree(), self.right.tree()]}

    def __str__(self):
        return "({} - {})".format(str(self.left), str(self.right))

class Div:
    def __init__(self, le, re):
        self.right = re
        self.left = le

    def eval(self):
        return self.left.eval() / self.right.eval()

    def tree(self):
        return {"div" : [self.left.tree(), self.right.tree()]}

    def __str__(self):
        return "({} / {})".format(str(self.left), str(self.right))

class Mult:
    def __init__(self, le, re):
        self.right = re
        self.left = le

    def eval(self):
        return self.left.eval() * self.right.eval()

    def tree(self):
        return {"mult" : [self.left.tree(), self.right.tree()] }

    def __str__(self):
        return "({} * {})".format(str(self.left), str(self.right))

class Num:
    def __init__(self, val):
        self.val = val

    def eval(self):
        return self.val

    def tree(self):
        return {"num" : self.val}

    def __str__(self):
        return str(self.val)

class Var:
    def __init__(self, name):
        self.name = name

    def tree(self):
        return {"var" : self.name}

    def __str__(self):
        return self.name

class Assighnment:
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def tree(self):
        return {"assighn" : {"var" : self.var.name, "value" : self.expr.tree()}}

    def __str__(self):
        return "{} = {}".format(str(self.var), str(self.expr))

class Call:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def tree(self):
        return {self.name : [arg.tree() for i, arg in enumerate(self.args)]}

    def __str__(self):
        return "{}({})".format(self.name, ", ".join([str(arg) for arg in self.args]))

class Pair:
    def __init__(self, le, re):
        self.left = le
        self.right = re

    def tree(self):
        return {"pair" : [self.left.tree(), self.right.tree()]}

    def __str__(self):
        return "({}, {})".format(str(self.left), str(self.right))

class Array:
    def __init__(self, vals):
        self.vals = vals

    def tree(self):
        return {"array" : [val.tree() for val in self.vals]}

    def __str__(self):
        return "[{}]".format(", ".join([val.__str__() for val in self.vals]))

class Func:
    def __init__(self, name, args, expr):
        self.name = name
        self.args = args
        self.expr = expr

    def tree(self):
        return {"func" : {"input" : [arg.tree() for arg in self.args], "output" : self.expr.tree()}}

    def __str__(self):
        return "{}({}) = {}".format(self.name, ", ".join([str(arg) for arg in self.args]), str(self.expr))



nextToken = None

def scanNextToken():
    global tokens, nextToken
    nextToken = tokens[0]
    tokens = tokens[1:]


def parseP():
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
    global nextToken, tokens
    temp = (nextToken, tokens)

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

    nextToken = temp[0]
    tokens = temp[1]
    return parseE()

def parseE():
    a = parseT()

    while True:
        if nextToken.name == "OP":
            if nextToken.text == "+":
                scanNextToken()
                b = parseT()
                a = Add(a, b)

            elif nextToken.text == "-":
                scanNextToken()
                b = parseT()
                a = Sub(a, b)

            else:
                break
        else:
            break

    return a

def parseT():
    a = parseF()

    while True:
        if nextToken.name == "OP":
            if nextToken.text == "*":
                scanNextToken()
                b = parseF()
                a = Mult(a, b)

            elif nextToken.text == "/":
                scanNextToken()
                b = parseF()
                a = Div(a, b)

            else:
                break
        else:
            break
    return a

def parseF():
    if nextToken.name == "NUM":
        a = Num(float(nextToken.text))
        scanNextToken()
        if nextToken.name == "IDENT":
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
                    return Mult(a, Call(name, args))
        else:
            return a

    elif nextToken.text == "-":
        scanNextToken()
        if nextToken.name == "IDENT":
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
                    return Mult(Num(-1), Call(name, args))

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

    elif nextToken.text == "[":
        scanNextToken()
        vals = [parseE()]
        while nextToken.name == "COMMA":
            scanNextToken()
            vals.append(parseE())
        if nextToken.text == "]":
            scanNextToken()
            return Array(vals)

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

import json

scanNextToken()
stmts = parseP()
for s in stmts:
    print(s)
    print(json.dumps(s.tree(), sort_keys=False, indent=4))
