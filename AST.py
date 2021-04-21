class Add:
    def __init__(self, exprs):
        self.exprs = exprs

    def tree(self):
        return {"add" : [expr.tree() for expr in self.exprs]}

    def simplify(self):
        num = Num(0)
        other = []

        for expr in self.exprs:
            simple = expr.simplify()
            if type(simple) is Num:
                num.val += simple.val
            else:
                other.append(simple)

        if len(other) == 0:
            return num
        if num.val == 0:
            return Add(other)
        return Add([num] + other)



    def __str__(self):
        return "({})".format(" + ".join([str(expr) for expr in self.exprs]))

#mabey do the research
# class Negate:
#     def __init__(self, expr):
#         self.expr = expr
#
#     def tree(self):
#         return {"-" : self.expr.tree()}
#
#     def __str__(self):
#         return "-{}".format(str(self.expr))

class Mult:
    def __init__(self, exprs):
        self.exprs = exprs

    def tree(self):
        return {"mult" : [expr.tree() for expr in self.exprs]}

    def simplify(self):
        num = Num(1)
        other = []

        for expr in self.exprs:
            simple = expr.simplify()
            if type(simple) is Num:
                num.val *= simple.val
            else:
                other.append(simple)

        if len(other) == 0:
            return num

        exprs = ([num] if num.val != 1 else []) + other

        for i, expr in enumerate(exprs):

            if type(expr) is Div:
                numerater = expr.num.simplify()
                denum = expr.denum.simplify()

                numertor = Mult(exprs[:i] + [numerater] + exprs[i+1:])
                numertor = numertor.simplify()

                div = Div(numertor, denum)
                return div.simplify()
            

        return Mult(exprs)


    def __str__(self):
        return "({})".format(" * ".join([str(expr) for expr in self.exprs]))

class Div:
    def __init__(self, le, re):
        self.num = le
        self.denum = re

    def tree(self):
        return {"div" : [self.num.tree(), self.denum.tree()]}

    def simplify(self):
        num = self.num.simplify()
        denum = self.denum.simplify()

        if type(num) is Num and type(denum) is Num:
            return Num(num.val / denum.val)

        if type(num) is Div:
            numerator2 = num.num
            denum2 = Mult([num.denum, denum])
            denum2 = denum2.simplify()

            div = Div(numerator2, denum2)
            return div.simplify()
        
        if type(denum) is Div:
            numerator2 = Mult([num, denum.denum])
            numerator2 = numerator2.simplify()
            denum2 = denum.num

            div = Div(numerator2, denum2)
            return div.simplify()
        

        return Div(num, denum)

    def __str__(self):
        return "({} / {})".format(str(self.num), str(self.denum))

class Power:
    def __init__(self, val, power):
        self.base = val
        self.power = power

    def tree(self):
        return {"Power" : [self.base.tree(), self.power.tree()]}

    def simplify(self):
        base = self.base.simplify()
        power = self.power.simplify()

        if type(base) is Num and type(power) is Num:
            return Num(pow(base.val, power.val))

        return Power(base, power)

    def __str__(self):
        return "({} ^ {})".format(str(self.base), str(self.power))

class Num:
    def __init__(self, val):
        self.val = val

    def tree(self):
        return {"num" : self.val}

    def simplify(self):
        return Num(self.val)

    def __str__(self):
        return str(self.val)

class Var:
    def __init__(self, name):
        self.name = name

    def tree(self):
        return {"var" : self.name}

    def simplify(self):
        return Var(self.name)

    def __str__(self):
        return self.name

class Call:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def tree(self):
        return {self.name : [arg.tree() for i, arg in enumerate(self.args)]}

    def __str__(self):
        return "{}({})".format(self.name, ", ".join([str(arg) for arg in self.args]))

# to involved for now
# class Pair:
#     def __init__(self, le, re):
#         self.left = le
#         self.right = re
#
#     def tree(self):
#         return {"pair" : [self.left.tree(), self.right.tree()]}
#
#     def __str__(self):
#         return "({}, {})".format(str(self.left), str(self.right))
#
# class Array:
#     def __init__(self, vals):
#         self.vals = vals
#
#     def tree(self):
#         return {"array" : [val.tree() for val in self.vals]}
#
#     def __str__(self):
#         return "[{}]".format(", ".join([val.__str__() for val in self.vals]))
#

class Assighnment:
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def tree(self):
        return {"assighn" : {"var" : self.var.name, "value" : self.expr.tree()}}

    def simplify(self):
        var = self.var.simplify()
        expr = self.expr.simplify()
        return Assighnment(var, expr)

    def __str__(self):
        return "{} = {}".format(str(self.var), str(self.expr))

class Func:
    def __init__(self, name, args, expr):
        self.name = name
        self.args = args
        self.expr = expr

    def tree(self):
        return {"func" : {"input" : [arg.tree() for arg in self.args], "output" : self.expr.tree()}}

    def __str__(self):
        return "{}({}) = {}".format(self.name, ", ".join([str(arg) for arg in self.args]), str(self.expr))
