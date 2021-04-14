import re

class Token:
    def __init__(self, name, text):
        self.name = name
        self.text = text
    
    def __repr__(self):
        return "<Token : {} = \"{}\">".format(self.name, self.text)

class Lexer:
    def __init__(self):
        self.token_types = []
        
    def add(self, name, rule):
        self.token_types.append((name, rule))
    
    def lex(self, code):
        tokens = []
        
        def span(match):
            if match is None:
                return None
            return match.span()


        matches = [ (tt[0], span(re.search(tt[1], code))) for tt in self.token_types ]
        
        while len([1 for m in matches if m[1] is None]) < len(self.token_types) :
            
            top_match = None
            
            for m in matches:
                if m[1] is not None:
                    top_match = top_match or m
                    if m[1][0] < top_match[1][0]:
                        top_match = m
                    elif m[1][0] == top_match[1][0]:
                        if m[1][1] - m[1][0] > top_match[1][1] - top_match[1][0]:
                            top_match = m
            
            tokens.append(Token(top_match[0], code[top_match[1][0] : top_match[1][1]]))
            code = code[:top_match[1][0]] + code[top_match[1][1]:]
            
            print(top_match)
            print("F", matches)
            print(code)

            length = top_match[1][1] - top_match[1][0]
            matches = [(m[0], (m[1][0] - length, m[1][1] - length) if m[1] is not None else None) for m in matches if (m[1] is None) or not (top_match[1][0] <= m[1][0] < top_match[1][1])]
            print("S", matches)
            for tt in self.token_types:
                if sum([m[0] == tt[0] for m in matches]) == 0:
                    matches.append( (tt[0], span( re.match(tt[1], code) ) ) )
                    
            print("T", matches)
            break
        
        return tokens

lg = Lexer()
lg.add("EQUALS", "hi")
lg.add("OP", "[+-/*]")
lg.add("NUM", "[0-9]*[.]?[0-9]+")

code = "x = -101sin(y) + 10 / 50"
print(lg.lex(code))



        
