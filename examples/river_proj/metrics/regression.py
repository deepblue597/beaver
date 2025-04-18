# %%

from river import metrics

y_true = [3, -0.5, 2, 7]
y_pred = [2.5, 0.0, 2, 8]

metric = metrics.MAE()

for yt, yp in zip(y_true, y_pred):
    metric.update(yt, yp)
    print(metric.get())

# %%
metric = metrics.MAPE() + metrics.R2() + metrics.MSE() + metrics.R2()

for yt, yp in zip(y_true, y_pred):
    metric.update(yt, yp)
    print(metric)


# %%
metric = metrics.MSE()

for yt, yp in zip(y_true, y_pred):
    metric.update(yt, yp)
    print(metric.get())
# %%
metric = metrics.R2()
for yt, yp in zip(y_true, y_pred):
    metric.update(yt, yp)
    print(metric.get())
# %%
