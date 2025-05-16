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


app = Dash() 
 
#fig = px.scatter(df, x="sepal_width", y="sepal_length") 
np.random.seed(42) 
random_x = np.random.randint(1 , 101 , 100 ) 
random_y = np.random.randint(1 , 101 , 100 )

app.layout = html.Div(
    children=[
        dcc.Graph(
            id = 'scatterplot',
            figure = dict(
                data = [ go.Scatter(
                    x = random_x , 
                    y = random_y , 
                    mode = 'markers', 
                    marker = dict(
                        size = 10 , 
                        color = 'rgb(51 , 153 , 204 )', 
                        line = {
                            'width' : 2   
                                
                                }
                    )
                    )], 
                layout = go.Layout(
                    title = 'My scatterplot', 
                    xaxis=  dict(
                        title = 'random x'
                    )
                ) 
            )
        )
    ]
)

if __name__ == '__main__' : 
    
    app.run() 