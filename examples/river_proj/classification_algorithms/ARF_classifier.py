# %%
from river import evaluate
from river import forest
from river import metrics
from river.datasets import synth
import matplotlib.pyplot as plt
import seaborn as sns

# %%
dataset = synth.ConceptDriftStream(
    seed=42,
    position=500,
    width=40
).take(1000)

model = forest.ARFClassifier(seed=8, leaf_prediction="mc")

metric = metrics.Accuracy()

evaluate.progressive_val_score(dataset, model, metric)
# %%
model.n_warnings_detected(), model.n_drifts_detected()
# %%
metric.cm
# %%
# Get sorted class labels. Could also be metric.cm.classes
classes = sorted(metric.cm.classes)
data = [[metric.cm.data[true][pred] for pred in classes]
        for true in classes]  # Convert to 2D list

# Plot the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(data, annot=True, fmt=".0f", cmap=sns.color_palette(
    "Blues", as_cmap=True), xticklabels=classes, yticklabels=classes)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix Heatmap")
plt.show()

# %%
