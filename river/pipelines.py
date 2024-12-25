"""
The compose.Pipeline contains all the logic for building and applying pipelines. 
A pipeline is essentially a list of estimators that are applied in sequence. 
The only requirement is that the first n - 1 steps be transformers. 
The last step can be a regressor, a classifier, a clusterer, a transformer, etc.

"""
#%% 
from river import compose
from river import linear_model
from river import preprocessing
from river import feature_extraction

"""
A PolynomialExtender is a feature extraction tool that generates polynomial features from the existing features. It creates new features by taking combinations of the original features raised to a power. This can help in capturing non-linear relationships between the features and the target variable.

In the context of the river library, PolynomialExtender is used to extend the feature set by adding polynomial combinations of the existing features.

"""

model = compose.Pipeline(
    preprocessing.StandardScaler(),
    feature_extraction.PolynomialExtender(),
    linear_model.LinearRegression()
)
# %%
model
# %%
from river import datasets

dataset = datasets.TrumpApproval()
x, y = next(iter(dataset))
x, y
# %%

"""
We can predict the target value of a new sample by calling the predict_one method, 
however, by default, predict_one does not update any model parameter, therefore the predictions will be 0 and 
the model parameters will remain the default values (0 for StandardScaler component):
"""

for (x, y) in dataset.take(2):
    print(f"{model.predict_one(x)=:.2f}, {y=:.2f}")
    print(f"{model['StandardScaler'].means = }")
# %%
for (x, y) in dataset.take(2):
    model.learn_one(x, y)

    print(f"{model.predict_one(x)=:.2f}, {y=:.2f}")
    print(f"{model['StandardScaler'].means = }")
# %%
model.transform_one(x)
# %%
"""
In many cases, you might want to connect a step to multiple steps. For instance, you might to extract different kinds of features from a single input. An elegant way to do this is to use a compose.TransformerUnion. Essentially, the latter is a list of transformers who's results will be merged into a single dict when transform_one is called.

As an example let's say that we want to apply a feature_extraction.RBFSampler as well as the feature_extraction.PolynomialExtender. This may be done as so:
"""

model = (
    preprocessing.StandardScaler() |
    (feature_extraction.PolynomialExtender() + feature_extraction.RBFSampler()) |
    linear_model.LinearRegression()
)

model
# %%
# another way of typing the above 
# model = (
#     preprocessing.StandardScaler() |
#     compose.TransformerUnion(
#         feature_extraction.PolynomialExtender(),
#         feature_extraction.RBFSampler()
#     ) |
#     linear_model.LinearRegression()
# )
# %%
""" 
Learning during predict¶
In online machine learning, we can update the unsupervised parts of our model when a sample arrives. We don't really have to wait for the ground truth to arrive in order to update unsupervised estimators that don't depend on it.

In other words, in a pipeline, learn_one updates the supervised parts, whilst predict_one (or predict_proba_one for that matter) can update the unsupervised parts, which often yields better results.

In river, we can achieve this behavior using a dedicated context manager: compose.learn_during_predict.

"""
model = (
    preprocessing.StandardScaler() |
    feature_extraction.PolynomialExtender() |
    linear_model.LinearRegression()
)
# %%
with compose.learn_during_predict():
    for (x, y) in dataset.take(2):

        print(f"{model.predict_one(x)=:.2f}, {y=:.2f}")
        print(f"{model['StandardScaler'].means = }")
# %%
model.predict_one(x), model["LinearRegression"].weights
# %%
from contextlib import nullcontext
from river import metrics

import pandas as pd
# %%
def score_pipeline(learn_during_predict: bool, n_learning_samples: int | None = None) -> float:
    """Scores a pipeline on the TrumpApproval dataset.

    Parameters
    ----------
    learn_during_predict : bool
        Whether or not to learn the unsupervided components during the prediction step.
        If False it will only learn when `learn_one` is explicitly called.
    n_learning_samples : int | None 
        Number of samples used to `learn_one`.

    Return
    ------
    MAE : float
        Mean absolute error of the pipeline on the dataset
    """

    dataset = datasets.TrumpApproval()

    model = (
        preprocessing.StandardScaler() |
        linear_model.LinearRegression()
        )

    metric = metrics.MAE()

    ctx = compose.learn_during_predict if learn_during_predict else nullcontext
    n_learning_samples = n_learning_samples or dataset.n_samples

    with ctx():
        for _idx, (x, y) in enumerate(dataset):
            y_pred = model.predict_one(x)

            metric.update(y, y_pred)

            if _idx < n_learning_samples:
                model.learn_one(x, y)

    return metric.get()
# %%
max_samples = datasets.TrumpApproval().n_samples

results = [
    {
        "learn_during_predict": learn_during_predict,
        "pct_learning_samples": round(100*n_learning_samples/max_samples, 0),
        "mae": score_pipeline(learn_during_predict=learn_during_predict, n_learning_samples=n_learning_samples)
    }
    for learn_during_predict in (True, False)
    for n_learning_samples in range(max_samples, max_samples//10, -(max_samples//10))
]
# %%
(pd.DataFrame(results)
 .pivot(columns="learn_during_predict", index="pct_learning_samples", values="mae")
 .sort_index(ascending=False)
 .style.format_index('{0}%')
)
# %%
