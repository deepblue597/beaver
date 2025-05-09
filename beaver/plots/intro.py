# import plotly.express as px

# fig = px.line(x=["a","b","c"], y=[1,3,2], title="sample figure")
# print(fig)
# fig.show()

#%% 


from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import json

fig = px.line(
    x=["a","b","c"], y=[1,3,2], # replace with your own data source
    title="sample figure", height=325
)

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Displaying figure structure as JSON'),
    dcc.Graph(id="graph", figure=fig),
    # dcc.Clipboard(target_id="structure"),
    # html.Pre(
    #     id='structure',
    #     style={
    #         'border': 'thin lightgrey solid',
    #         'overflowY': 'scroll',
    #         'height': '275px'
    #     }
    # ),
])


@app.callback(
   #In Dash, the figure property is a predefined attribute of the dcc.Graph component. When you define a dcc.Graph in your layout, like this:

    #The figure property is automatically associated with 
    #the Plotly figure (fig) you pass to it. 
    # This property holds the entire JSON representation of the Plotly 
    # figure, which includes all the data, layout, and configuration details.
    #Output component that will be updated by the callback
    #Output("structure", "children"),
    #List of Input components that will trigger the callback
    Input("graph", "figure"))

def display_structure(fig_json):
    return json.dumps(fig_json, indent=2)
"""
The display_structure function is the callback function associated with the @app.callback.
The fig_json parameter receives the value of the figure property from the dcc.Graph component (in this case, the Plotly figure's JSON representation).
The function processes this input (formats it as a JSON string with indentation) and returns it.
"""

app.run(debug=True)
# %%
