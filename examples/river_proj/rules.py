#%%

from river import datasets
from river import drift
from river import evaluate
from river import metrics
from river import preprocessing
from river import rules

dataset = datasets.TrumpApproval()

model = (
    preprocessing.StandardScaler() |
    rules.AMRules(
        delta=0.01,
        n_min=50,
        drift_detector=drift.ADWIN()
    )
)

metric = metrics.MAE()

evaluate.progressive_val_score(dataset, model, metric)
# %%
