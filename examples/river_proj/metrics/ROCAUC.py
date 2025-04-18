# %%
from river import metrics

y_true = [0,  0,   1,  1]
y_pred = [.1, .4, .35, .8]

metric = metrics.ROCAUC()

for yt, yp in zip(y_true, y_pred):
    metric.update(yt, yp)

metric
# %%
