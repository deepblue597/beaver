# %%
from river import utils
import functools
from river.neighbors.base import BaseNN
from river import datasets
from river import evaluate
from river import metrics
from river import neighbors
from river import preprocessing

dataset = datasets.TrumpApproval()

model = neighbors.KNNRegressor()
evaluate.progressive_val_score(dataset, model, metrics.RMSE())
# %%
model._unit_test_params()
# %%
model._supervised
# %%

# Get all direct subclasses of BaseNN
subclasses = BaseNN.__subclasses__()
print(subclasses)
# %%

dataset = datasets.Phishing()
l1_dist = functools.partial(utils.math.minkowski_distance, p=1)

model = (
    preprocessing.StandardScaler() |
    neighbors.KNNClassifier(
        engine=neighbors.LazySearch(
            window_size=80
        )
    )
)

evaluate.progressive_val_score(dataset, model, metrics.Accuracy())

# %%
