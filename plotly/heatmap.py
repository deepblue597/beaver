#%% 
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix

# Example classification data
y_true = [0, 1, 0, 1, 0, 1, 1, 0, 1, 0]  # True labels
y_pred = [0, 1, 0, 0, 0, 1, 1, 1, 1, 0]  # Predicted labels

# Generate the confusion matrix
cm = confusion_matrix(y_true, y_pred)

# Create a heatmap
fig = go.Figure(data=go.Heatmap(
    z=cm,
    x=['Predicted 0', 'Predicted 1'],  # Predicted classes
    y=['True 0', 'True 1'],            # True classes
    colorscale='Viridis',
    texttemplate="%{z}"               # Display values in the heatmap
    
))

# Update layout
fig.update_layout(
    title='Confusion Matrix Heatmap',
    xaxis_title='Predicted Labels',
    yaxis_title='True Labels',
    
)

# Show the plot
fig.show()