import dash
from dash import html
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dash_table, callback, dcc
from db import consulta
import plotly.express as px
from datetime import datetime

dash.register_page(__name__, path='/',name='Página Inicial')

def tabelas():
    """ Tabelas da página inicial. """
    colunas = ['Id', 'Nome', 'Idade', 'Data de Admissão', 'Setor', 'Estado']
    lista = []
    recset = consulta('select * from pessoa')
    for rec in recset:
        lista.append(rec)
    dfTC = pd.DataFrame(lista, columns=colunas)
    dfTC = dfTC.sort_values(by=['Id'])
    dfTC = dfTC.reset_index(drop=True)
    dfTC['Data de Admissão'] = pd.to_datetime(dfTC['Data de Admissão']).dt.strftime('%d/%m/%Y')

    dfTCg = dfTC.groupby(['Estado','Setor']).count()
    dfTCg = dfTCg.rename(columns={'Nome':'Colaboradores'})
    dfTCg = dfTCg['Colaboradores']
    dfTCg = dfTCg.reset_index()

    figdfTC = px.bar(dfTCg, x="Estado", y="Colaboradores", color="Setor", barmode="group", text_auto=True)
    figdfTC.update_traces(textposition="outside")

    colunas = ['Id', 'Nome', 'Valor', 'Categoria', 'Estoque']
    lista = []
    recset = consulta('select * from produto')
    for rec in recset:
        lista.append(rec)
    dfTP = pd.DataFrame(lista, columns=colunas)
    dfTP = dfTP.sort_values(by=['Id'])
    dfTP = dfTP.reset_index(drop=True)
    dfTP['Valor'] = dfTP['Valor'].apply(lambda x: f'R$ {x:_.2f}'.replace('.', ',').replace('_', '.'))

    dfTPg = dfTP[['Nome', 'Estoque', 'Categoria']]
    dfTPg = dfTPg.rename(columns={'Nome':'Produtos'})
    dfTPg = dfTPg[dfTPg['Estoque'] <= 5]

    figdfTP = px.bar(dfTPg, x="Estoque", y="Produtos", color="Categoria", text_auto=True, orientation='h')
    figdfTP.update_traces(textposition="outside")

    colunas = ['Id', 'Nome', 'CPF', 'Data de Inclusão', 'Status', 'Estado']
    lista = []
    recset = consulta('select * from cliente')
    for rec in recset:
        lista.append(rec)
    dfCL = pd.DataFrame(lista, columns=colunas)
    dfCL = dfCL.sort_values(by=['Id'])
    dfCL = dfCL.reset_index(drop=True)

    dfCLg = dfCL.groupby(['Estado','Status']).count()
    dfCLg = dfCLg.rename(columns={'Nome':'Clientes'})
    dfCLg = dfCLg['Clientes']
    dfCLg = dfCLg.reset_index()

    figdfCL = px.bar(dfCLg, x="Estado", y="Clientes", color="Status", text_auto=True)
    figdfCL.update_traces(textposition="outside")

    colunas = ['Id Pedido', 'Vendedor', 'Cliente', 'Total', 'Data']
    lista = []
    recset = consulta('select * from pedido_lista')
    for rec in recset:
        lista.append(rec)
    PeLt = pd.DataFrame(lista, columns=colunas)
    PeLt = PeLt.sort_values(by=['Id Pedido'], ascending=False)
    PeLt = PeLt.reset_index(drop=True)
    PeLt['Total'] = PeLt['Total'].apply(lambda x: f'R$ {x:_.2f}'.replace('.', ',').replace('_', '.'))
    def criar_link(x):
        return f"<a href='http://127.0.0.1:8050/pesquisa={x}' target='_blank'><p style='text-align:center'>{x}</p></a>"
    def alinhar_link(x):
        return f"<p style='text-align:center'>{x}</p>"
    PeLt['Vendedor'] = PeLt['Vendedor'].apply(lambda x: alinhar_link(x))
    PeLt['Cliente'] = PeLt['Cliente'].apply(lambda x: alinhar_link(x))
    PeLt['Vendedor'] = PeLt['Vendedor'].apply(lambda x: alinhar_link(x))
    PeLt['Total'] = PeLt['Total'].apply(lambda x: alinhar_link(x))
    PeLt['Data'] = PeLt['Data'].apply(lambda x: alinhar_link(x))
    PeLt['Id Pedido'] = PeLt['Id Pedido'].apply(lambda x: criar_link(x))

    colunas = ['Id Transação', 'Id Vendedor', 'Valor', 'Quantidade', 'Data']
    lista = []
    recset = consulta('select idtransacao, idvendedor, valor, quantidade, iddata from pedido')
    for rec in recset:
        lista.append(rec)
    PeG = pd.DataFrame(lista, columns=colunas)
    PeG = PeG.sort_values(by=['Id Transação'])
    PeG = PeG.reset_index(drop=True)

    PeG['Mês'] = PeG['Data'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M'))
    PeG = PeG[(PeG['Mês'] >= datetime.strptime(f"{datetime.today().day}/{(datetime.today().month - 6) if (datetime.today().month - 6) > 0 else (12 + (datetime.today().month - 6))}/{datetime.today().year if (datetime.today().month - 6) > 0 else (datetime.today().year - 1)}", '%d/%m/%Y')) & (PeG['Mês'] <= datetime.today())]
    PeG2 = PeG.copy()
    PeG2['Total'] = PeG2['Quantidade'] * PeG2['Valor']
    PeG2['Mês'] = PeG2['Mês'].apply(lambda x: datetime.strptime(datetime.strftime(x, '%b - %Y'), '%b - %Y'))
    PeG2 = PeG2[['Mês', 'Total']].groupby(['Mês'],).sum().reset_index()
    
    figdfPe = px.line(PeG2, x='Mês', y="Total", text="Total")
    figdfPe.update_traces(textposition="top center")

    return [
        dbc.Tabs(
            [
                dbc.Tab(
                    #Tabela colaboradores tela inicial
                    label="Colaboradores",
                    tab_id="colaboradores",
                    children = [
                        html.H1("Consulta Colaboradores", style={'textAlign': 'center', 'margin-top': '1%', 'margin-bottom': '1%'}),
                        dash_table.DataTable(
                            id='tabelaColaboradores',
                            columns=[
                                {"name": i, "id": i} for i in dfTC.columns
                            ],
                            data=dfTC.to_dict('records'),
                            style_header = {'textAlign': 'center', 'font-weight':'bold'},
                            style_data = {'textAlign': 'center'},
                            filter_action="native",
                            filter_options = {'placeholder_text':'Filtar Dados...'},
                            page_action="native",
                            page_current= 0,
                            page_size= 10,
                            persistence=True,
                            cell_selectable=False
                        ),
                        html.Hr(style={'margin-top': '1%', 'margin-bottom': '1%'}),
                        html.H2(
                            ["Gráficos"],
                            style={'margin-top': '1%', 'margin-bottom': '1%', 'textAlign': 'center'},
                            ),
                        html.H4(
                            ["Relação Colaboradores por Setor/Estado"],
                            style={'margin-top': '1%', 'margin-bottom': '1%'},
                            ),
                        dcc.Graph(
                            id='grafico-colaboradores',
                            figure=figdfTC,
                            config={"displayModeBar": False}
                        ),
                    ],
                    ),
                    dbc.Tab(
                        #Tabela produto tela inicial
                        label="Produtos",
                        tab_id="Produtos",
                        children = [
                            html.H1("Consulta Produtos", style={'textAlign': 'center', 'margin-top': '1%', 'margin-bottom': '1%'}),
                            dash_table.DataTable(
                                id='tabelaProdutos',
                                columns=[
                                    {"name": i, "id": i} for i in dfTP.columns
                                ],
                                data=dfTP.to_dict('records'),
                                style_header = {'textAlign': 'center', 'font-weight':'bold'},
                                filter_action="native",
                                style_data = {'textAlign': 'center'},
                                filter_options = {'placeholder_text':'Filtar Dados...'},
                                page_action="native",
                                page_current= 0,
                                page_size= 10,
                                persistence=True,
                                cell_selectable=False
                            ),
                            html.Hr(style={'margin-top': '1%', 'margin-bottom': '1%'}),
                            html.H2(
                                ["Gráficos"],
                                style={'margin-top': '1%', 'margin-bottom': '1%', 'textAlign': 'center'},
                                ),
                            html.H4(
                                ["Relação Produtos com Baixo Estoque"],
                                style={'margin-top': '1%', 'margin-bottom': '1%'},
                                ),
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText("Mínimo:"), 
                                    dbc.Input(placeholder="Inserir valor mínimo", type="number", id='idmin', value=0),
                                    dbc.InputGroupText("Máximo:"),
                                    dbc.Input(placeholder="Inserir valor máximo", type="number", id='idmax', value=5),
                                    dbc.Button('Pesquisar', id='botaoPesquisarG2'),
                                ],
                                className="mb-3",
                                style={'margin-top': '2%'}
                            ),
                            html.Div(
                                [
                                    dcc.Graph(
                                        id='grafico-produtos',
                                        figure=figdfTP,
                                        config={"displayModeBar": False}
                                    ),
                                ],
                                id='alt-grafico-produtos'
                            ),
                        ],
                    ),
                    dbc.Tab(
                        #Tabela produto tela inicial
                        label="Clientes",
                        tab_id="Clientes",
                        children = [
                            html.H1("Consulta Clientes", style={'textAlign': 'center', 'margin-top': '1%', 'margin-bottom': '1%'}),
                            dash_table.DataTable(
                                id='tabelaClientes',
                                columns=[
                                    {"name": i, "id": i} for i in dfCL.columns
                                ],
                                data=dfCL.to_dict('records'),
                                style_header = {'textAlign': 'center', 'font-weight':'bold'},
                                filter_action="native",
                                style_data = {'textAlign': 'center'},
                                filter_options = {'placeholder_text':'Filtar Dados...'},
                                page_action="native",
                                page_current= 0,
                                page_size= 10,
                                persistence=True,
                                cell_selectable=False
                            ),
                            html.Hr(style={'margin-top': '1%', 'margin-bottom': '1%'}),
                            html.H2(
                                ["Gráficos"],
                                style={'margin-top': '1%', 'margin-bottom': '1%', 'textAlign': 'center'},
                                ),
                            html.H4(
                                ["Relação Clientes por Estado"],
                                style={'margin-top': '1%', 'margin-bottom': '1%'},
                                ),
                            dcc.Graph(
                                id='grafico-clientes',
                                figure=figdfCL,
                                config={"displayModeBar": False}
                            ),
                        ],
                    ),
                    dbc.Tab(
                        #Tabela produto tela inicial
                        label="Pedidos",
                        tab_id="Pedidos",
                        children = [
                            html.H1("Consulta Pedidos", style={'textAlign': 'center', 'margin-top': '1%', 'margin-bottom': '1%'}),
                            dash_table.DataTable(
                                id='tabelaPedidos',
                                columns=[
                                    {"name": i, "id": i, "presentation": "markdown"} for i in PeLt.columns
                                ],
                                data=PeLt.to_dict('records'),
                                style_header = {'textAlign': 'center', 'font-weight':'bold'},
                                filter_action="native",
                                style_data = {'textAlign': 'center'},
                                filter_options = {'placeholder_text':'Filtar Dados...'},
                                page_action="native",
                                page_current= 0,
                                page_size= 10,
                                persistence=True,
                                cell_selectable=False,
                                markdown_options={"html": True}
                            ),
                            html.Hr(style={'margin-top': '1%', 'margin-bottom': '1%'}),
                            html.H2(
                                ["Gráficos"],
                                style={'margin-top': '1%', 'margin-bottom': '1%', 'textAlign': 'center'},
                                ),
                            html.H4(
                                ["Relação Valor dos Pedidos por Data (Padrão 6 Meses)"],
                                style={'margin-top': '1%', 'margin-bottom': '1%'},
                                ),
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupText("Data: "), 
                                    dbc.Input(placeholder="Inserir data inicial", type="date", id='datamin'),
                                    dbc.InputGroupText(" Até "),
                                    dbc.Input(placeholder="Inserir data final", type="date", id='datamax'),
                                    dbc.Button('Pesquisar', id='botaoPesquisarG4'),
                                ],
                                className="mb-3",
                                style={'margin-top': '2%'}
                            ),
                            html.Div(
                                [
                                    dcc.Graph(
                                        id='grafico-pedidos',
                                        figure=figdfPe,
                                        config={"displayModeBar": False}
                                    ),
                                ],
                                id='alt-grafico-pedidos'
                            ),
                        ],
                    ),
            ],
            id="tabs",
            persistence='True',
        ),
    ]

