#%%
import random
from river import drift

rng = random.Random(12345)
adwin = drift.ADWIN()

data_stream = rng.choices([0, 1], k=1000) + rng.choices(range(4, 8), k=1000)

for i, val in enumerate(data_stream):
    y = adwin.update(val)
    print(y)
    if adwin.drift_detected:
        print(f"Change detected at index {i}, input value: {val}")
# %%
from river import linear_model

alma = linear_model.ALMAClassifier(
)
if hasattr(alma , 'learn_one' ):
    print('hi')
else : 
    print('oh nooo')
# %%
from river import datasets
from river import ensemble
from river import evaluate
from river import metrics
from river import tree

dataset = datasets.Phishing()

metric = metrics.LogLoss()

model = ensemble.AdaBoostClassifier(
    model=(
        tree.HoeffdingTreeClassifier(
            split_criterion='gini',
            delta=1e-5,
            grace_period=2000
        )
    ),
    n_models=5,
    seed=42
)

for i, (x, y) in enumerate(dataset):
    y_pred = model.predict_proba_one(x)
    model.learn_one(x, y)
    metric.update(y, y_pred)
    if i % 100 == 0:
        print(y_pred)
        print(f"Step {i}, LogLoss: {metric.get()}")
# %%
