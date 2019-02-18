listaatual = []
parciais = []
atual = ""
entrada  = input("Digite o que deseja calcular: ")
i = 0

if (not entrada[0].isnumeric()) or (not entrada[-1].isnumeric()):
    print("Entrada inválida")
    exit()

while(i < len(entrada)):
    while(entrada[i].isnumeric()):
        listaatual.append(entrada[i])
        if (i < len(entrada)):
            i += 1
        if (i > len(entrada)-1):
            break
    
    if(len(listaatual) > 0):
        for n in listaatual:
            atual = atual + n
        atual = int(atual)
        parciais.append(atual)
        listaatual = []
        atual = ""

    if (i < len(entrada)-1):
        if (entrada[i] == " "):
            i+=1
            pass

        elif (entrada[i] == "+" or entrada[i] == "-"):
            parciais.append(entrada[i])
            i+=1
            pass

        if (i >= len(entrada)):
            break

n = 0
resultado = 0
while(n < len(parciais)):
    if n == 0:
        resultado = parciais[n]
    elif (parciais[n] == "+"):
        n += 1
        resultado += parciais[n]

    elif (parciais[n] == "-"):
        n += 1
        resultado -= parciais[n]

    n +=1

#print(parciais)
print(resultado)