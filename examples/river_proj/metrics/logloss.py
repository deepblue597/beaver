# %%

from river import metrics

y_true = [True, False, False, True]
y_pred = [0.9,  0.1,   0.2,   0.65]

metric = metrics.LogLoss()
for yt, yp in zip(y_true, y_pred):
    metric.update(yt, yp)
    print(metric.get())
# %%
