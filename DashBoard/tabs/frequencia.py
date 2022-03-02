import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from app import app

from utils import *
from model_nlp import predict
from datetime import date, datetime, timedelta



image_card = dbc.Card(
    [
        dbc.CardBody(
            [   
                html.H4("Filtros", className="card-title"),
                html.Hr(),

                html.H6("Selecione o intervalo de busca:", className="card-text"),
                html.Br(),
                dcc.DatePickerRange(
                    month_format='D/MM/Y',
                    display_format='D/MM/Y',
                    id='my-date-picker-range',
                    min_date_allowed=date(2021, 6, 5),
                    max_date_allowed=date.today(),
                    initial_visible_month=date.today(),
                    start_date= (datetime.today() - timedelta(days=7)),
                    end_date=date.today(),
                ),
                html.Hr(),

                html.H6("Selecione a palavra chave:", className="card-text"),
                html.Br(),
                dcc.Input(id='word_filter'),
                html.Br(),
                html.Hr(),
                html.H6("Selecione os grupos:", className="card-text"),
                html.Br(),
                dcc.Dropdown(id='groups_fre', 
                        options=[{'label':key, 'value':key} for key in Analy.CANAIS.keys()],
                        multi=True, style={"color": "#000000"}),

                html.Br(),
                html.Hr(),
                html.Button('Submit', id='submit-filter', n_clicks=0)
            ]
        ),
    ],
    color="light",
)

graph_card = dbc.Card(
    [   html.Hr(),
        dbc.CardBody(
            [
                html.H4("Gráfico de recorrência de sentimentos", className="card-title", style={"text-align": "center"}),
                dcc.Graph(id='line_chart', figure={}),

            ]
        ),
    ],
    color="light",
)
 

# *********************************************************************************************************
frequencia_layout = html.Div([
    dbc.Row([dbc.Col(image_card, width=4), dbc.Col(graph_card, width=8)], justify="around")
])
# *********************************************************************************************************

@app.callback(
    Output("line_chart", "figure"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input("submit-filter", "n_clicks"), 
    Input("groups_fre", "value"),
    Input("word_filter", "value")
)
def update_graph_card(start_date, end_date, n_clicks, canais, words_filter):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'n_clicks' in changed_id:   
        positivo, negativo = [],[]

        if words_filter!='' and words_filter!=None:
            words_filter = words_filter.split(',')
            label = f'Filtro por Palavra Chave: {" ".join(words_filter)}'

        else:
            words_filter = False
            label = 'Análise de todas as mensagens'

        groups_msgs = Analy.all_msgs_dict_from_canais(canais, (start_date, end_date))

        for grupo in groups_msgs.keys():
            analise_sentimentos = predict(Analy.filter_list_strings(groups_msgs[grupo], words_filter))

            positivo.append(analise_sentimentos.count(1))
            negativo.append(analise_sentimentos.count(0))


        fig = go.Figure(data=[
            go.Bar(name='Positivo', x=canais, y=positivo),
            go.Bar(name='Negativo', x=canais, y=negativo)
            ], 
            layout=go.Layout(title=go.layout.Title(text=label))
        )
        fig.update_layout(barmode='group',
                    autosize=False,
                    width=700,
                    height=680)

        return fig
    return dash.no_update

    
