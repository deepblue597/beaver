# %%
from river import metrics

y_true = [0, 0, 0, 1, 1, 1]
y_pred = [0, 0, 1, 1, 0, 0]

metric = metrics.FBeta(beta=2) + metrics.F1() + metrics.Accuracy()
for yt, yp in zip(y_true, y_pred):
    metric.update(yt, yp)

metric

# %%
