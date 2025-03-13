# %%
from river import datasets
from river import ensemble
from river import evaluate
from river import linear_model
from river import metrics
from river import preprocessing
from river import tree


dataset = datasets.Phishing()
model = ensemble.ADWINBoostingClassifier(
    model=(
        preprocessing.StandardScaler() |
        tree.HoeffdingTreeClassifier(
            grace_period=100,
            delta=1e-1
        )
    ),
    n_models=3,
    seed=42
)
metric = metrics.F1()

evaluate.progressive_val_score(dataset, model, metric)

# %%
