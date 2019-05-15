# Compilador_Isabella


### EBNF:
##### Program = "Sub", "Main", "(", ")", "\n", {statement, "\n"}, "End", "Sub";
##### Statement = "" | (identifier, "=", relexpression) | ("PRINT", relexpression) | ("Dim", identifier, "as", Type) |  ("While", relexpression, "\n" {statement, "\n"}, "Wend") | ("If", relexpression, "Then", "\n", {statement, "\n"}, {"Else", "\n", {statement, "\n"}}, "End", "If");
##### Relexpression = expression, {("="|">"|"<"), expression};
##### Expression = term, {("+"|"-"|"or"), term};
##### Term = factor, {("*"|"/"|"and"), factor};
##### Factor = number | ("True"|"False) | identifier | ("(", relexpression, ")") | (("+"|"-"|"not"), factor) | "Input";
##### Type = "Integer"|"Boolean";

### Diagrama Sintático:
![Diagrama_compilador](imgs/diagramalc.JPG "Diagrama 1")
