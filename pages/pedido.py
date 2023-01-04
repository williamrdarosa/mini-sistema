import dash
from dash import html, callback
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
import pandas as pd
from datetime import datetime
from db import consulta, inclusao

dados = {
    'Id':[],
    'Nome':[],
    'Valor':[],
    'Categoria':[],
    'Quantidade':[],
    'Total':[],
}

dfpedido = pd.DataFrame(dados)

dfProduto = pd.DataFrame()

dfid = pd.DataFrame(dados)

dfidCL = pd.DataFrame(dados)

dash.register_page(__name__, path='/pedido')

layout = html.Div([
    dbc.Button('Novo Pedido', id='novoPedido'),
    html.Div(
        [],
        id='corpoPPedido'
    ),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Confirmar Pedido")),
            dbc.ModalBody([], id='descricao'),
            dbc.ModalFooter(
                dbc.Button(
                    "Confirmar", id="botaoCP", color="success", n_clicks=0
                ),
            ),
        ],
        id="modalCP",
        is_open=False,
    ),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Alerta")),
            dbc.ModalBody([
                html.P('Pedido Realizado ✔️')
            ]),
            dbc.ModalFooter(),
        ],
        id="modalAlerta",
        is_open=False,
    ),
])

@callback(
    Output("corpoPPedido", "children"),
    Input("novoPedido", "n_clicks"),
)
def funccorpoPPedido(n1):
    global dfpedido
    """ Abrir aba para inserir cliente. """
    if n1:
        dfpedido = pd.DataFrame(dados)
        return [
            html.Div([
                html.H4('Inserir Vendedor:', style={'margin-top': '1%'}),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Id Vendedor:"),
                        dbc.Input(placeholder="Insira o Id do Vendedor", type="number", id='idVendedor', value=0),
                    ],
                    className="mb-3",
                ),
                html.Div(
                    [],
                    id='idVendedorT'
                ),
            ],
            style= {'width': '45%', 'display': 'inline-block', 'margin-right': '20px', 'margin-left': '10px'}),
            html.Div([
                html.H4('Inserir Cliente:', style={'margin-top': '1%'}),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Id Cliente:"),
                        dbc.Input(placeholder="Insira o Id do Cliente", type="number", id='idCliente', value=0),
                    ],
                    className="mb-3",
                ),
                html.Div(
                    [],
                    id='idClienteT'
                ),
            ],
            style= {'width': '45%', 'display': 'inline-block', 'margin-left': '20px', 'margin-right': '10px'}),
            html.Div(
                [],
                id='verificarInativado'
            ),
            html.Hr(),
            html.H4('Inserir Produto:'),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Id Produto:"), 
                    dbc.Input(placeholder="Insira o nome do produto", type="number", id='idProduto'),
                    dbc.InputGroupText("Quantidade:"),
                    dbc.Input(placeholder="Insira a quantidade em estoque", type="number", id='pedidoQuantidade'),
                    dbc.Button('Inserir', id='botaoInserir'),
                ],
                className="mb-3",
            ),
            html.Div(
                [],
                id='idProdutoT',
            ),
            html.Hr(),
            html.H4('Sacola:'),
            html.Div(
                [],
                id='idSacola',
            ),
        ]

@callback(
    [Output("idClienteT", "children"),
    Output("verificarInativado", "children"),],
    [Input("idCliente", "value")]
)
def idCliente(value):
    """ Pesquisar cliente """
    global dfidCL
    if value == None:
        return []
    else:
        idCL = value
        colunas = ['Id', 'Nome', 'CPF', 'Status', 'Estado']
        lista = []
        recset = consulta(f"select id, nome, cpf, status, estado from cliente where id={idCL}")
        for rec in recset:
            lista.append(rec)
        dfidCL = pd.DataFrame(lista, columns=colunas)
        dfidCL = dfidCL.sort_values(by=['Id'])
        dfidCL = dfidCL.reset_index(drop=True)

        if value <= dfidCL['Id'].max():
            if dfidCL['Status'][0] == 'Inativo':
                return [
                    dbc.Table.from_dataframe(dfidCL, striped=True, bordered=True, hover=True),
                ], [
                    dbc.Badge(f"Cliente: {dfidCL['Nome'][0]} está Inativado.", color="danger", className="me-1"),
                ]

        return [
            dbc.Table.from_dataframe(dfidCL, striped=True, bordered=True, hover=True),
        ], []

