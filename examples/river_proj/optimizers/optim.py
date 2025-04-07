# %%

from river import datasets
from river import evaluate
from river import linear_model
from river import metrics
from river import optim
from river import preprocessing

dataset = datasets.Phishing()
# optimizer = optim.AMSGrad(
#    lr=optim.schedulers.Optimal(loss=optim.losses.Hinge()))

# optimizer = optim.Momentum()
optimizer = optim.SGD()
model = (
    preprocessing.StandardScaler() |
    linear_model.LogisticRegression(optimizer)
)
metric = metrics.Accuracy()

evaluate.progressive_val_score(dataset, model, metric)
# %%

dataset = datasets.Phishing()
optimizer = optim.Averager(optim.SGD(0.01), 23)
model = (
    preprocessing.StandardScaler() |
    linear_model.LogisticRegression(optimizer)
)
metric = metrics.F1()

evaluate.progressive_val_score(dataset, model, metric)
# %%
optimizer = optim.AMSGrad(lr=optim.schedulers.Optimal(
    loss=optim.losses.EpsilonInsensitiveHinge()))
model = (
    preprocessing.StandardScaler() |
    linear_model.LinearRegression(intercept_lr=.1, optimizer=optimizer)
)
metric = metrics.MAE()

# Evaluate the model
evaluate.progressive_val_score(dataset, model, metric)

# Reset the dataset and lists for plotting
dataset = datasets.TrumpApproval()

evaluate.progressive_val_score(dataset, model, metric)

# %%
