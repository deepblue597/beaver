# %%
from river import evaluate
from river import metrics
from river import neighbors
from river import datasets

dataset = datasets.TrumpApproval()
dataset
# %%
x, y = next(iter(dataset))
x
# %%

model = neighbors.KNNRegressor()
model.predict_one(x)
# %%
model.learn_one(x, y)
# %%
model.predict_one(x)
# %%

model = neighbors.KNNRegressor()

metric = metrics.MAE()

for x, y in dataset:
    y_pred = model.predict_one(x)
    model.learn_one(x, y)
    metric.update(y, y_pred)

metric
# %%

model = neighbors.KNNRegressor()
metric = metrics.MAE()

evaluate.progressive_val_score(dataset, model, metric)
# %%
