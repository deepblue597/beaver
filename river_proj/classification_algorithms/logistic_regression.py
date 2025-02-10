# %%

from river_proj import datasets
from river_proj import evaluate
from river_proj import linear_model
from river_proj import metrics
from river_proj import optim
from river_proj import preprocessing

datasets = [datasets.Phishing(), datasets.CreditCard()]


optimizers = [optim.Adam(lr=0.01, beta_1=0.7, beta_2=0.9), optim.SGD(.02)]

model = (
    preprocessing.StandardScaler() |
    linear_model.LogisticRegression(optimizer=optimizers[0])
)

metric = metrics.Accuracy()

evaluate.progressive_val_score(datasets[1], model, metric)

# %%
model

# %%
