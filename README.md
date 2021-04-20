# llama


![alt text](https://raw.githubusercontent.com/MasonJohnHawver42/llama/main/llama_logo.png)


llama is a programming language centered around playing with math without the hump.

# Grammar


Program -> {Statment;}+
Statment -> id = Expression | id(id {, id}*) = E | E
Expression -> Term { [+-] Term }*
Term -> Factor { [*/] Factor }
Factor -> num | id | (Expression)
Factor -> id(Expression {, Expression}*)
Factor -> (Expression, Expression)
Factor -> [Expression {, Expression}*]
