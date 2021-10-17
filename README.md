# llama


![alt text](https://raw.githubusercontent.com/MasonJohnHawver42/llama/main/llama_logo.png)


llama is a programming language centered around playing with math without the hump.

# Basics of making a Language

making a language understandable to a computer requires 3 steps : tokenizing, parsing, evaluating. Tokenizing takes the raw text and identifies the tokens (words) of the language and orders them in a list. Parsing takes that linear order and puts into a tree structure that defines the realtionship of those tokens based of a grahmar. Evaluating takes the tree structure and does what it defines.  


# Progress

The tokenizer is done. The parser is done and it took me forever. Understanding bottom up parsing requires a degree and I'm barley a senior at my highschool, so I went with a simple recursive parser to turn the linear tokens into a tree. The Eveluator is not done. I started it, but never finished it. I moved on, and nows its in the back of my mind. I'll probally come back to it, but there so much else I'm interested in. 

# Grammar

1) Program -> {Statment/r/n}+
2) Statment -> Expression {= | => | >= | <= | =<]} Expression
3) Statment -> id(id {, id}*) = Expression
4) Statment -> Expression
5) Expression -> Term { [+-] Term }*
6) Term -> Factor { [*/] Factor }*
7) Factor -> Power { [^] Power }*
8) Power -> num | id | (Expression)
9) Power -> id(Expression {, Expression}*)
10) Power -> '{' Expression {= | != | => | >= | <= | =<]} Expression '?' { Expression : Expression '}' | Expression '}' | '}' }
