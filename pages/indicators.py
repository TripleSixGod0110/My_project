from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df  # Подставьте свои данные

# Создаем макет страницы "Статистика"
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([
            html.H1("Статистика"),
            html.P("Анализ основных показателей по странам мира."),
            html.P("Используйте фильтры для выбора континента и интервала лет, а также показателя."),
        ])),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Label("Выберите континент:"),
            dcc.Dropdown(
                id='continent-dropdown',
                options=[{'label': cont, 'value': cont} for cont in df['continent'].unique()],
                value=df['continent'].unique()[0],  # Значение по умолчанию
                multi=True  # Разрешаем множественный выбор
            ),
        ], width=3),
        dbc.Col([
            dbc.Label("Выберите интервал лет:"),
            dcc.RangeSlider(
                id='year-slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=[df['Year'].min(), df['Year'].max()],
                marks={str(year): str(year) for year in range(df['Year'].min(), df['Year'].max()+1)},
            ),
        ], width=6),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Label("Выберите показатель:"),
            dbc.RadioItems(
                options=[
                    {'label': 'Продолжительность жизни', 'value': 'Life expectancy'},
                    {'label': 'Население', 'value': 'Population'},
                    {'label': 'ВВП', 'value': 'GDP'},
                    {'label': 'Школьное образование', 'value': 'Schooling'},
                ],
                value='GDP',
                id='indicator-radio',
            ),
        ], width=3),
        dbc.Col([
            dcc.Graph(id='indicator-graph', config={'displayModeBar': False}),
        ], width=9),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='pie-chart', config={'displayModeBar': False}),
        ], width=12),  # Расширяем диаграмму на всю ширину
    ]),
])

# Callback для обновления графика при изменении фильтров
@callback(
    [
        Output('indicator-graph', 'figure'),
        Output('pie-chart', 'figure'),
    ],
    [
        Input('continent-dropdown', 'value'),
        Input('year-slider', 'value'),
        Input('indicator-radio', 'value'),
    ]
)
def update_graph(selected_continents, selected_years, selected_indicator):
    filtered_df = df[(df['continent'].isin(selected_continents)) &
                     (df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]
    
    # График для выбранного показателя
    line_fig = px.line(filtered_df, x='Year', y=selected_indicator, color='Country',
                       labels={'Year': 'Год', selected_indicator: selected_indicator},
                       title=f'Динамика {selected_indicator} по странам')
    
    line_fig.update_layout(margin={"r": 20, "t": 50, "l": 20, "b": 20})
    
    # Круговая диаграмма для суммарных значений выбранного показателя по континентам
    pie_fig = px.pie(filtered_df.groupby('continent').sum().reset_index(),
                     values=selected_indicator, names='continent',
                     title=f'Суммарные значения {selected_indicator} по континентам')
    
    return line_fig, pie_fig
