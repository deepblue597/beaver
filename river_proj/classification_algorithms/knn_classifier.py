# %%
import functools
from river import datasets
from river import evaluate
from river import metrics
from river import neighbors
from river import preprocessing
from river import utils

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
