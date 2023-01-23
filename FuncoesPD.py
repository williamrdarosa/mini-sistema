import dash
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import datetime
import io
import webbrowser
from dash import Input, Output, State, html, dcc
from db import consulta, inclusao

def menu(nome, menusSuspensos, caminho = "/", cor = "primary", temaDark = True):
    return dbc.NavbarSimple(
        children=menusSuspensos,
        brand=nome,
        brand_href=caminho,
        color=cor,
        dark=temaDark,
    )

def menuSuspenso(rotulo, botoes, navegacao = True, naBarraNav = True):
    return dbc.DropdownMenu(  
        children=botoes,
        nav=navegacao,
        in_navbar=naBarraNav,
        label=rotulo,
    )

