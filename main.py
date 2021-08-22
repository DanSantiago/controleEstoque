import PySimpleGUI as sg
import bancodados


def tela_ini():
    sg.theme('LightGray1')

    inilayout = [
        [sg.Text('BEM-VINDO A CENTRAL DE CONTROLE GOSTOSURINHAS!')],
        [sg.Button('PEDIDOS'), sg.Button('ESTOQUE'), sg.Button('ORÇAMENTO'), sg.Button('SAIR')]
    ]

    janela = sg.Window('Organizador de Estoque/Controle de renda', inilayout, size=(400, 100),
                       element_justification='center')
    event, values = janela.read()

    if event == 'PEDIDOS':
        janela.close()
        return True, 'pedidos'

    if event == 'ESTOQUE':
        janela.close()
        return True, 'estoque'

    if event == 'ORÇAMENTO':
        janela.close()
        return True, 'orçamento'

    if event == 'SAIR':
        janela.close()
        return False, 'falha'
    if event == sg.WIN_CLOSED:
        janela.close()
        return False, 'falha'


def main():
    sg.theme('LightGray1')
    while True:
        cont, tipo = tela_ini()
        if not cont:
            break
        if tipo == 'pedidos':
            NUMERO_VENDA = ''
            VALOR = ''
            ENDERECO = ''
            SITUACAO = ''
            DATA_ENTR = ''
            PEDIDO = ''
            NOME = bancodados.read_pedidos()

            layout = [
                [sg.Text('NOME', size=(20, 1)), sg.Input(key='nome', size=(30, 1))],
                [sg.Text('NÚMERO DO PEDIDO', size=(20, 1)), sg.Input(key='vendnum', size=(30, 1))],
                [sg.Text('ENDEREÇO', size=(20, 1)), sg.Input(key='end', size=(30, 1))],
                [sg.Text('PEDIDO', size=(20, 1)), sg.Input(key='ped', size=(30, 1))],
                [sg.Text('VALOR', size=(20, 1)), sg.Input(key='val', size=(30, 1))],
                [sg.Text('DATA DE ENTREGA', size=(20, 1)), sg.Input(key='date', size=(30, 1))],
                [sg.Text('SITUAÇÃO', size=(20, 1)), sg.Input(key='sit', size=(30, 1))],
                [sg.Button('ADICIONAR')],
                [sg.Text('')],
                [sg.Text('LISTAGEM DE CLIENTES')],
                [sg.Text('Nº CLIENTE')],
                [sg.Listbox(NOME, size=(50, 10), key='BOX')],
                [sg.Button('DELETAR'), sg.Button('SITUAÇÃO'), sg.Button('ENDEREÇO')],
                [sg.Button('VALOR'), sg.Button('PEDIDO'), sg.Button('DATA ENTREGA')],
                [sg.Button('SAIR')]
            ]
            janela = sg.Window('Cadastro de clientes', layout)

            while True:
                event, values = janela.read()

                if event == 'SAIR':
                    janela.close()
                    break

                if event == sg.WIN_CLOSED:
                    janela.close()
                    break

                if event == 'ADICIONAR':
                    NOME = values['nome'].capitalize()
                    ENDERECO = values['end']
                    VALOR = values['val']
                    SITUACAO = values['sit']
                    NUMERO_VENDA = values['vendnum']
                    DATA_ENTR = values['date']
                    PEDIDO = values['ped']

                    if NOME != '':
                        bancodados.write_pedidos(NOME, NUMERO_VENDA, ENDERECO, VALOR, SITUACAO, DATA_ENTR, PEDIDO)

                    NOME = bancodados.read_pedidos()
                    janela.find_element('nome').Update('')
                    janela.find_element('end').Update('')
                    janela.find_element('val').Update('')
                    janela.find_element('sit').Update('')
                    janela.find_element('vendnum').Update('')
                    janela.find_element('date').Update('')
                    janela.find_element('ped').Update('')
                    janela.find_element('BOX').Update(NOME)

                if event == 'DELETAR':
                    if NOME:
                        x = values['BOX'][0]
                        bancodados.delete_pedidos(x)
                        NOME = bancodados.read_pedidos()
                        janela.find_element('BOX').Update(NOME)

                if event == 'SITUAÇÃO':
                    if NOME:
                        x = values['BOX'][0]
                        sit = bancodados.show_sit(x)
                        sg.popup(f'Situação: {sit[0]}')

                if event == 'ENDEREÇO':
                    if NOME:
                        x = values['BOX'][0]
                        end = bancodados.show_end(x)
                        sg.popup(f'Endereço: {end[0]}')

                if event == 'VALOR':
                    if NOME:
                        x = values['BOX'][0]
                        val_t = bancodados.show_value(x)
                        val = float(val_t[0].replace(',', '.'))
                        sg.popup(f'Valor: {val} R$')

                if event == 'PEDIDO':
                    if NOME:
                        x = values['BOX'][0]
                        sit = bancodados.show_ped(x)
                        sg.popup(f'Pedido: {sit[0]}')

                if event == 'DATA ENTREGA':
                    if NOME:
                        x = values['BOX'][0]
                        sit = bancodados.show_date(x)
                        sg.popup(f'Data de entrega: {sit[0]}')

        if tipo == 'orçamento':
            VALOR_VENDIDO = ''
            VALOR_PREVISTO = ''
            LUCRO = ''
            REPOSICAO_PRODUTOS = ''

            layout = [
                [sg.Text('TOTAL DE VENDAS', size=(15, 1)), sg.Input(key='tvendas', size=(30, 1))],
                [sg.Text('TOTAL ESPERADO', size=(15, 1)), sg.Input(key='estvendas', size=(30, 1))],
                [sg.Text('MINÍMO ESTOQUE', size=(15, 1)), sg.Input(key='minimo', size=(30, 1))],
                [sg.Button('MOSTRAR INFORMAÇÕES')],
                [sg.Text('')],
                [sg.Text('INFORMAÇÕES')],
                [sg.Output(size=(80, 20))],
                [sg.Button('SAIR')]
            ]
            janela = sg.Window('Controle de Orçamento', layout)

            while True:
                event, values = janela.read()

                if event == 'SAIR':
                    janela.close()
                    break

                if event == sg.WIN_CLOSED:
                    janela.close()
                    break

                if event == 'MOSTRAR INFORMAÇÕES':
                    VALOR_VENDIDO = values['tvendas']
                    VALOR_PREVISTO = values['estvendas']
                    REPOSICAO_PRODUTOS = values['minimo']

                    meta = (float(VALOR_VENDIDO.replace(',', '.'))/float(VALOR_PREVISTO.replace(',', '.')))*100
                    minimo = int(REPOSICAO_PRODUTOS)
                    gastos = 0.0

                    produtos = bancodados.show_all_quant()
                    print(f"A sua meta de venda era {float(VALOR_PREVISTO.replace(',', '.'))} R$, você vendeu {float(VALOR_VENDIDO.replace(',', '.'))} R$. Isso corresponde a {meta:.2f}% da sua meta.")
                    print(f"Como você escolheu fazer a reposição dos items com menos de {REPOSICAO_PRODUTOS} unidades, é necessário: ")

                    for t in range(0, len(produtos)):
                        if int(produtos[t][1]) < minimo:
                            reposicao = minimo - int(produtos[t][1])
                            dimdim = float(produtos[t][2].replace(',', '.')) * reposicao
                            print(f"Repor {reposicao} unidades de {produtos[t][0]}, que dará um total de {dimdim} R$.")
                            gastos += dimdim

                    print(f"Para repor todos os itens, de acordo com os valores cadastrados, seu gasto será de {gastos} R$.")
                    LUCRO = float(VALOR_VENDIDO.replace(',', '.')) - gastos
                    print(f"Finalizando com um lucro de {LUCRO} R$. Bom trabalho!")
                    bancodados.write_orcamento(VALOR_VENDIDO, VALOR_PREVISTO, LUCRO)

                    janela.find_element('tvendas').Update('')
                    janela.find_element('estvendas').Update('')
                    janela.find_element('minimo').Update('')

        if tipo == 'estoque':
            CODIGO = ''
            PRECO = ''
            QUANT = ''
            PROD = bancodados.read_estoque()

            layout = [
                [sg.Text('PRODUTO', size=(20, 1)), sg.Input(key='prod', size=(30, 1))],
                [sg.Text('CÓDIGO DO PRODUTO', size=(20, 1)), sg.Input(key='cod', size=(30, 1))],
                [sg.Text('PREÇO DO PRODUTO', size=(20, 1)), sg.Input(key='preco', size=(30, 1))],
                [sg.Text('QUANT. DO PRODUTO', size=(20, 1)), sg.Input(key='quant', size=(30, 1))],
                [sg.Button('ADICIONAR')],
                [sg.Text('')],
                [sg.Text('LOG')],
                [sg.Output(size=(50, 10))],
                [sg.Text('')],
                [sg.Text('LISTAGEM DE PRODUTOS')],
                [sg.Text('COD PRODUTO')],
                [sg.Listbox(PROD, size=(50, 10), key='BOX')],
                [sg.Button('DELETAR'), sg.Button('-1 UN.'), sg.Button('-5 UN.'), sg.Button('-10 UN.'), sg.Button('QUANTIDADE')],
                [sg.Button('PREÇO'), sg.Button('+1 UN.'), sg.Button('+5 UN.'), sg.Button('+10 UN.'), sg.Button('SAIR')]
            ]
            janela = sg.Window('Cadastro de produtos', layout)

            while True:
                event, values = janela.read()

                if event == 'ADICIONAR':
                    CODIGO = values['cod']
                    PRECO = values['preco']
                    QUANT = values['quant']
                    PROD = values['prod'].capitalize()
                    if PROD != '':
                        bancodados.write_estoque(CODIGO, PROD, PRECO, QUANT)

                    PROD = bancodados.read_estoque()
                    janela.find_element('prod').Update('')
                    janela.find_element('cod').Update('')
                    janela.find_element('preco').Update('')
                    janela.find_element('quant').Update('')
                    janela.find_element('BOX').Update(PROD)

                if event == 'SAIR':
                    janela.close()
                    break

                if event == sg.WIN_CLOSED:
                    janela.close()
                    break

                if event == 'DELETAR':
                    if PROD:
                        x = values['BOX'][0]
                        bancodados.delete_estoque(x)
                        PROD = bancodados.read_estoque()
                        janela.find_element('BOX').Update(PROD)

                if event == 'PREÇO':
                    if PROD:
                        x = values['BOX'][0]
                        val_str = ''.join(bancodados.show_price(x))
                        val = float(val_str.replace(',', '.'))
                        sg.popup(f'O valor do item é {val} R$')

                if event == 'QUANTIDADE':
                    if PROD:
                        x = values['BOX'][0]
                        val_t = bancodados.show_quant(x)
                        val = val_t[0]
                        sg.popup(f'Restam {val} desse item no estoque')

                if event == '-1 UN.':
                    if PROD:
                        x = values['BOX'][0]
                        val_t = bancodados.show_quant(x)
                        if val_t[0] >= 1:
                            val = val_t[0] - 1
                        bancodados.quant_retirar(val, x)
                        PROD = bancodados.read_estoque()
                        janela.find_element('BOX').Update(PROD)

                if event == '-5 UN.':
                    if PROD:
                        x = values['BOX'][0]
                        val_t = bancodados.show_quant(x)
                        if val_t[0] >= 5:
                            val = val_t[0] - 5
                        bancodados.quant_retirar(val, x)
                        PROD = bancodados.read_estoque()
                        janela.find_element('BOX').Update(PROD)

                if event == '-10 UN.':
                    if PROD:
                        x = values['BOX'][0]
                        val_t = bancodados.show_quant(x)
                        if val_t[0] >= 10:
                            val = val_t[0] - 10
                        bancodados.quant_retirar(val, x)
                        PROD = bancodados.read_estoque()
                        janela.find_element('BOX').Update(PROD)

                if event == '+1 UN.':
                    if PROD:
                        x = values['BOX'][0]
                        val_t = bancodados.show_quant(x)
                        val = val_t[0] + 1
                        bancodados.quant_adicionar(val, x)
                        PROD = bancodados.read_estoque()
                        janela.find_element('BOX').Update(PROD)

                if event == '+5 UN.':
                    if PROD:
                        x = values['BOX'][0]
                        val_t = bancodados.show_quant(x)
                        val = val_t[0] + 5
                        bancodados.quant_adicionar(val, x)
                        PROD = bancodados.read_estoque()
                        janela.find_element('BOX').Update(PROD)

                if event == '+10 UN.':
                    if PROD:
                        x = values['BOX'][0]
                        val_t = bancodados.show_quant(x)
                        val = val_t[0] + 10
                        bancodados.quant_adicionar(val, x)
                        PROD = bancodados.read_estoque()
                        janela.find_element('BOX').Update(PROD)

if __name__ == '__main__':
    main()