@callback(
    Output("idSacola", "children"),
    Input("botaoInserir", "n_clicks"),
    State("idProduto", "value"),
    State("pedidoQuantidade", "value"),
    )
def tabelaSacola(n_clicks, v1, v2):
    """ Inserir sacola """
    global dfpedido
    global dfProduto
    if n_clicks:
        if v1 == None or v2 == None:
            return []
        else:
            colunas = ['Id', 'Nome', 'Valor', 'Categoria']
            lista = []
            recset = consulta(f"select id, nome, valor, categoria from produto where id={v1}")
            for rec in recset:
                lista.append(rec)
            dfidP = pd.DataFrame(lista, columns=colunas)
            dfidP = dfidP.sort_values(by=['Id'])
            dfidP = dfidP.reset_index(drop=True)
            dfidP['Quantidade'] = v2
            dfidP['Total'] = dfidP['Quantidade'] * dfidP['Valor']

            if v2 > int(dfProduto[dfProduto['Id'] == v1]['Estoque']):
                dfpedido
            else:
                dfpedido = pd.concat([dfpedido, dfidP])

            dfpedidoD = dfpedido.copy()
            dfpedidoTotal = f'R$ {dfpedido["Total"].sum():_.2f}'.replace('.', ',').replace('_', '.')
            dfpedidoD['Valor'] = dfpedidoD['Valor'].apply(lambda x: f'R$ {x:_.2f}'.replace('.', ',').replace('_', '.'))
            dfpedidoD['Total'] = dfpedidoD['Total'].apply(lambda x: f'R$ {x:_.2f}'.replace('.', ',').replace('_', '.'))

            return [
                dbc.Table.from_dataframe(dfpedidoD, striped=True, bordered=True, hover=True),
                html.P(f"Total: {dfpedidoTotal}", style={'text-align':'right', 'font-weight': 'bold'}),
                dbc.Button('Concluir Pedido', id='concluirPedido', color="success"),
            ]

@callback(Output("idProdutoT", "children"), [Input("idProduto", "value")])
def tabelaidP(value):
    """ Pesquisar Produto """
    global dfProduto
    global dfpedido
    if value == None:
        return []
    else:
        colunas = ['Id', 'Nome', 'Valor', 'Categoria', 'Estoque']
        lista = []
        recset = consulta(f'select * from produto where id={value}')
        for rec in recset:
            lista.append(rec)
        dfProduto = pd.DataFrame(lista, columns=colunas)
        dfProduto = dfProduto.sort_values(by=['Id'])
        dfProduto = dfProduto.reset_index(drop=True)
        dfProduto['Valor'] = dfProduto['Valor'].apply(lambda x: f'R$ {x:_.2f}'.replace('.', ',').replace('_', '.'))

        try:
            if int(dfProduto['Id']) in list(dfpedido['Id']):
                dfProduto.loc[0,'Estoque'] = int(dfProduto['Estoque']) - int(dfpedido[dfpedido['Id'] == int(dfProduto['Id'])]['Quantidade'])
        except:
            pass

        return [
            dbc.Table.from_dataframe(dfProduto, striped=True, bordered=True, hover=True),
        ]

@callback(Output("idVendedorT", "children"), [Input("idVendedor", "value")])
def idVendedor(value):
    """ Pesquisar vendedor """
    global dfid
    global dfpedido
    if value == None:
        return []
    else:
        id_pessoa = value
        colunas = ['Id', 'Nome', 'Idade', 'Setor', 'Estado']
        lista = []
        recset = consulta(f"select id_pessoa, nome, idade, setor, estado from pessoa where id_pessoa={id_pessoa} AND setor = 'Vendas' ")
        for rec in recset:
            lista.append(rec)
        dfid = pd.DataFrame(lista, columns=colunas)
        dfid = dfid.sort_values(by=['Id'])
        dfid = dfid.reset_index(drop=True)
        return [
            dbc.Table.from_dataframe(dfid, striped=True, bordered=True, hover=True),
        ]

