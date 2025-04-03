# %%
from river import neighbors
from river import metrics
from river import linear_model

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
