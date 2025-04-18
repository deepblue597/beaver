# %%
from river import neighbors
from river import metrics
from river import linear_model
import matplotlib.pyplot as plt
import seaborn as sns

y_true = [True, False, True, True, True]
y_pred = [True, True, False, True, True]

metric = metrics.Accuracy()
for yt, yp in zip(y_true, y_pred):
    metric.update(yt, yp)

metric
# %%

model = linear_model.LogisticRegression()

metric.works_with(model)
# %%
metric.cm
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
