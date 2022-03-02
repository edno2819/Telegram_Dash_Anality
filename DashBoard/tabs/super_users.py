import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from app import app
from utils import *
from datetime import date, datetime, timedelta


image_card = dbc.Card(
    [
        dbc.CardBody(
            [   
                html.H4("Filtros", className="card-title"),
                html.Br(),
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

                html.H6("Selecione os grupos:", className="card-text"),
                html.Br(),
                dcc.Dropdown(id='groups_users', 
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
                html.H4("Gráfico de super usuários", className="card-title", style={"text-align": "center"}),
                dcc.Graph(id='bar_chart_users', figure={}),

            ]
        ),
    ],
    color="light",
)
 

# *********************************************************************************************************
super_usuarios_layout = html.Div([
    dbc.Row([dbc.Col(image_card, width=4), dbc.Col(graph_card, width=8)], justify="around")
])
# *********************************************************************************************************

@app.callback(
    Output("bar_chart_users", "figure"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input("submit-filter", "n_clicks"), 
    Input("groups_users", "value"),
)
def update_graph_users(start_date, end_date, n_clicks, canais):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'n_clicks' in changed_id:   
        qtd = 15
        user_list = Analy.super_uses(canais, (start_date, end_date))
        user_list = user_list[:qtd]
        user_name = [user[0] for user in user_list]
        user_value = [user[1] for user in user_list]
        user_name.reverse()
        user_value.reverse()

        fig = go.Figure([go.Bar(x=user_name, y=user_value)],layout=go.Layout(title=go.layout.Title(text='Super Usuários')))

        fig.update_layout(
                        autosize=False,
                        width=700,
                        height=580)

        return fig
    return dash.no_update

    
