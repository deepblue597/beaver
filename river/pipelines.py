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