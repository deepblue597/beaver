# %%
import functools
from river_proj import datasets
from river_proj import evaluate
from river_proj import metrics
from river_proj import neighbors
from river_proj import preprocessing
from river_proj import utils

dataset = datasets.Phishing()


l1_dist = functools.partial(utils.math.minkowski_distance, p=1)

model = (
    preprocessing.StandardScaler() |
    neighbors.KNNClassifier(
        engine=neighbors.SWINN(
            dist_func=l1_dist,
            seed=42
        )
    )
)

evaluate.progressive_val_score(dataset, model, metrics.Accuracy())

# %%
