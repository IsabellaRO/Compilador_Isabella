sub main()

dim media as integer
dim p1 as integer
dim p2 as integer
dim projeto as integer
dim nota as integer
dim reprovado as boolean

p1 = 5
p2 = 3
projeto = 5
media = 4
reprovado = true

if projeto > media then
    nota = (projeto+p1+p2)/3
    print nota
    if nota > media then
        reprovado = false
        print reprovado
    else 
        print reprovado
    end if
else
    print reprovado
end if

while reprovado
    if projeto < 10 then
        projeto = projeto + 1
        nota = (projeto+p1+p2)/3
        if nota > media then
            reprovado = false
            print reprovado
        else
            print reprovado
        end if
    else
        p1 = p1 + 1
        nota = (projeto+p1+p2)/3
        if nota > media then
            reprovado = false
            print reprovado
        else
            print reprovado
        end if
    end if
wend

end sub
