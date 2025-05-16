import dash
from dash import dcc, html, Input, Output, ctx
import plotly.express as px
import numpy as np
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc, html
import plotly.graph_objects as go 
# # Dummy data
df = px.data.iris()
# heat_data = np.random.rand(10, 10)

# app = dash.Dash(__name__, suppress_callback_exceptions=True)

# app.layout = html.Div([
#     dcc.Location(id='url'),

#     # Navigation Buttons
#     html.Div([
#         html.Button("Metrics", id="btn-metrics", n_clicks=0),
#         html.Button("Heatmap", id="btn-heatmap", n_clicks=0),
#     ], style={'display': 'flex', 'gap': '10px', 'margin': '10px'}),

#     html.Hr(),

#     # Placeholder for page content
#     html.Div(id='page-content')
# ])

# # Pages
# metrics_layout = html.Div([
#     html.H2("Metrics Page"),
#     dcc.Graph(figure=px.scatter(df, x="sepal_width", y="sepal_length" ))
# ])

# heatmap_layout = html.Div([
#     html.H2("Heatmap Page"),
#     dcc.Graph(figure=px.imshow(heat_data, color_continuous_scale='Viridis'))
# ])

# # Navigation callback
# @app.callback(
#     Output('url', 'pathname'),
#     Input('btn-metrics', 'n_clicks'),
#     Input('btn-heatmap', 'n_clicks'),
#     prevent_initial_call=True
# )
# def navigate(n_metrics, n_heatmap):
#     triggered_id = ctx.triggered_id
#     if triggered_id == 'btn-metrics':
#         return '/'
#     elif triggered_id == 'btn-heatmap':
#         return '/heatmap'

# # Content callback
# @app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
# def render_page(pathname):
#     if pathname == '/heatmap':
#         return heatmap_layout
#     return metrics_layout

# if __name__ == '__main__':
#     app.run(debug=True)

app = Dash() 
 
fig = px.scatter(df, x="sepal_width", y="sepal_length") 
#fig.update_traces(marker=dict(color='#7FDBFF'))  # Use your text color or another light color
colors = {
    'background' : '#111111', 
    'text' : '#7FDBFF'    
}



app.layout = html.Div(
    children= [
        html.H1(
            'Hello world', 
            style=dict(
                textAlign = 'center', 
                color = colors['text']
            )

            ),
        html.Div('Web dashboards with Python'),
        dcc.Graph(id = 'example', figure = fig 
        )
        
    ], 
    style= {'backgroundColor' : colors['background']} 
) 

#updated version from the one that is being shown on the course 
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font=dict(color=colors['text']),
    title='scatter'
)

if __name__ == '__main__' : 
    
    app.run() 