
# %%
from river_proj import datasets, preprocessing, linear_model, metrics, evaluate
import matplotlib.pyplot as plt

# Load the dataset
dataset = datasets.TrumpApproval()

# Extract data for plotting
dates = []
approvals = []
model = (
    preprocessing.StandardScaler() |
    linear_model.LinearRegression(intercept_lr=.1)
)
metric = metrics.MAE()

# Evaluate the model
evaluate.progressive_val_score(dataset, model, metric)

# Reset the dataset and lists for plotting
dataset = datasets.TrumpApproval()
dates = []
approvals = []
predictions = []

for x, y in dataset:
    dates.append(x['ordinal_date'])
    approvals.append(y)
    y_pred = model.predict_one(x)
    predictions.append(y_pred)
    model.learn_one(x, y)

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(dates, approvals, label='Actual Approval Rating')
plt.plot(dates, predictions, label='Predicted Approval Rating', linestyle='--')
plt.xlabel('Ordinal Date')
plt.ylabel('Approval Rating')
plt.title('Trump Approval Rating Over Time')
plt.legend()
plt.show()
# %%
