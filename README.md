# llama


![alt text](https://raw.githubusercontent.com/MasonJohnHawver42/llama/main/llama_logo.png)


llama is a programming language centered around playing with math without the hump.

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
