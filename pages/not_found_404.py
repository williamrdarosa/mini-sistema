from dash import html
import dash

dash.register_page(__name__, name='Página não encontrada')

layout = html.H1("Página não encontrada.")