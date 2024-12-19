# %%
from river import preprocessing
from river import compose
from river import metrics
from river import linear_model
from river import datasets
from river import evaluate
# %%
dataset = datasets.Phishing()
dataset

# %%
for x, y in dataset:
    pass

# %%
x, y = next(iter(dataset))
x
# %%
y
# %%

model = linear_model.LogisticRegression()
# Predict probability of one item ( 50% in the beginning )
model.predict_proba_one(x)
# %%
# Learn from the data ( one example at a time)
model.learn_one(x, y)
# %%
# Gives the probababilities of the classes
model.predict_proba_one(x)
# %%
# sets True or False
model.predict_one(x)
# %%

model = linear_model.LogisticRegression()

metric = metrics.ROCAUC()

for x, y in dataset:
    y_pred = model.predict_proba_one(x)
    model.learn_one(x, y)
    metric.update(y, y_pred)

metric
# %%

model = compose.Pipeline(
    preprocessing.StandardScaler(),
    linear_model.LogisticRegression()
)

model
# %%
metric = metrics.ROCAUC()
evaluate.progressive_val_score(dataset, model, metric)
# %%
