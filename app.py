import dash
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import datetime
import io
import webbrowser
from dash import Input, Output, State, html, dcc
from db import consulta, inclusao
from FuncoesPD import menu, menuSuspenso

"""
Funções Banco de Dados
"""

"""
Variaveis
"""

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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.PULSE], use_pages=True, update_title='Carregando...', suppress_callback_exceptions=True)

"""
Menu
"""
botoes1 = [
    dbc.DropdownMenuItem("Inserir Dados", id="botaoC1", n_clicks=0),
    dbc.DropdownMenuItem("Excluir Dados", id="botaoC2", n_clicks=0),
    dbc.DropdownMenuItem("Download Dados", id="botaoC3", n_clicks=0),
    dcc.Download(id="DadosdeColaboradores"),
    dbc.DropdownMenuItem("Upload Dados", id="botaoC4", n_clicks=0),
]
botoes2 = [
    dbc.DropdownMenuItem("Inserir Dados", id="botaoP1", n_clicks=0),
    dbc.DropdownMenuItem("Excluir Dados", id="botaoP2", n_clicks=0),
    dbc.DropdownMenuItem("Download Dados", id="botaoP3", n_clicks=0),
    dcc.Download(id="DadosdeProdutos"),
    dbc.DropdownMenuItem("Upload Dados", id="botaoP4", n_clicks=0),
]
botoes3 = [
    dbc.DropdownMenuItem("Inserir Dados", id="botaoCL1", n_clicks=0),
    dbc.DropdownMenuItem("Excluir Dados", id="botaoCL2", n_clicks=0),
    dbc.DropdownMenuItem("Download Dados", id="botaoCL3", n_clicks=0),
    dcc.Download(id="DadosdeClientes"),
    dbc.DropdownMenuItem("Upload Dados", id="botaoCL4", n_clicks=0),
]
botoes4 = [
    dbc.DropdownMenuItem("Pesquisar Pedidos", id="botaoPe2", href="/pesquisa"),
    dbc.DropdownMenuItem("Download Dados", id="botaoPe3", n_clicks=0),
    dcc.Download(id="DadosdePedidos"),
]
botaoMenu = dbc.Button("Inserir Pedido", href="/pedido")
menuSuspenso1 = menuSuspenso('Colaboradores', botoes1)
menuSuspenso2 = menuSuspenso('Produtos', botoes2)
menuSuspenso3 = menuSuspenso('Clientes', botoes3)
menuSuspenso4 = menuSuspenso('Pedidos', botoes4)
menuSistema = menu("🤖 Mini Sistema", [botaoMenu, menuSuspenso1, menuSuspenso2, menuSuspenso3, menuSuspenso4])

"""
Fim Menu
"""

