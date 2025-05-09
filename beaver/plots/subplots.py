from dash import Dash, html, dcc
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Create subplots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

fig.add_trace(
    go.Scatter(x=[1, 2, 3], y=[10, 20, 30], mode='lines', name="My Series"),
    row=1, col=1 
)

fig.add_trace(
    go.Scatter(x=[1, 2, 3], y=[30, 20, 10], mode='lines+markers', name='Bottom'),
    row=2, col=1
)

fig.update_layout(height=600, title_text="Subplots in Dash")

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dash App with Subplots"),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)
