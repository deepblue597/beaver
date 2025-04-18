# %%
from river import metrics
from river import tree
from river import datasets

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
from river import datasets
from river import evaluate
from river import linear_model
from river import metrics
from river import multiclass
from river import preprocessing

dataset = datasets.ImageSegments()

scaler = preprocessing.StandardScaler()
ovo = multiclass.OneVsOneClassifier(linear_model.LogisticRegression())
model = scaler | ovo

metric = metrics.MacroF1()

evaluate.progressive_val_score(dataset, model, metric)
#%% 
from river import datasets
from river import evaluate
from river import linear_model
from river import metrics
from river import multiclass
from river import preprocessing

dataset = datasets.ImageSegments()

scaler = preprocessing.StandardScaler()
ooc = multiclass.OutputCodeClassifier(
    classifier=linear_model.LogisticRegression(),
    code_size=10,
    coding_method='random',
    seed=1
)
model = scaler | ooc

metric = metrics.MacroF1()

evaluate.progressive_val_score(dataset, model, metric)
# %%
dataset = datasets.ImageSegments()

scaler = preprocessing.StandardScaler()
ovo = multiclass.OneVsOneClassifier(linear_model.LogisticRegression())
model = scaler | ovo

metric = metrics.MacroF1()

evaluate.progressive_val_score(dataset, model, metric)
    
# %%
model[1].classifiers
# %%
