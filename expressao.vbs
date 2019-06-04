Function Soma(x as Integer, y as Integer) as Integer
    Dim a as Integer
    a = x + y
    Print a
    Soma = a
End Function
Sub Main()
    Dim a as Integer
    Dim b as Integer
    Dim c as Boolean
    a = 0
    while a < 3
        a = a + 1
    wend
    b = Soma(a, 4)
    c = True
    Print a
    Print b
    if c then
        Print not c
    end if
End Sub

