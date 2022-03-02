import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from app import app
from datetime import date, datetime, timedelta


from utils import *



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
                    min_date_allowed=date(2021, 1, 5),
                    max_date_allowed=date.today(),
                    initial_visible_month=date.today(),
                    start_date= (datetime.today() - timedelta(days=7)),
                    end_date=date.today(),
                ),

                html.Hr(),
                html.H6("Selecione a palavra chave:", className="card-text"),
                html.Br(),
                dcc.Input(id='word_filter_tema'),
                html.Br(),
                html.Hr(),
                html.H6("Selecione os grupos:", className="card-text"),
                html.Br(),
                dcc.Dropdown(id='groups_fre_tema', 
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
                html.H4("Gráfico de frequência de temas", className="card-title", style={"text-align": "center"}),
                dcc.Graph(id='line_chart_temas', figure={}),

            ]
        ),
    ],
    color="light",
)
 

# *********************************************************************************************************
frequencia_temas_layout = html.Div([
    dbc.Row([dbc.Col(image_card, width=4), dbc.Col(graph_card, width=8)], justify="around")
])
# *********************************************************************************************************

@app.callback(
    Output("line_chart_temas", "figure"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input("submit-filter", "n_clicks"), 
    Input("groups_fre_tema", "value"),
    Input("word_filter_tema", "value")
)
def update_graph_temas(start_date, end_date, n_clicks, canais, words_filter):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'n_clicks' in changed_id and words_filter not in ['', None] and canais not in ['', None]:   

        label_name = f'Filtro por Tema: {words_filter}'
        canais_frequencia_tema = dict()

        datas_list = Analy.frequencia_temas(canais, (start_date, end_date))
        datas_list_str = [str(data) for data in datas_list]

        groups_msgs = Analy.all_msgs_dict_from_canais_temas(canais, (start_date, end_date), 'mensagem, OrderDate')

        for canal in canais:
            canais_frequencia_tema[canal] =  list()
            x = Analy.filter_list_strings_temas(groups_msgs[canal], words_filter)
            x = [c[1] for c in x]

            for data in datas_list:
                canais_frequencia_tema[canal].append(x.count(data))

        fig = go.Figure(layout=go.Layout(title=go.layout.Title(text=label_name)))
        for canal in canais:
            fig.add_trace(go.Scatter(x=datas_list_str, y=canais_frequencia_tema[canal],
                                mode='lines',
                                name=canal))

        fig.update_layout(
                    legend=dict(orientation="h", yanchor="bottom",y=1.0,xanchor="right",x=1),
                    autosize=False,
                    width=700,
                    height=580)

        return fig
    return dash.no_update

    
