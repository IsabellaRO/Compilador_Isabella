class Token:
    def __init__(self, tipo, valor):
        self.type = tipo # string
        self.value = valor # integer

class Tokenizer:
    def __init__(self, origin, actual):
        self.origin = origin # string, código fonte que sera tokenizado
        self.position = 0 # integer, posição atual que o Tokenizador está separando
        if actual == None:
            self.actual = Token("int", 0) # token, lê o próximo token e atualiza o atributo actual
        else:
            self.actual = Token(actual.type, actual.value)

    def selectNext(self):
        while (self.position < len(self.origin)) and self.origin[self.position] == " ": # se for espaço só pula
            self.position = self.position + 1

        if self.position == len(self.origin):
            self.actual = Token("eof", "-1")

        elif self.origin[self.position].isdigit():
            word = ""
            while (self.position < len(self.origin)) and (self.origin[self.position].isdigit()): # se for digito vai concatenando
                word = word + self.origin[self.position]
                self.position = self.position + 1

            self.actual = Token("int", int(word))

        elif self.origin[self.position] == '*': # se for mult
            self.actual =  Token("mult", "*")
            self.position = self.position + 1

        elif self.origin[self.position] == '/': # se for div
            self.actual =  Token("div", "/")
            self.position = self.position + 1

        elif self.origin[self.position] == '+': # se for soma
            self.actual =  Token("plus", "+")
            self.position = self.position + 1

        elif self.origin[self.position] == '-': # se for sub
            self.actual = Token("minus", "-")
            self.position = self.position + 1

        else:
            raise ValueError("Caractere inválido.")

        return self.actual

class Parser:
    
    def parseTerm():
        if Parser.tokens.actual.type == "int":
            res = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            while Parser.tokens.actual.type == "mult" or Parser.tokens.actual.type == "div":
                if Parser.tokens.actual.type == "mult":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "int":
                        res = res * Parser.tokens.actual.value
                    else:
                        raise ValueError('Esperava-se um int e foi encontrado um', Parser.tokens.actual.type, 'durante a soma.')

                elif Parser.tokens.actual.type == "div":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "int":
                        res = res // Parser.tokens.actual.value
                    else:
                        raise ValueError('Esperava-se um int e foi encontrado um', Parser.tokens.actual.type, 'durante a subtração.')
                
                Parser.tokens.selectNext()
        else:
            raise ValueError('Esperava-se um int e foi encontrado um', Parser.tokens.actual.type, 'no início da expressão.')
        
        return res

    def parseExpression():
        res = Parser.parseTerm()
        while Parser.tokens.actual.type == "plus" or Parser.tokens.actual.type == "minus":
            if Parser.tokens.actual.type == "plus":
                Parser.tokens.selectNext()
                res = res + Parser.parseTerm()
            elif Parser.tokens.actual.type == "minus":
                Parser.tokens.selectNext()
                res = res - Parser.parseTerm()    
        return res

    def run(origin):
        Parser.tokens = Tokenizer(origin, None)
        Parser.tokens.selectNext()
        res = Parser.parseExpression()
        if Parser.tokens.actual.type != 'eof':
            raise ValueError('Entrada inválida')
        
        return res
    

def main():
    try:
        entrada  = input("Digite o que deseja calcular: ")
        res = Parser.run(entrada)
        print("Resultado:", res)
    except Exception as ex:
        print(ex)

if  __name__ =='__main__':main()