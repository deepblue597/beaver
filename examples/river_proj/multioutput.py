#%% 
from river import feature_selection
from river import linear_model
from river import metrics
from river import multioutput
from river import preprocessing
from river import stream
from sklearn import datasets

dataset = stream.iter_sklearn_dataset(
    dataset=datasets.fetch_openml('yeast', version=4, parser='auto', as_frame=False),
    shuffle=True,
    seed=42
)

model = feature_selection.VarianceThreshold(threshold=0.01)
model |= preprocessing.StandardScaler()
model |= multioutput.ClassifierChain(
    model=linear_model.LogisticRegression(),
    order=list(range(14))
)

metric = metrics.multioutput.MicroAverage(metrics.Jaccard())

for x, y in dataset:
    # Convert y values to booleans
    y = {i: yi == 'TRUE' for i, yi in y.items()}
    y_pred = model.predict_one(x)
    metric.update(y, y_pred)
    model.learn_one(x, y)

metric

#%%
from river import feature_selection
from river import linear_model
from river import metrics
from river import multioutput
from river import preprocessing
from river import stream
from sklearn import datasets

dataset = stream.iter_sklearn_dataset(
    dataset=datasets.fetch_openml('yeast', version=4, parser='auto', as_frame=False),
    shuffle=True,
    seed=42
)

model = feature_selection.VarianceThreshold(threshold=0.01)
model |= preprocessing.StandardScaler()
model |= multioutput.ClassifierChain(
    model=linear_model.LogisticRegression(),
    order=list(range(14))
)

metric = metrics.multioutput.MicroAverage(metrics.Jaccard())

for x, y in dataset:
    # Convert y values to booleans
    #print(y)
    y = {i: yi == 'TRUE' for i, yi in y.items()}
    print(y)
    y_pred = model.predict_one(x)
    metric.update(y, y_pred)
    model.learn_one(x, y)

metric
# %%
list(range(14))
# %%
from river import evaluate
from river import linear_model
from river import metrics
from river import multioutput
from river import preprocessing
from river import stream

from sklearn import datasets

dataset = stream.iter_sklearn_dataset(
    dataset=datasets.load_linnerud(),
    shuffle=True,
    seed=42
)

model = multioutput.RegressorChain(
    model=(
        preprocessing.StandardScaler() |
        linear_model.LinearRegression(intercept_lr=0.3)
    ),
    order=[0, 1, 2]
)

metric = metrics.multioutput.MicroAverage(metrics.MAE())

evaluate.progressive_val_score(dataset, model, metric)
# %%
from river import linear_model
from river import metrics
from river import multioutput
from river.datasets import synth

dataset = synth.Logical(seed=42, n_tiles=100)

model = multioutput.ProbabilisticClassifierChain(
    model=linear_model.LogisticRegression()
)

metric = metrics.multioutput.MicroAverage(metrics.Jaccard())

for x, y in dataset:
   y_pred = model.predict_one(x)
   #print(y_pred)
   if y_pred is not None:
    y_pred = {k: y_pred.get(k, 0) for k in y}
    print(y_pred)
    metric.update(y, y_pred)
   model.learn_one(x, y)

metric
# %%
from river import feature_selection
from river import linear_model
from river import metrics
from river import multioutput
from river import preprocessing
from river.datasets import synth

dataset = synth.Logical(seed=42, n_tiles=100)

model = multioutput.MonteCarloClassifierChain(
    model=linear_model.LogisticRegression(),
    m=10,
    seed=42
)

metric = metrics.multioutput.MicroAverage(metrics.Jaccard())

for x, y in dataset:
   y_pred = model.predict_one(x)
   y_pred = {k: y_pred.get(k, 0) for k in y}
   metric.update(y, y_pred)
   model.learn_one(x, y)

metric
# %%
from river import forest
from river import metrics
from river import multioutput
from river.datasets import synth

dataset = synth.Logical(seed=42, n_tiles=100)

model = multioutput.MultiClassEncoder(
    model=forest.ARFClassifier(seed=7)
)

#%%

dataset
#%%

metric = metrics.multioutput.MicroAverage(metrics.Jaccard())

for x, y in dataset:
   y_pred = model.predict_one(x)
   #print(y_pred)
   y_pred = {k: y_pred.get(k, 0) for k in y}
   #print(y_pred)
   metric.update(y, y_pred)
   model.learn_one(x, y)

metric
# %%
