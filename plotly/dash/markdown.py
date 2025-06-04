import pandas as pd 
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc, html 
import plotly.graph_objects as go 

app = Dash()

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/) specification of Markdown.

Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!

Markdown includes syntax for things like **bold text** and *italics*,
[links](http://commonmark.org/help), inline `code` snippets, lists,
quotes, and more.
'''

app.layout = html.Div([
    dcc.Markdown(children=markdown_text)
])

if __name__ == '__main__':
    app.run()

#%% 
#for info about a component (meeeeehhhh) 
print(help(html.Div))
# %%
