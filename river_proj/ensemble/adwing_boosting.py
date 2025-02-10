# %%
from river_proj import datasets
from river_proj import ensemble
from river_proj import evaluate
from river_proj import linear_model
from river_proj import metrics
from river_proj import preprocessing
from river_proj import tree


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
