# %%
from river import metrics
import matplotlib.pyplot as plt
import seaborn as sns

y_true = ['cat', 'ant', 'cat', 'cat', 'ant', 'bird']
y_pred = ['ant', 'ant', 'cat', 'cat', 'ant', 'cat']

metric = metrics.ConfusionMatrix()

for yt, yp in zip(y_true, y_pred):
    metric.update(yt, yp)


classes = sorted(metric.classes)
data = [[metric.data[true][pred] for pred in classes]
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
