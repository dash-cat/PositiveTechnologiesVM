import asyncio
import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output
import plotly.express as px
from OS import get_system
from packages import get_cross_platform_packages
import time

def main():
    app = Dash(__name__)

    def get_data():
        start_time = time.time()
        pkgs = get_system().get_packages()
        pkgs.extend(asyncio.run(get_cross_platform_packages()))
        end_time = time.time()
        elapsed_time = end_time - start_time

        df = pd.DataFrame(pkgs, columns=["name", "version", "source"])
        return df, elapsed_time

    df, elapsed_time = get_data()

    def header_line(text):
        return html.Div(text, style={'fontSize': 20, 'margin': '10px'})

    app.layout = html.Div([
        html.H1("Package Report"),
        html.Div(id="summary"),
        html.Button("Обновить данные", id="refresh-button", n_clicks=0),
        dcc.Graph(id="pie-chart"),
        dcc.Graph(id="bar-chart"),  # New bar chart for percentage of collected versions
        dash_table.DataTable(
            id='table',
            columns=[
                {"name": "Name", "id": "name"},
                {"name": "Version", "id": "version"},
                {"name": "Source", "id": "source"},
            ],
            data=df.to_dict('records'),
            filter_action="native",
            sort_action="native",
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        ),
    ])

    @app.callback(
        [Output("summary", "children"), Output("pie-chart", "figure"), Output("bar-chart", "figure"), Output("table", "data")],
        Input("refresh-button", "n_clicks")
    )
    def update_data(n_clicks):
        new_df, new_elapsed_time = get_data()
        total_packages = len(new_df)
        
        # Pie chart data
        source_counts = new_df['source'].value_counts().reset_index()
        source_counts.columns = ['source', 'count']
        pie_fig = px.pie(
            source_counts,
            values='count',
            names='source',
            hole=0.5,
            title="Package Distribution by Source"
        )

        # Calculate percentage of version collection
        version_percentages = new_df.groupby('source').apply(
            lambda x: x['version'].notnull().sum() / len(x) * 100
        ).reset_index()
        version_percentages.columns = ['source', 'percentage']

        bar_fig = px.bar(
            version_percentages,
            x='source',
            y='percentage',
            title="Percentage of Collected Versions by Source",
            labels={'source': 'Source', 'percentage': 'Percentage (%)'},
            text_auto='.2f'
        )

        summary = [
            header_line(f"Всего пакетов обнаружено: {total_packages}"),
            header_line(f"Время сканирования: {new_elapsed_time:.2f} с")
        ]
        return summary, pie_fig, bar_fig, new_df.to_dict('records')

    app.run_server(debug=True)

if __name__ == "__main__":
    main()