layout = html.Div(children=[
    html.Div(
        dbc.Button("Atualizar Dados", color="warning", className="mb-3", id='atualizar'),
    ),
    html.Div(
        [],
        id='tabelas',
        className='output-example-loading',
    ),
])

@callback(
    Output("tabelas", "children"),
    Input("atualizar", "n_clicks"),
)
def tabelasFunc(n1):
    """ Função botão atualizar informações tabelas iniciais. """
    if n1:
        return tabelas()
    return tabelas()

@callback(
    Output("alt-grafico-produtos", "children"),
    Input("botaoPesquisarG2", "n_clicks"),
    State("alt-grafico-produtos", "children"),
    State("idmin", "value"),
    State("idmax", "value"),
    )
def tabelaProdutos(n_clicks, n1, v1, v2):
    """ Inserir sacola """
    global dfTP
    if n_clicks:
        if v1 == None or v2 == None:
            return n1
        else:
            colunas = ['Id', 'Nome', 'Valor', 'Categoria', 'Estoque']
            lista = []
            recset = consulta('select * from produto')
            for rec in recset:
                lista.append(rec)
            dfTP = pd.DataFrame(lista, columns=colunas)
            dfTP = dfTP.sort_values(by=['Id'])
            dfTP = dfTP.reset_index(drop=True)
            dfTP['Valor'] = dfTP['Valor'].apply(lambda x: f'R$ {x:_.2f}'.replace('.', ',').replace('_', '.'))

            dfTPg = dfTP[['Nome', 'Estoque', 'Categoria']]
            dfTPg = dfTPg.rename(columns={'Nome':'Produtos'})
            dfTPg = dfTPg[(dfTPg['Estoque'] >= v1) & (dfTPg['Estoque'] <= v2)]

            figdfTP = px.bar(dfTPg, x="Estoque", y="Produtos", color="Categoria", text_auto=True, orientation='h')
            figdfTP.update_traces(textposition="outside")

            return [
                dcc.Graph(
                    id='grafico-produtos',
                    figure=figdfTP,
                    config={"displayModeBar": False}
                ),
            ]
    return n1

