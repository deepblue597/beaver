import dash
from dash import Dash, html, dcc
from dash import html, dcc, callback, Input, Output
app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container, 
    
    html.Div([
    html.H1('This is our Analytics page'),
    html.Div([
        "Select a city: ",
        dcc.RadioItems(
            options=['New York City', 'Montreal', 'San Francisco'],
            value='Montreal',
            id='analytics-input'
        )
    ]),
    html.Br(),
    html.Div(id='analytics-output'),
])
])
@app.callback(
    Output('analytics-output', 'children'),
    Input('analytics-input', 'value')
)

def update_city_selected(input_value):
    return f'You selected: {input_value}'
if __name__ == '__main__':
    app.run(debug=True)