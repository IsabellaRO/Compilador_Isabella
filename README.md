# Compilador_Isabella


### EBNF:
##### Statements = statement, ("" | ("\n", statements));
##### Statement = "" | (identifier, "=", expressão) | ("PRINT", expressão) | ("while", expressãorel, statements, "wend") | ("if", expressãorel, "then", statements, ("else", statements, "end", "if") | ("end", "if"));
##### expressãorel = expressão, ("="|">"|"<"), expressão
##### expressão = termo, {("+"|"-"|"or"), termo};
##### termo = factor, {("*"|"/"|"and"), factor};
##### factor = número | identifier | ("(", expressão, ")") | (("+"|"-"|"not"), factor) | "input";

### Diagrama Sintático:
![Diagrama_compilador](imgs/diagramalc.JPG "Diagrama 1")
