
import pandas as pd
from dash import Dash, dcc, html, dash_table
import plotly.express as px

from OS import get_system
from packages import get_cross_platform_packages

import time

def main():
    start_time = time.time()

    pkgs = get_system().get_packages()
    pkgs.extend(get_cross_platform_packages())

    # Stop measuring time here
    end_time = time.time()
    elapsed_time = end_time - start_time

    df = pd.DataFrame(pkgs)

    total_packages = len(df)
    source_counts = df['source'].value_counts().reset_index()
    source_counts.columns = ['source', 'count']

    fig = px.pie(
        source_counts,
        values='count',
        names='source',
        hole=0.5,
        title="Package Distribution by Source"
    )

    app = Dash(__name__)

    def header_line(text):
        return html.Div(text, style={'fontSize': 20, 'margin': '10px'})

    app.layout = html.Div([
        html.H1("Package Report"),
        html.Div([
            header_line(f"Всего пакетов обнаружено: {total_packages}"),
            header_line(f"Время сканирования: {elapsed_time:.2f} с"),
            dcc.Graph(figure=fig)
        ]),
        html.Div([
            dash_table.DataTable(
                id='table',
                columns=[
                    {"name": "Name", "id": "name"},
                    {"name": "Version", "id": "version"},
                    {"name": "Source", "id": "source"},
                ],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '5px'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            )
        ], style={'marginTop': 30}),
    ])

    app.run_server(debug=True)

if __name__ == "__main__":
    main()