app.layout = html.Div(
    # Barra inicial
    [   
        menuSistema,
        html.Div([
            dash.page_container,
        ],
        style={'margin-top': '1%', 'margin-right': '5%', 'margin-left': '5%', 'margin-bottom': '1%'},
        ),
        dbc.Offcanvas(
            # Aba Inseir Dados Colaborador
            html.Div(
                [
                    dbc.InputGroup(
                        [dbc.InputGroupText("Nome:"), dbc.Input(placeholder="Insira o nome completo", id='nome')],
                        className="mb-3",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Idade:"),
                            dbc.Input(placeholder="Insira a idade", type="number", id='idade'),
                        ],
                        className="mb-3",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Data da Admissão:"),
                            dbc.Input(placeholder="Insira a idade", type="date", id='data'),
                        ],
                        className="mb-3",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Setor:"),
                            dbc.Select(
                                options=[
                                    {"label": "Administrativo", "value": "Administrativo"},
                                    {"label": "Vendas", "value": "Vendas"},
                                    {"label": "Compras", "value": "Compras"},
                                    {"label": "Gestão de Pessoas", "value": "Gestão de Pessoas"},
                                ], id='setor'
                            ),
                        ],
                        className="mb-3",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Estado:"),
                            dbc.Select(
                                options=[
                                    {"label": "RS", "value": "RS"},
                                    {"label": "SC", "value": "SC"},
                                    {"label": "SP", "value": "SP"},
                                    {"label": "RJ", "value": "RJ"},
                                ], id = 'estado'
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        dbc.Button("Enviar", color="primary", className="me-1", id="enviar", n_clicks=0),
                        className="d-grid gap-2 col-6 mx-auto",
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Dados Inseridos")),
                            dbc.ModalBody(
                                [],
                                id="modalBodyCI",
                            ),
                        ],
                        id="modalCI",
                        is_open=False,
                    ),
                ]
            ),
            id="inserirColaborador",
            scrollable=True,
            title="Inserir Colaborador",
            is_open=False,
        ),
        dbc.Offcanvas(
            # Aba Excluir Dados Colaborador
            html.Div(
                [
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Id:"),
                            dbc.Input(placeholder="Insira o Id do Colaborador", type="number", id='id', value=0),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [],
                        id='tabelaid'
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Confirmação da Exclusão")),
                            dbc.ModalBody(
                                html.P('Colaborador Excluido.')
                            ),
                        ],
                        id="modalCE",
                        is_open=False,
                    ),
                ],
            ),
            id="excluirColaborador",
            scrollable=True,
            title="Excluir Colaborador",
            is_open=False,
        ),
        dbc.Offcanvas(
            # Aba Upload Dados Colaborador
            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Arraste e Solte ou ',
                        html.A('Selecione o Arquivo')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    multiple=True
                ),
                html.Div(id='output-data-upload'),
            ]),
            id="uploadColaborador",
            title="Upload Colaborador",
            is_open=False,
        ),
        dbc.Offcanvas(
            # Aba Inseir Dados Produto
            html.Div(
                [
                    dbc.InputGroup(
                        [dbc.InputGroupText("Nome:"), dbc.Input(placeholder="Insira o nome do poroduto", id='nomeP')],
                        className="mb-3",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Valor: R$ "),
                            dbc.Input(placeholder="Insira valor do produto", type="number", id='valorP'),
                        ],
                        className="mb-3",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Categoria:"),
                            dbc.Select(
                                options=[
                                    {"label": "Cozinha", "value": "Cozinha"},
                                    {"label": "Escolar", "value": "Escolar"},
                                    {"label": "Escritorio", "value": "Escritorio"},
                                    {"label": "Vestuario", "value": "Vestuario"},
                                ], id='categoriaP'
                            ),
                        ],
                        className="mb-3",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Estoque:"),
                            dbc.Input(placeholder="Insira a quantidade em estoque", type="number", id='estoqueP'),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        dbc.Button("Enviar", color="primary", className="me-1", id="enviarP", n_clicks=0),
                        className="d-grid gap-2 col-6 mx-auto",
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Dados Inseridos")),
                            dbc.ModalBody(
                                [],
                                id="modalBodyPI",
                            ),
                        ],
                        id="modalPI",
                        is_open=False,
                    ),
                ]
            ),
            id="inserirProduto",
            scrollable=True,
            title="Inserir Produto",
            is_open=False,
        ),
         dbc.Offcanvas(
            # Aba Excluir Dados Produto
            html.Div(
                [
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Id:"),
                            dbc.Input(placeholder="Insira o Id do Produto", type="number", id='idP', value=0),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [],
                        id='tabelaidP'
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Confirmação da Exclusão")),
                            dbc.ModalBody(
                                html.P('Produto Excluido.')
                            ),
                        ],
                        id="modalPE",
                        is_open=False,
                    ),
                ],
            ),
            id="excluirProduto",
            scrollable=True,
            title="Excluir Produto",
            is_open=False,
        ),
        dbc.Offcanvas(
            # Aba Upload Dados Produto
            html.Div([
                dcc.Upload(
                    id='upload-dataP',
                    children=html.Div([
                        'Arraste e Solte ou ',
                        html.A('Selecione o Arquivo')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    multiple=True
                ),
                html.Div(id='output-data-uploadP'),
            ]),
            id="uploadProduto",
            title="Upload Produto",
            is_open=False,
        ),
        dbc.Offcanvas(
            # Aba Inseir Dados Cliente
            html.Div(
                [
                    dbc.InputGroup(
                        [dbc.InputGroupText("Nome:"), dbc.Input(placeholder="Insira o nome completo", id='nomeCliente')],
                        className="mb-3",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("CPF:"),
                            dbc.Input(placeholder="Insira o CPF", type="number", id='CPF'),
                        ],
                        className="mb-3",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Status:"),
                            dbc.Select(
                                options=[
                                    {"label": "Ativo", "value": "Ativo"},
                                    {"label": "Inativo", "value": "Inativo"},
                                ], id='status'
                            ),
                        ],
                        className="mb-3",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Estado:"),
                            dbc.Select(
                                options=[
                                    {"label": "RS", "value": "RS"},
                                    {"label": "SC", "value": "SC"},
                                    {"label": "SP", "value": "SP"},
                                    {"label": "RJ", "value": "RJ"},
                                ], id = 'estadoCliente'
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        dbc.Button("Enviar", color="primary", className="me-1", id="enviarCliente", n_clicks=0),
                        className="d-grid gap-2 col-6 mx-auto",
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Dados Inseridos")),
                            dbc.ModalBody(
                                [],
                                id='modalBodyCL',
                            ),
                        ],
                        id="modalCL",
                        is_open=False,
                    ),
                ]
            ),
            id="inserirCliente",
            scrollable=True,
            title="Inserir Cliente",
            is_open=False,
        ),
        dbc.Offcanvas(
            # Aba Excluir Dados Cliente
            html.Div(
                [
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Id:"),
                            dbc.Input(placeholder="Insira o Id do Cliente", type="number", id='idCliente', value=0),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [],
                        id='tabelaidCliente'
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Confirmação da Exclusão")),
                            dbc.ModalBody(
                                html.P('Cliente Excluido.')
                            ),
                        ],
                        id="modalCLE",
                        is_open=False,
                    ),
                ],
            ),
            id="excluirCliente",
            scrollable=True,
            title="Excluir Cliente",
            is_open=False,
        ),
        dbc.Offcanvas(
            # Aba Upload Dados Clientes
            html.Div([
                dcc.Upload(
                    id='upload-dataCL',
                    children=html.Div([
                        'Arraste e Solte ou ',
                        html.A('Selecione o Arquivo')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    multiple=True
                ),
                html.Div(id='output-data-uploadCL'),
            ]),
            id="uploadCliente",
            title="Upload Cliente",
            is_open=False,
        ),
    ],
)