@callback(
    Output("alt-grafico-pedidos", "children"),
    Input("botaoPesquisarG4", "n_clicks"),
    State("alt-grafico-pedidos", "children"),
    State("datamin", "value"),
    State("datamax", "value"),
    )
def tabelaPedidos(n_clicks, n1, v1, v2):
    """ Inserir sacola """
    global dfTP
    if n_clicks:
        if v1 == None or v2 == None or v1 == "" or v2 == "":
            return n1
        else:
            colunas = ['Id Transação', 'Id Vendedor', 'Valor', 'Quantidade', 'Data']
            lista = []
            recset = consulta('select idtransacao, idvendedor, valor, quantidade, iddata from pedido')
            for rec in recset:
                lista.append(rec)
            PeG = pd.DataFrame(lista, columns=colunas)
            PeG = PeG.sort_values(by=['Id Transação'])
            PeG = PeG.reset_index(drop=True)

            print(f'{v1} - {v2}')

            PeG['Mês'] = PeG['Data'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M'))
            PeG = PeG[(PeG['Mês'] >= datetime.strptime(v1, '%Y-%m-%d')) & (PeG['Mês'] <= datetime.strptime(v2, '%Y-%m-%d'))]
            PeG2 = PeG.copy()
            PeG2['Total'] = PeG2['Quantidade'] * PeG2['Valor']
            PeG2['Mês'] = PeG2['Mês'].apply(lambda x: datetime.strptime(datetime.strftime(x, '%b - %Y'), '%b - %Y'))    
            PeG2 = PeG2[['Mês', 'Total']].groupby(['Mês'],).sum().reset_index()

            figdfPe = px.line(PeG2, x='Mês', y="Total", text="Total")
            figdfPe.update_traces(textposition="top center")
            return [
                dcc.Graph(
                    id='grafico-pedidos',
                    figure=figdfPe,
                    config={"displayModeBar": False}
                ),
            ]
    return n1