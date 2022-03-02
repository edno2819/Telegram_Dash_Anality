from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc
from wordcloud import WordCloud
import plotly.express as px
from app import app
from utils import *
import dash
from processing import RemoveStopWords
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
                html.H6("Selecione os grupos:", className="card-text"),
                html.Br(),
                dcc.Dropdown(id='groups', 
                        options=[{'label':key, 'value':Analy.CANAIS[key]} for key in Analy.CANAIS.keys()],
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
                html.H4("Nuvens de Palavras", className="card-title", style={"text-align": "center"}),
                dcc.Graph(id='wordcloud', figure={}, config={'displayModeBar': False}),
            ]
        ),
    ],
    color="light",
)
 

# *********************************************************************************************************
cloud_words_layout = html.Div([
    dbc.Row([dbc.Col(image_card, width=4), dbc.Col(graph_card, width=8)], justify="around")
])
# *********************************************************************************************************


# Word Cloud **********************************************************************************************
@app.callback(
    Output('wordcloud','figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('groups','value'), 
    Input('submit-filter','n_clicks')
)
def create_cloud(start_date, end_date, groups, submit):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'n_clicks' in changed_id:

        Analy.banco.reconnect()
        msgs = Analy.all_msgs_from_canais(groups, (start_date, end_date))
        msgs = RemoveStopWords(' '.join(msgs))
        wordcloud = WordCloud(background_color='white', height=450, width=600).generate(msgs)

        fig_wordcloud = px.imshow(wordcloud, template='ggplot2')
        fig_wordcloud.update_layout(margin=dict(l=100, r=20, t=45, b=20), width=600, height=450)
        fig_wordcloud.update_xaxes(visible=False)
        fig_wordcloud.update_yaxes(visible=False)

        return fig_wordcloud
    return dash.no_update
