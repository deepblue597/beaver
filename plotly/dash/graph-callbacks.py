#%%
import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc, html 
import plotly.graph_objects as go 
# %%
df = pd.read_csv('../data/gapminderDataFiveYear.csv')
# %%
df
# %%

app = Dash() 

# %%
app.layout = html.Div(
    children= [ 
        dcc.Graph(
            id='graph', 

        ), 
        dcc.Dropdown(
            id='year-picker', 
            options=[
                {"label": str(year), "value": year} for year in df['year'].unique() 
            ], 
            value= df['year'].min() 
        )
    ]
)
#%%

@app.callback(
        Output(
            component_id='graph', 
            component_property='figure'
        ), 
        [ 
            Input(
                component_id='year-picker', 
                component_property='value'
            )
        ]

)

def update_figure(selected_year) : 
    
    # data only for selected year 
    filtered_df = df[df['year'] == selected_year]

    traces = [] 

    for continent in filtered_df['continent'].unique():  
        df_by_continent = filtered_df[filtered_df['continent'] == continent]
        traces.append(
            go.Scatter(
                x = df_by_continent['gdpPercap'], 
                y=df_by_continent['lifeExp'],
                mode = 'markers', 
                opacity=0.7,
                name=continent, 
                text = df_by_continent['country'],  # <-- Add this line
                hoverinfo = 'text+x+y'              

            )
        )

    

    return dict(
        data = traces, 
        layout = go.Layout(
            title = 'My plot', 
            xaxis= dict(
                title = 'GDP per capita', 
                type = 'log'
            ), 
            yaxis= dict(
                title = 'life expectancy'
            )
        )
    )



# %%

if __name__ == '__main__': 
    app.run() 