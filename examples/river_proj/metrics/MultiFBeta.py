# %%
from river import metrics
import matplotlib.pyplot as plt
import seaborn as sns

y_true = [0, 1, 2, 2, 2]
y_pred = [0, 0, 2, 2, 1]

metric = metrics.MultiFBeta(
    betas={0: 0.25, 1: 1, 2: 4},
    weights={0: 1, 1: 1, 2: 2}
)

for yt, yp in zip(y_true, y_pred):
    metric.update(yt, yp)
    print(metric)

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
