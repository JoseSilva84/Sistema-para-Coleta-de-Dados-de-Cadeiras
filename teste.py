def quantidade_cadeiras(vl_qtde, vl):
    qtde = vl_qtde
    valor_unitario = vl
    total = qtde * valor_unitario
    return print(f'O valor é R$ {total:.2f}')

quantidade_cadeiras(100, 4)