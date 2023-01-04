import dash
from dash import html, callback
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
import pandas as pd
from db import consulta, inclusao

dash.register_page(__name__, path='/pesquisa', path_template="/pesquisa=<report_id>")

def layout(report_id=0):
    return html.Div(children=[
        html.H1(children='Pesquisar Pedidos'),
        html.Div(
            [
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Id:"),
                        dbc.Input(placeholder="Insira o Id do Pedido", type="number", id='idPe', value=report_id),
                    ],
                    className="mb-3",
                ),
                html.Div(
                    [],
                    id='tabelaidPe'
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Confirmação da Exclusão")),
                        dbc.ModalBody(
                            html.P('Pedido Excluido.')
                        ),
                    ],
                    id="modalPEDIDO",
                    is_open=False,
                ),
            ],
        ),
    ]),

@callback(
    Output("modalPEDIDO", "is_open"),
    [Input("excluirPe", "n_clicks")],
    [State("modalPEDIDO", "is_open"), State("idPe", "value")],
)
def modalCE(n1, is_open, v1):
    """ Aplicar exclução do produto ao clicar no botão de excluir. """
    if n1:
        inclusao(f"DELETE FROM pedido WHERE idpedido={v1}")
        return not is_open
    return is_open

@callback(Output("tabelaidPe", "children"), [Input("idPe", "value")])
def tabelaidP(value):
    """ Layout aba exclução produto """

    colunas = ['Id Transacao', 'Id Pedido', 'Id Vendedor', 'Id Cliente', 'Id Produto', 'Valor', 'Quantidade', 'Data']
    lista = []
    recset = consulta(f'select * from pedido')
    for rec in recset:
        lista.append(rec)
    dfPeM = pd.DataFrame(lista, columns=colunas)
    dfPeM = dfPeM.sort_values(by=['Id Transacao'])
    dfPeM = dfPeM.reset_index(drop=True)

    if value == None or value == 0 or int(value) < 0 or int(value) > int(dfPeM['Id Pedido'].max()):
        return []
    else:
        colunas = ['Id Transacao', 'Id Pedido', 'Id Vendedor', 'Id Cliente', 'Id Produto', 'Valor', 'Quantidade', 'Data']
        lista = []
        recset = consulta(f'select * from pedido where idpedido={value}')
        for rec in recset:
            lista.append(rec)
        dfPe = pd.DataFrame(lista, columns=colunas)
        dfPe = dfPe.sort_values(by=['Id Transacao'])
        dfPe = dfPe.reset_index(drop=True)
        def botaoExcluirP():
            if lista != []:
                return html.Div(
                            dbc.Button("Excluir", color="danger" , className="me-1", id="excluirPe", n_clicks=0),
                            className="d-grid gap-2 col-6 mx-auto",
                        )
            else:
                return html.P('')

        df = dfPe[dfPe['Id Pedido'] == int(value)]
        colunas = ['Id', 'Nome', 'Idade', 'Data de Admissão', 'Setor', 'Estado']
        lista = []
        recset = consulta(f'select * from pessoa where id_pessoa = {list(df["Id Vendedor"])[0]}')
        for rec in recset:
            lista.append(rec)
        dfCo = pd.DataFrame(lista, columns=colunas)
        dfCo = dfCo.sort_values(by=['Id'])
        dfCo = dfCo.reset_index(drop=True)

        colunas = ['Id', 'Nome', 'CPF', 'Data de Inclusão', 'Status', 'Estado']
        lista = []
        recset = consulta(f'select * from cliente where id = {list(df["Id Cliente"])[0]}')
        for rec in recset:
            lista.append(rec)
        dfCl = pd.DataFrame(lista, columns=colunas)
        dfCl = dfCl.sort_values(by=['Id'])
        dfCl = dfCl.reset_index(drop=True)

        colunas = ['Id Produto', 'Nome', 'Valor', 'Categoria', 'Quantidade', 'Total']
        lista = []
        recset = consulta(f'select idproduto, nome, valor, categoria, quantidade, total from pedido_completo where idpedido = {value}')
        for rec in recset:
            lista.append(rec)
        PeCp = pd.DataFrame(lista, columns=colunas)
        PeCp = PeCp.sort_values(by=['Id Produto'])
        PeCp = PeCp.reset_index(drop=True)
        PeCpTotal = f'R$ {PeCp["Total"].sum():_.2f}'.replace('.', ',').replace('_', '.')

        PeCp['Valor'] = PeCp['Valor'].apply(lambda x: f'R$ {x:_.2f}'.replace('.', ',').replace('_', '.'))
        PeCp['Total'] = PeCp['Total'].apply(lambda x: f'R$ {x:_.2f}'.replace('.', ',').replace('_', '.'))

        return [
            html.H5(f'Pedido {value}', style={"text-align": "center"}),
            html.P(f'Id do Vendedor: {list(df["Id Vendedor"])[0]}', style={"font-weight": "bold"}),
            html.P(f'Nome do Vendedor: {list(dfCo["Nome"])[0]}', style={"font-weight": "bold"}),
            html.P(f'Id do Comprador: {list(df["Id Cliente"])[0]}', style={"font-weight": "bold"}),
            html.P(f'Nome do Comprador: {list(dfCl["Nome"])[0]}', style={"font-weight": "bold"}),
            html.H5(f'Produtos', style={"text-align": "center"}),
            dbc.Table.from_dataframe(PeCp, striped=True, bordered=True, hover=True),
            html.P(f"Total: {PeCpTotal}", style={'text-align':'right', 'font-weight': 'bold'}),
            botaoExcluirP(),
        ]