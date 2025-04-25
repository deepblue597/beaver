# %%
import functools
from river import datasets
from river import evaluate
from river import metrics
from river import neighbors
from river import preprocessing
from river import utils

dataset = datasets.Phishing()

# %%
l1_dist = functools.partial(utils.math.minkowski_distance, p=1)

model = (
    preprocessing.StandardScaler() |
    neighbors.KNNClassifier(
        engine=neighbors.SWINN(
            dist_func=l1_dist,
            seed=42
        )
    )
)
# %%
metric = metrics.base.Metrics
# %%
metric.get()
# %%
metric_proba = metrics.CrossEntropy()
metric = metrics.Accuracy()
metric_proba.requires_labels
# %%
issubclass(metrics.MAE(), )
# %%
CrossEntropy = []
Accuracy = []
for x, y in dataset:
    y_pred_proba = model.predict_proba_one(x)
    y_pred = model.predict_one(x)
    model.learn_one(x, y)
    metric_proba.update(y, y_pred_proba)
    metric.update(y, y_pred)
    CrossEntropy.append(metric_proba.get())
    Accuracy.append(metric.get())


# %%
CrossEntropy
# %%
Accuracy

# %%
metric_proba.requires_labels