def Upload_arquivo_CL(contents, filename, date):
    """ Função upload arquivo de clientes """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Suponha que o usuário tenha feito upload de um arquivo CSV
            dfUp = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Suponha que o usuário tenha carregado um arquivo Excel
            dfUp = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'Ocorreu um erro ao processar este arquivo.'
        ])

    for coluna, linha in dfUp.iterrows():
        try:
            inclusao(f"UPDATE cliente SET id={linha.Id}, nome='{linha.Nome}', cpf='{linha.CPF}', data_inclusao='{linha[3]}', status='{linha.Status}', estado='{linha.Estado}' WHERE id={linha.Id}")
        except:
            lista = [0]
            recset = consulta('select id from cliente')
            for rec in recset:
                lista.append(rec[0])
            idCL = max(lista) + 1
            inclusao(f"insert into cliente values ({idCL}, '{linha.Nome}', '{linha.CPF}', '{linha[3]}', '{linha.Status}', '{linha.Estado}')")

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.P('Upload realizado com sucesso.')
    ])

@app.callback(Output('output-data-uploadCL', 'children'),
              Input('upload-dataCL', 'contents'),
              State('upload-dataCL', 'filename'),
              State('upload-dataCL', 'last_modified'))
def update_outputCL(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            Upload_arquivo_CL(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(
    Output("uploadCliente", "is_open"),
    Input("botaoCL4", "n_clicks"),
    [State("uploadColaborador", "is_open")],
)
def uploadColaborador(n1, is_open):
    """ Abrir aba upload arquivo de Cliente. """
    if n1:
        return not is_open
    return is_open

@app.callback(
    Output("DadosdeClientes", "data"),
    Input("botaoCL3", "n_clicks"),
    prevent_initial_call=True,
)
def DadosdeClientes(n_clicks):
    """ Abrir aba download arquivo de cliente. """
    colunas = ['Id', 'Nome', 'CPF', 'Data de Inclusão', 'Status', 'Estado']
    lista = []
    recset = consulta('select * from cliente')
    for rec in recset:
        lista.append(rec)
    dfDCL = pd.DataFrame(lista, columns=colunas)
    dfDCL = dfDCL.sort_values(by=['Id'])
    return dcc.send_data_frame(
         dfDCL.to_excel, 
        "DadosdeClientes.xlsx", 
        sheet_name="Clientes", 
        index=False,
        )

@app.callback(
    Output("modalCLE", "is_open"),
    [Input("excluirClienteB", "n_clicks")],
    [State("modalCLE", "is_open"), State("idCliente", "value")],
)
def modalCLE(n1, is_open, v1):
    """ Aplicar exclução do cliente ao clicar no botão de excluir. """
    if n1:
        inclusao(f"DELETE FROM cliente WHERE id={v1}")
        return not is_open
    return is_open

@app.callback(Output("tabelaidCliente", "children"), [Input("idCliente", "value")])
def tabelaidCliente(value):
    """ Layout aba exclução cliente """
    if value == None:
        return []
    else:
        id_cliente = value
        colunas = ['Id', 'Nome', 'CPF', 'Status', 'Estado']
        lista = []
        recset = consulta(f"select id, nome, cpf, status, estado from cliente where id={id_cliente}")
        for rec in recset:
            lista.append(rec)
        dfidC = pd.DataFrame(lista, columns=colunas)
        dfidC = dfidC.sort_values(by=['Id'])
        dfidC = dfidC.reset_index(drop=True)
        def botaoExcluir():
            if lista != []:
                return html.Div(
                            dbc.Button("Excluir", color="danger", className="me-1", id="excluirClienteB", n_clicks=0),
                            className="d-grid gap-2 col-6 mx-auto",
                        )
            else:
                return html.P('')

        return [
            dbc.Table.from_dataframe(dfidC, striped=True, bordered=True, hover=True),
            botaoExcluir(),
        ]

@app.callback(
    Output("excluirCliente", "is_open"),
    Input("botaoCL2", "n_clicks"),
    State("excluirCliente", "is_open"),
)
def excluirColaborador(n1, is_open):
    """ Abrir aba exclução de cliente. """
    if n1:
        return not is_open
    return is_open


@app.callback(
    [
        Output("modalCL", "is_open"),
        Output("modalBodyCL", "children"),
        Output("nomeCliente", "value"),
        Output("CPF", "value"),
        Output("status", "value"),
        Output("estadoCliente", "value"),
    ],
    [
        Input("enviarCliente", "n_clicks")
    ],
    [
        State("modalCL", "is_open"), 
        State("nomeCliente", "value"), 
        State("CPF", "value"),
        State("status", "value"),
        State("estadoCliente", "value"),
    ],
)
def modalPr(n1, is_open, v1, v2, v4, v5):
    """ Funsão para inserir produto. """
    if n1:
        if v1 == None or v1 == "" or v2 == None or v4 == None or v5 == None:
            return not is_open, [
                html.P('Informações de Nome/CPF/Status ou Estado faltando..', style={"font-weight": "bold", "color":"red"})
            ], v1, v2, v4, v5
        else:
            lista = [0]
            recset = consulta('select id from cliente')
            for rec in recset:
                lista.append(rec[0])
            id = max(lista) + 1
            inclusao(f"insert into cliente values ({id}, '{v1}', {v2}, '{datetime.datetime.today().strftime('%d/%m/%Y %H:%M')}', '{v4}', '{v5}')")
            return not is_open, [
                html.P('Dados Inseridos com sucesso.'),
            ], None, None, None, None
    return is_open, [], v1, v2, v4, v5

@app.callback(
    Output("inserirCliente", "is_open"),
    Input("botaoCL1", "n_clicks"),
    State("inserirCliente", "is_open"),
)
def inserirCliente(n1, is_open):
    """ Abrir aba para inserir cliente. """
    if n1:
        return not is_open
    return is_open


"""
Inicio funções relacionadas aos pedidos.

"""

@app.callback(
    Output("excluirPedido", "is_open"),
    Input("botaoPe2", "n_clicks"),
    State("excluirPedido", "is_open"),
)
def excluirProduto(n1, is_open):
    """ Abrir aba exclução de pedido. """
    if n1:
        return not is_open
    return is_open


@app.callback(
    Output("DadosdePedidos", "data"),
    Input("botaoPe3", "n_clicks"),
    prevent_initial_call=True,
)
def DadosdePedidos(n_clicks):
    """ Abrir aba download arquivo de pedido. """
    colunas = ['idtransacao', 'idpedido', 'idvendedor', 'idcliente', 'idproduto', 'valor', 'quantidade', 'iddata']
    lista = []
    recset = consulta('select * from pedido')
    for rec in recset:
        lista.append(rec)
    dfDP = pd.DataFrame(lista, columns=colunas)
    dfDP = dfDP.sort_values(by=['idtransacao'])
    return dcc.send_data_frame(
         dfDP.to_excel, 
        "DadosdePedidos.xlsx", 
        sheet_name="Pedidos", 
        index=False,
        )


"""
Fim funções relacionadas aos pedidos.

"""

"""
Inicio funções relacionadas aos produtos.

"""

def Upload_arquivo_P(contents, filename, date):
    """ Função upload arquivo de produtos """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Suponha que o usuário tenha feito upload de um arquivo CSV
            dfUpP = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Suponha que o usuário tenha carregado um arquivo Excel
            dfUpP = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'Ocorreu um erro ao processar este arquivo.'
        ])

    for coluna, linha in dfUpP.iterrows():
        try:
            inclusao(f"UPDATE produto SET id={linha.Id}, nome='{linha.Nome}', valor={linha.Valor}, categoria='{linha.Categoria}', estoque='{linha.Estoque}' WHERE id={linha.Id}")
        except:
            lista = [0]
            recset = consulta('select id from produto')
            for rec in recset:
                lista.append(rec[0])
            id = max(lista) + 1
            inclusao(f"insert into produto values ({id}, '{linha.Nome}', {linha.Valor}, '{linha.Categoria}', '{linha.Estoque}')")

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.P('Upload realizado com sucesso.')
    ])

