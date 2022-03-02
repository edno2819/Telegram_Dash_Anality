import dash_bootstrap_components as dbc
from dash import html
from dash import dash_table

from utils import *



df = Analy.all_msgs_from_all_canais()
df

graph_card = dbc.Card(
    [   html.Hr(),
        dbc.CardBody(
            [
                html.H4("Gráfico de recorrência de temas", className="card-title", style={"text-align": "center"}),
                dash_table.DataTable(
                    filter_action="native",
                    page_current= 0,
                    page_size= 50,

                    style_data={
                        'whiteSpace': 'normal',
                    },
                    data=df.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in df.columns],
                    css=[{
                        'selector': '.dash-spreadsheet td div',
                        'rule': '''
                            line-height: 15px;
                            max-height: 30px; min-height: 30px; height: 30px;
                            display: block;
                            overflow-y: hidden;
                        '''
                    }],
                    tooltip_data=[
                        {
                            column: {'value': str(value), 'type': 'markdown'}
                            for column, value in row.items()
                        } for row in df.to_dict('records')
                    ],
                    tooltip_duration=None,

                    style_cell_conditional=[
                        {'if': {'column_id': 'Grupo'},
                        'width': '25%'}
                    ],

                    style_cell={'textAlign': 'left'}
                )
            ]
        ),
    ],
    color="light",
)
 

# *********************************************************************************************************
datatable_layout = html.Div([
    dbc.Row([dbc.Col(graph_card, width=12)], justify="around")
])
# *********************************************************************************************************


    
