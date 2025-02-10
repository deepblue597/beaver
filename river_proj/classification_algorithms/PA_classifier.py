# %%
from river_proj import linear_model, metrics, datasets

# Load the dataset
dataset = datasets.Phishing()

# Define the Passive-Aggressive Classifier
model = linear_model.PAClassifier(
    C=0.2,
    mode=1
)

# Define the evaluation metric
metric = metrics.Accuracy() + metrics.LogLoss()

# Train and evaluate the model
for x, y in dataset:
    y_pred = model.predict_one(x)  # Predict
    metric.update(y, model.predict_proba_one(x))
    # metric.update(y, y_pred)       # Update metric
    model.learn_one(x, y)          # Learn

# Print the final accuracy
print(metric)

# %%
