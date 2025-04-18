# %%
from river import metrics
import matplotlib.pyplot as plt
import seaborn as sns

y_true = [0, 1, 2, 2, 0]
y_pred = [0, 1, 1, 2, 1]

metric = metrics.MicroFBeta(beta=2)
for yt, yp in zip(y_true, y_pred):
    metric.update(yt, yp)

metric

# %%
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

y_true = [0, 1, 2, 2, 0]
y_pred = [0, 1, 1, 2, 1]

metric = metrics.MicroF1()
for yt, yp in zip(y_true, y_pred):
    metric.update(yt, yp)

metric
# %%