@callback(
    Output("modalCP", "is_open"),
    Output("descricao", "children"),
    [Input("concluirPedido", "n_clicks")],
    [State("modalCP", "is_open"),
    State("idVendedor", "value"),
    State("idCliente", "value")],
)
def funcaoCP(n1, is_open, v3, v4):
    global dfid
    global dfidCL

    if n1:
        if v3 == None or v3 == 0 or v4 == None or v4 == 0:
            return not is_open, [
                html.P('Informações do vendedor e/ou cliente faltando.', style={"font-weight": "bold", "color":"red"})
            ]
        else:
            lista = [0]
            recset = consulta('select idpedido from pedido')
            for rec in recset:
                lista.append(rec[0])
            id = max(lista) + 1

            dfpedidoD = dfpedido.copy()
            dfpedidoTotal = f'R$ {dfpedido["Total"].sum():_.2f}'.replace('.', ',').replace('_', '.')
            dfpedidoD['Valor'] = dfpedidoD['Valor'].apply(lambda x: f'R$ {x:_.2f}'.replace('.', ',').replace('_', '.'))
            dfpedidoD['Total'] = dfpedidoD['Total'].apply(lambda x: f'R$ {x:_.2f}'.replace('.', ',').replace('_', '.'))

            return not is_open, [
                html.H5(f'Pedido {id}', style={"text-align": "center"}),
                html.P(f'Id do Vendedor: {int(dfid.Id)}', style={"font-weight": "bold"}),
                html.P(f'Nome do Vendedor: {str(dfid.Nome.values[0])}', style={"font-weight": "bold"}),
                html.P(f'Id do Comprador: {int(dfidCL.Id)}', style={"font-weight": "bold"}),
                html.P(f'Nome do Comprador: {str(dfidCL.Nome.values[0])}', style={"font-weight": "bold"}),
                html.H5(f'Produtos', style={"text-align": "center"}),
                dbc.Table.from_dataframe(dfpedidoD, striped=True, bordered=True, hover=True),
                html.P(f"Total: R$ {dfpedidoTotal}", style={'text-align':'right', 'font-weight': 'bold'}),
                ]
    return is_open, []

@callback(
    Output("modalAlerta", "is_open"),
    [Input("botaoCP", "n_clicks")],
    [State("modalAlerta", "is_open"),
    State("idVendedor", "value"),
    State("idCliente", "value")],
)
def funcaoAlerta(n1, is_open, v3, v4):
    global dfpedido
    global dfid
    global dfidCL
    lista = [0]
    recset = consulta('select idpedido from pedido')
    for rec in recset:
        lista.append(rec[0])
    id = max(lista) + 1
    if n1:
        if v3 == None or v3 == 0 or v4 == None or v4 == 0:
            return is_open
        else:
            for coluna, linha in dfpedido.iterrows():
                colunas = ['Id', 'Estoque']
                lista = []
                recset = consulta('select id, estoque from produto')
                for rec in recset:
                    lista.append(rec)
                dfproduto = pd.DataFrame(lista, columns=colunas)
                sql = f"UPDATE produto SET estoque={dfproduto[dfproduto['Id']==linha.Id]['Estoque'].values[0] - int(linha.Quantidade)} WHERE id={linha.Id}"
                inclusao(sql)
                recset = consulta('select idtransacao from pedido')
                lista = []
                for rec in recset:
                    lista.append(rec[0])
                if lista == []:
                    idtransacao = 1
                else:
                    idtransacao = max(lista) + 1
                sql = f"insert into pedido values ({idtransacao}, {id}, {int(dfid.Id)}, {int(dfidCL.Id)}, {linha.Id}, {linha.Valor}, {linha.Quantidade}, '{datetime.today().strftime('%d/%m/%Y %H:%M')}')"
                inclusao(sql)
            return not is_open
    return is_open