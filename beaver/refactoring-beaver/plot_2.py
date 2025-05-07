import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import threading
import time
import random
import plotly.express as px
ys = [2]

# Background data simulator
def update_data():
    while True:
        time.sleep(1)
        ys.append(ys[-1] + random.randint(-10, 10))
        print("Dash app is running...")



 
def run_dash_app():
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H4('Interactive color selection with simple Dash example'),
        dcc.Graph(id='live-graph'),
        dcc.Interval(id='interval', interval=1000, n_intervals=0)
    ])

    @app.callback(
        Output('live-graph', 'figure'),
        [Input('interval', 'n_intervals')]
    )
    def update_graph(n):
        # Create the figure
        figure = go.Figure(data=[go.Scatter(y=ys, mode='lines')])

        # Set the labels and title
        figure.update_layout(
            title='Live Data Plot',  # Graph title
            xaxis_title='Time',      # X-axis label
            yaxis_title='Value',     # Y-axis label
        )

        return figure

    app.run(debug=True, use_reloader=False)


if __name__ == '__main__':
    threading.Thread(target=run_dash_app, daemon=True).start()
    update_data()
    