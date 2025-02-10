# %%
from river_proj import linear_model, metrics, datasets
import matplotlib.pyplot as plt

# Load a regression dataset (e.g., Trump Approval dataset)
dataset = datasets.TrumpApproval()

# Define the Passive-Aggressive Regressor model
model = linear_model.PARegressor(C=1e-5)

# Define the evaluation metric (e.g., Mean Absolute Error)
metric = metrics.MAE()

x_axis = []
y_true = []
y_pred = []
# Train and evaluate the model
for x, y in dataset:
    x_axis.append(x['ordinal_date'])
    y_true.append(y)
    y_predi = model.predict_one(x)  # Predict the value
    y_pred.append(y_predi)
    metric.update(y, y_predi)       # Update the metric
    model.learn_one(x, y)          # Update the model

# Print the final MAE
print(f"Mean Absolute Error: {metric.get():.4f}")

# %%
# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(x_axis, y_true, label='Actual Approval Rating')
plt.plot(x_axis, y_pred, label='Predicted Approval Rating', linestyle='--')
plt.xlabel('Ordinal Date')
plt.ylabel('Approval Rating')
plt.title('Trump Approval Rating Over Time')
plt.legend()
plt.show()

# %%
