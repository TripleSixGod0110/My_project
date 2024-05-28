from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df

layout = dbc.Container([
    dbc.Row ([
        dbc.Col( html.Div([
                html.H1("Тепловая карта показателей"),
                html.P("Анализ основных показателей по странам мира с 2000 по 2015 годы."),
                html.P(" Используйте фильтр, чтобы увидеть результат.")
            ])

        )
    ]),

    html.Br(),

    dbc.Row ([
        dbc.Col([ 
            dbc.Label("Выберите показатель:"),
            dbc.RadioItems(
                options=[
                    {'label':'Продолжительность жизни', 'value': 'Life expectancy'},
                    {'label':'Население', 'value': 'Population'},
                    {'label':'ВВП', 'value': 'GDP'},
                    {'label':'Школьное образование', 'value': 'Schooling'},
                ],
                value='GDP',
                id='crossfilter-ind',
            ),
        ],width=3),

        dbc.Col([ dcc.Graph(id = 'choropleth', config={'displayModeBar': False}),

        ],width=9)
    ])
])



@callback(
    Output('choropleth', 'figure'),
    Input('crossfilter-ind', 'value')
)
def update_choropleth(indication):
    figure = px.choropleth(
        df,
        locations='Country',
        locationmode = 'country names',
        color=indication,
        hover_name='Country',
        hover_data = {'Country':True,'Year':True,'Status':False,
                    'Life expectancy':True,'Population':True,
                    'GDP':True,'Schooling':True,
                    'continent':False},
        labels={'Country':'Страна', 'Year':'Год',
                'Population':'Население', 'Life expectancy':'Продолжительность жизни',
                'GDP':'ВВП', 'Schooling':'Продолжительность обучения'},
        color_continuous_scale=px.colors.sequential.YlOrBr,
        animation_frame='Year',
        )
   
    figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        showlegend=False)
    return figure