# %%
from river import datasets
from river import evaluate
from river import neural_net as nn
from river import optim
from river import preprocessing as pp
from river import metrics

model = (
    pp.StandardScaler() |
    nn.MLPRegressor(
        hidden_dims=(5,),
        activations=(
            nn.activations.ReLU,
            nn.activations.ReLU,
            nn.activations.Identity
        ),
        optimizer=optim.SGD(1e-3),
        seed=42
    )
)

dataset = datasets.TrumpApproval()

metric = metrics.MAE()

for x, y in dataset:
    y_pred = model.predict_one(x)
    model.learn_one(x, y)
    metric.update(y, y_pred)
    print(metric)
# %%
model._supervised
# %%
