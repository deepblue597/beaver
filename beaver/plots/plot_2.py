import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import threading
import time
import random
import plotly.express as px
from plotly.subplots import make_subplots

ys = []
ys2 = []
metrics_values = { 
    'MAE':[2, 3, 1,10], # replace with your own data source
    'MSE':[2, 3, 1,10], # replace with your own data source
}
# Background data simulator
def update_data():
    while True:
        time.sleep(1)
        for metric_name in metrics_values.keys():
            # Simulate new data for each metric
            metrics_values[metric_name].append(random.randint(0, 100))
        
        ys2.append( random.randint(-20, 20))
        print("Dash app is running...")

def add_metrics(fig , row , col ) : 
        for metric_name, values in metrics_values.items():
            fig.add_trace(go.Scatter(
                y=values,
                mode="lines",
                name=f"{metric_name}"
            ), row=row, col=col)

 
def run_dash_app():
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H2("Pipelines' Plots" , style={
        'textAlign': 'center',  # Center the text

        'fontFamily': 'sans-serif',  # Change the font family
        'font-weight': 'normal',  # Make the text bold
        }),
        dcc.Graph(id='live-graph'),
        #You can add interval to update the graph every 2 seconds ()
        dcc.Interval(id='interval', interval=2000 , n_intervals=0)
    ])

    @app.callback(
        Output('live-graph', 'figure'),
        [Input('interval', 'n_intervals')]
    )
    def update_graph(n):
        # Create the figure
        #figure = go.Figure(data=[go.Scatter(y=ys, mode='lines')])
        figure = make_subplots(rows=2, cols=1, vertical_spacing=0.1)
        # Set the labels and title
        add_metrics(figure, row=1, col=1)
        figure.add_trace(
            go.Scatter(y=ys2, mode='lines', name='Bottom'),
            row=2, col=1
        )

        figure.update_layout(height=600, title="Live Metrics", margin=dict(t=40, b=40) , 
                                yaxis_title='Values'  ),
        return figure

    app.run(debug=True, use_reloader=False)


if __name__ == '__main__':
    threading.Thread(target=run_dash_app, daemon=True).start()
    update_data()
    