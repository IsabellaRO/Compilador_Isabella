# Compilador_Isabella


### EBNF:
##### expressão = termo, {("+"|"-"), termo};
##### termo = factor, {("*"|"/"), factor};
##### factor = número | {("(", expressão, ")")} | (("+"|"-"), factor);

### Diagrama Sintático:
![Diagrama_compilador](imgs/diagramalc.png "Diagrama 1")
