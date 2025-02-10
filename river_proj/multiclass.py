# %%
from river_proj import metrics
from river_proj import tree
from river_proj import datasets

dataset = datasets.ImageSegments()
dataset
# %%
x, y = next(iter(dataset))
x
# %%
y
# %%
x, y = next(iter(dataset))
x
# %%
y
# %%

model = tree.HoeffdingTreeClassifier()
model.predict_proba_one(x)
# %%
print(model.predict_one(x))
# %%
model.learn_one(x, y)
model.predict_proba_one(x)
# %%

model = tree.HoeffdingTreeClassifier()

metric = metrics.ClassificationReport()

for x, y in dataset:
    y_pred = model.predict_one(x)
    model.learn_one(x, y)
    if y_pred is not None:
        metric.update(y, y_pred)

metric
# %%
