Function Soma(x as Integer, y as Integer) as Integer
    Dim a as Integer
    a = x + y
    Print a
    While a < 8
        a = Soma(a, 1)
    wend
    Soma = a
End Function
Sub Main()
    Dim a as Integer
    Dim b as Integer
    Print true
    a = 3
    print True
    b = Soma(a, 4)
    Print a 
    Print b
End Sub