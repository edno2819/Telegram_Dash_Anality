from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import html
from app import app

from tabs.frequencia_temas import frequencia_temas_layout
from tabs.super_users import super_usuarios_layout
from tabs.cloud_words import cloud_words_layout
from tabs.frequencia import frequencia_layout
from tabs.msg_table import datatable_layout

from utils import *


server = app.server

app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Word Cloud", tab_id="cloud_words_layout", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Frequência Sentimentos", tab_id="frequencia_layout", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Tabela de Mensagens", tab_id="datatable_layout", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Frequência de Temas", tab_id="frequencia_temas_layout", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Super Usuários", tab_id="super_usuarios_layout", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
            ],
            id="tabs",
            active_tab="tab-mentions",
        ),
    ], className="mt-3"
)

app.layout = dbc.Container([
    html.Hr(),
    html.Div(html.Img(src='assets\\tele.png', style={'height':'60px', 'width':'70px'}), style={"textAlign": "center"}),
    dbc.Row(dbc.Col(html.H1("ANALISE TELEGRAM DASHBOARD", style={"textAlign": "center"}), width=12)),
    html.Hr(),
    dbc.Row(dbc.Col(app_tabs, width=16), className="mb-3"),
    html.Div(id='content', children=[])

])

@app.callback(
    Output("content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "cloud_words_layout":
        return cloud_words_layout
    elif tab_chosen == "frequencia_layout":
       return frequencia_layout
    elif tab_chosen == "datatable_layout":
        return datatable_layout
    elif tab_chosen == "frequencia_temas_layout":
        return frequencia_temas_layout
    elif tab_chosen == "super_usuarios_layout":
        return super_usuarios_layout

    return cloud_words_layout



if __name__=='__main__':
    app.run_server(debug=True)