@app.callback(Output('output-data-uploadP', 'children'),
              Input('upload-dataP', 'contents'),
              State('upload-dataP', 'filename'),
              State('upload-dataP', 'last_modified'))
def update_outputP(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            Upload_arquivo_P(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(
    Output("uploadProduto", "is_open"),
    Input("botaoP4", "n_clicks"),
    [State("uploadProduto", "is_open")],
)
def uploadProduto(n1, is_open):
    """ Abrir aba upload arquivo de produto. """
    if n1:
        return not is_open
    return is_open

@app.callback(
    Output("DadosdeProdutos", "data"),
    Input("botaoP3", "n_clicks"),
    prevent_initial_call=True,
)
def DadosdeProdutos(n_clicks):
    """ Abrir aba download arquivo de produto. """
    colunas = ['Id', 'Nome', 'Valor', 'Categoria', 'Estoque']
    lista = []
    recset = consulta('select * from produto')
    for rec in recset:
        lista.append(rec)
    dfDP = pd.DataFrame(lista, columns=colunas)
    dfDP = dfDP.sort_values(by=['Id'])
    return dcc.send_data_frame(
         dfDP.to_excel, 
        "DadosdeProdutos.xlsx", 
        sheet_name="Produtos", 
        index=False,
        )

@app.callback(
    Output("modalPE", "is_open"),
    [Input("excluirP", "n_clicks")],
    [State("modalPE", "is_open"), State("idP", "value")],
)
def modalPE(n1, is_open, v1):
    """ Aplicar exclução do produto ao clicar no botão de excluir. """
    if n1:
        inclusao(f"DELETE FROM produto	WHERE id={v1}")
        return not is_open
    return is_open

@app.callback(Output("tabelaidP", "children"), [Input("idP", "value")])
def tabelaidP(value):
    """ Layout aba exclução produto """
    if value == None:
        return []
    else:
        colunas = ['Id', 'Nome', 'Valor', 'Categoria', 'Estoque']
        lista = []
        recset = consulta(f'select * from produto where id={value}')
        for rec in recset:
            lista.append(rec)
        dfidP = pd.DataFrame(lista, columns=colunas)
        dfidP = dfidP.sort_values(by=['Id'])
        dfidP = dfidP.reset_index(drop=True)
        def botaoExcluirP():
            if lista != []:
                return html.Div(
                            dbc.Button("Excluir", color="danger", className="me-1", id="excluirP", n_clicks=0),
                            className="d-grid gap-2 col-6 mx-auto",
                        )
            else:
                return html.P('')

        return [
            dbc.Table.from_dataframe(dfidP, striped=True, bordered=True, hover=True),
            botaoExcluirP(),
        ]

@app.callback(
    Output("excluirProduto", "is_open"),
    Input("botaoP2", "n_clicks"),
    State("excluirProduto", "is_open"),
)
def excluirProduto(n1, is_open):
    """ Abrir aba exclução de produto. """
    if n1:
        return not is_open
    return is_open


@app.callback(
    [
        Output("modalPI", "is_open"),
        Output("modalBodyPI", "children"),
        Output("nomeP", "value"),
        Output("valorP", "value"),
        Output("categoriaP", "value"),
        Output("estoqueP", "value")
    ],
    [
        Input("enviarP", "n_clicks")
    ],
    [
        State("modalPI", "is_open"), 
        State("nomeP", "value"), 
        State("valorP", "value"),
        State("categoriaP", "value"),
        State("estoqueP", "value"),
    ],
)
def modalPI(n1, is_open, v1, v2, v3, v4):
    """ Funsão para inserir produto. """
    if n1:
        if v1 == None or v1 == "" or v2 == None or v3 == None or v4 == None:
            return not is_open, [
                html.P('Informações de nome/Valor/Categoria ou Estoque faltando..', style={"font-weight": "bold", "color":"red"})
            ], v1, v2, v3, v4
        else:
            lista = [0]
            recset = consulta('select id from produto')
            for rec in recset:
                lista.append(rec[0])
            idP = max(lista) + 1
            inclusao(f"insert into produto values ({idP}, '{v1}', {v2}, '{v3}', '{v4}')")
            return not is_open, [
                html.P('Dados Inseridos com sucesso.'),
            ], None, None, None, None
    return is_open, [], v1, v2, v3, v4

@app.callback(
    Output("inserirProduto", "is_open"),
    Input("botaoP1", "n_clicks"),
    State("inserirProduto", "is_open"),
)
def inserirProduto(n1, is_open):
    """ Abrir aba para inserir produto. """
    if n1:
        return not is_open
    return is_open

"""
Fim funções relacionadas aos produtos.

"""

"""
Inicio funções relacionadas aos Colaborador.

"""

def Upload_arquivo_C(contents, filename, date):
    """ Função upload arquivo de colaborador """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Suponha que o usuário tenha feito upload de um arquivo CSV
            dfUp = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Suponha que o usuário tenha carregado um arquivo Excel
            dfUp = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'Ocorreu um erro ao processar este arquivo.'
        ])

    for coluna, linha in dfUp.iterrows():
        try:
            inclusao(f"UPDATE pessoa SET id_pessoa={linha.Id}, nome='{linha.Nome}', idade={linha.Idade}, data_admissao='{linha[3]}', setor='{linha.Setor}', estado='{linha.Estado}' WHERE id_pessoa={linha.Id}")
        except:
            lista = [0]
            recset = consulta('select id_pessoa from pessoa')
            for rec in recset:
                lista.append(rec[0])
            id = max(lista) + 1
            inclusao(f"insert into pessoa values ({id}, '{linha.Nome}', {linha.Idade}, '{linha[3]}', '{linha.Setor}', '{linha.Estado}')")

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.P('Upload realizado com sucesso.')
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            Upload_arquivo_C(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(
    Output("uploadColaborador", "is_open"),
    Input("botaoC4", "n_clicks"),
    [State("uploadColaborador", "is_open")],
)
def uploadColaborador(n1, is_open):
    """ Abrir aba upload arquivo de colaborador. """
    if n1:
        return not is_open
    return is_open

@app.callback(
    Output("DadosdeColaboradores", "data"),
    Input("botaoC3", "n_clicks"),
    prevent_initial_call=True,
)
def DadosdeColaboradores(n_clicks):
    """ Abrir aba download arquivo de colaborador. """
    colunas = ['Id', 'Nome', 'Idade', 'Data de Admissão', 'Setor', 'Estado']
    lista = []
    recset = consulta('select * from pessoa')
    for rec in recset:
        lista.append(rec)
    dfDC = pd.DataFrame(lista, columns=colunas)
    dfDC = dfDC.sort_values(by=['Id'])
    return dcc.send_data_frame(
         dfDC.to_excel, 
        "DadosdeColaboradores.xlsx", 
        sheet_name="Colaboradores", 
        index=False,
        )

@app.callback(
    Output("modalCE", "is_open"),
    [Input("excluir", "n_clicks")],
    [State("modalCE", "is_open"), State("id", "value")],
)
def modalCE(n1, is_open, v1):
    """ Aplicar exclução do colaborador ao clicar no botão de excluir. """
    if n1:
        inclusao(f"DELETE FROM pessoa	WHERE id_pessoa={v1}")
        return not is_open
    return is_open


@app.callback(Output("tabelaid", "children"), [Input("id", "value")])
def tabelaid(value):
    """ Layout aba exclução colaborador """
    if value == None:
        return []
    else:
        id_pessoa = value
        colunas = ['Id', 'Nome', 'Idade', 'Setor', 'Estado']
        lista = []
        recset = consulta(f"select id_pessoa, nome, idade, setor, estado from pessoa where id_pessoa={id_pessoa}")
        for rec in recset:
            lista.append(rec)
        dfid = pd.DataFrame(lista, columns=colunas)
        dfid = dfid.sort_values(by=['Id'])
        dfid = dfid.reset_index(drop=True)
        def botaoExcluir():
            if lista != []:
                return html.Div(
                            dbc.Button("Excluir", color="danger", className="me-1", id="excluir", n_clicks=0),
                            className="d-grid gap-2 col-6 mx-auto",
                        )
            else:
                return html.P('')

        return [
            dbc.Table.from_dataframe(dfid, striped=True, bordered=True, hover=True),
            botaoExcluir(),
        ]

@app.callback(
    Output("excluirColaborador", "is_open"),
    Input("botaoC2", "n_clicks"),
    State("excluirColaborador", "is_open"),
)
def excluirColaborador(n1, is_open):
    """ Abrir aba exclução de colaborador. """
    if n1:
        return not is_open
    return is_open

@app.callback(
    [Output("modalCI", "is_open"),
    Output("modalBodyCI", "children"),
    Output("nome", "value"),
    Output("idade", "value"),
    Output("data", "value"),
    Output("setor", "value"),
    Output("estado", "value")],
    [Input("enviar", "n_clicks")],
    [
        State("modalCI", "is_open"), 
        State("nome", "value"), 
        State("idade", "value"),
        State("data", "value"),
        State("setor", "value"),
        State("estado", "value"),
    ],
)
def modalCI(n1, is_open, v1, v2, v3, v4, v5):
    """ Funsão para inserir colaborador. """
    if n1:
        if v1 == None or v1 == "" or v2 == None or v3 == None or v4 == None or v5 == None:
            return not is_open, [
                html.P('Informações de Nome/Idade/Data da Admissão/Setor ou Estado faltando..', style={"font-weight": "bold", "color":"red"})
            ], v1, v2, v3, v4, v5
        else:
            lista = [0]
            recset = consulta('select id_pessoa from pessoa')
            for rec in recset:
                lista.append(rec[0])
            id = max(lista) + 1
            inclusao(f"insert into pessoa values ({id}, '{v1}', {v2}, '{v3}', '{v4}', '{v5}')")
            return not is_open, [
                html.P('Dados Inseridos com sucesso.'),
            ], None, None, None, None, None
    return is_open, [], v1, v2, v3, v4, v5

@app.callback(
    Output("inserirColaborador", "is_open"),
    Input("botaoC1", "n_clicks"),
    State("inserirColaborador", "is_open"),
)
def inserirColaborador(n1, is_open):
    """ Abrir aba para inserir colaborador. """
    if n1:
        return not is_open
    return is_open

"""
Fim funções relacionadas aos colaborador.

"""

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8050/")
    app.run_server()
