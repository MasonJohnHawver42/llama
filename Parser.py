from Lexer import *
from AST import *

# Pr -> {S EOL}+
# S -> id = E | IDENT(id {, id}*) = E
# E -> T { [+-] T }*
# T -> F { [*/] F }*
# P -> P { [^] P }*
# P -> num | [-]IDENT | (E) | IDENT(E {, E}*)


class Parser:
    def __init__(self):
        self.tokens = []
        self.nextToken = None
    
    def parse(self, tokens):
        self.tokens = tokens
        self.scanNextToken()
        return self.parseProgram()

    def scanNextToken(self):
        self.nextToken = self.tokens[0]
        self.tokens = self.tokens[1:]

    def parseProgram(self):    
        stmts = []
        while self.nextToken.name != "EOF":
            a = self.parseS()
            stmts.append(a)
            if (self.nextToken.name != "EOL"):
                break
            else:
                self.scanNextToken()

        return stmts

    def parseS(self):

        if self.nextToken.name == "IDENT":
            name = self.nextToken.text
            self.scanNextToken()
            if self.nextToken.name == "EQUALS":
                self.scanNextToken()
                a = Var(name)
                b = self.parseE()
                return Assighnment(a, b)

            elif self.nextToken.text == "(":
                self.scanNextToken()
                args = []
                while self.nextToken.name == "IDENT":
                    args.append(Var(self.nextToken.text))
                    self.scanNextToken()
                    if self.nextToken.name == "COMMA":
                        continue
                    elif self.nextToken.text == ")":
                        self.scanNextToken()
                        if self.nextToken.name == "EQUALS":
                            self.scanNextToken()
                            expr = self.parseE()
                            return Func(name, args, expr)

                    else:
                        break

    def parseE(self):
        a = self.parseT()
        exprs = [a]
        while self.nextToken.name == "OP":
            if self.nextToken.text == "+":
                self.scanNextToken()
                a = self.parseT()

            elif self.nextToken.text == "-":
                self.scanNextToken()
                a = Mult([Num(-1.0), self.parseT()])

            else:
                break

            exprs.append(a)
        if len(exprs) > 1:
            return Add(exprs)
        elif len(exprs) == 1:
            return exprs[0]
        return None

    def parseT(self):
        a = self.parseF()
        numer = [a]
        denum = []
        while self.nextToken.name == "OP":
            if self.nextToken.text == "*":
                self.scanNextToken()
                a = self.parseF()
                numer.append(a)

            elif self.nextToken.text == "/":
                self.scanNextToken()
                a = self.parseF()
                denum.append(a)

            else:
                break

        if len(denum) == 0:
            return Mult(numer) if len(numer) > 1 else numer[0]

        return Div(Mult(numer) if len(numer) > 1 else numer[0], Mult(denum) if len(denum) > 1 else denum[0])

    def parseF(self):
        a = self.parseP()
        while self.nextToken.text == "^":
            self.scanNextToken()
            b = self.parseP()
            a = Power(a, b)

        return a

    def parseP(self):
        if self.nextToken.name == "NUM":
            a = Num(float(self.nextToken.text))
            self.scanNextToken()
            return a
        elif self.nextToken.text == "(" :
            self.scanNextToken()
            a = self.parseE()
            if self.nextToken.text == ")":
                self.scanNextToken()
                return a
        elif self.nextToken.name == "IDENT":
            name = self.nextToken.text
            self.scanNextToken()
            if self.nextToken.text == "(":
                self.scanNextToken()
                args = [self.parseE()]
                while self.nextToken.name == "COMMA":
                    self.scanNextToken()
                    args.append(self.parseE())

                if self.nextToken.text == ")":
                    self.scanNextToken()
                    return Call(name, args)

            else:
                return Var(name)