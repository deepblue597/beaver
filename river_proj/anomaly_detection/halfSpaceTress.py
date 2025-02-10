# %%

from river_proj import evaluate
from river_proj import compose, datasets, metrics, preprocessing, anomaly, evaluate
import matplotlib.pyplot as plt

# Initialize the model pipeline
model = compose.Pipeline(
    preprocessing.MinMaxScaler(),
    anomaly.HalfSpaceTrees(seed=42)
)

# Load the dataset
dataset = datasets.CreditCard().take(2500)

# Lists to store data points and anomaly scores
data_points = []
anomaly_scores = []

# Evaluate the model and collect anomaly scores
for x, y in dataset:
    score = model.score_one(x)
    data_points.append(x)
    anomaly_scores.append(score)
    model.learn_one(x)

# Convert data points to a 2D array for plotting
data_points = [{k: v for k, v in point.items()} for point in data_points]

# Plot the data points and highlight anomalies
plt.figure(figsize=(10, 5))
for i, point in enumerate(data_points):
    # Assuming 'V1' and 'V2' are the features to plot
    x, y = point['V1'], point['V2']
    if anomaly_scores[i] > 0.5:  # Threshold for anomaly detection
        plt.scatter(x, y, color='red', s=10, label='Anomaly' if i == 0 else "")
    else:
        plt.scatter(x, y, color='blue', s=10, label='Normal' if i == 0 else "")

plt.xlabel('V1')
plt.ylabel('V2')
plt.title('Anomaly Detection using HalfSpaceTrees')
plt.legend()
plt.show()

# %%
datasets.CreditCard().desc
# %%

model = model.clone()

evaluate.progressive_val_score(
    dataset=datasets.CreditCard().take(2500),
    model=model,
    metric=metrics.ROCAUC(),
    print_every=1000
)
# %%
