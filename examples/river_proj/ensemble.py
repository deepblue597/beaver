# %%
from river import preprocessing as pp
from river import linear_model as lm
from river import compose
from river import neighbors
from river import stream
from river import drift
from river import tree
from river import datasets
from river import ensemble
from river import evaluate
from river import linear_model
from river import metrics
from river import optim
from river import preprocessing

dataset = datasets.Phishing()

model = ensemble.ADWINBaggingClassifier(
    model=(
        preprocessing.StandardScaler() |
        linear_model.LogisticRegression()
    ),
    n_models=3,
    seed=42
)

metric = metrics.F1()

evaluate.progressive_val_score(dataset, model, metric)

# %%

dataset = datasets.Phishing()

model = ensemble.BaggingClassifier(
    model=(
        preprocessing.StandardScaler() |
        linear_model.LogisticRegression()
    ),
    n_models=3,
    seed=42
)

metric = metrics.F1()

# evaluate.progressive_val_score(dataset, model, metric)
# %%
model.models
# %%
model.n_models
# %%
for x, y in dataset:
    model.learn_one(x, y)
    y_pred = model.predict_one(x)
    print(f"Y true: {y}, Predicted: {y_pred}")


# %%

model._supervised
# %%

dataset = datasets.TrumpApproval()

model = preprocessing.StandardScaler()
model |= ensemble.BaggingRegressor(
    model=linear_model.LinearRegression(intercept_lr=0.1),
    n_models=3,
    seed=42
)

metric = metrics.MAE()

# %%
for x, y in dataset:
    model.learn_one(x, y)
    y_pred = model.predict_one(x)
    metric.update(y, y_pred)
    print(f"MAE: {metric}")
    print(f"Y true: {y}, Predicted: {y_pred}")
# %%
dataset = datasets.Phishing()

model = ensemble.ADWINBaggingClassifier(
    model=(
        preprocessing.StandardScaler() |
        linear_model.LogisticRegression()
    ),
    n_models=3,
    seed=42
)

metric = metrics.F1()

evaluate.progressive_val_score(dataset, model, metric)
# %%
model._drift_detectors
# %%
for x, y in dataset:
    model.learn_one(x, y)
    y_pred = model.predict_one(x)
    metric.update(y, y_pred)
    print(f"F1: {metric}")
    print(f"Y true: {y}, Predicted: {y_pred}")

# %%

dataset = datasets.Phishing()

model = ensemble.LeveragingBaggingClassifier(
    model=(
        preprocessing.StandardScaler() |
        linear_model.LogisticRegression()
    ),
    n_models=3,
    seed=42
)

metric = metrics.F1()

evaluate.progressive_val_score(dataset, model, metric)
# %%
model.bagging_methods
# %%

dataset = datasets.Phishing()

metric = metrics.LogLoss()

model = ensemble.AdaBoostClassifier(
    model=(
        tree.HoeffdingTreeClassifier(
            split_criterion='gini',
            delta=1e-5,
            grace_period=2000
        )
    ),
    n_models=5,
    seed=42
)

evaluate.progressive_val_score(dataset, model, metric)
# %%
model.models
# %%
model._unit_test_params()
# %%

dataset = datasets.Phishing()
model = ensemble.ADWINBoostingClassifier(
    model=(
        preprocessing.StandardScaler() |
        linear_model.LogisticRegression()
    ),
    n_models=3,
    seed=42
)
metric = metrics.F1()

evaluate.progressive_val_score(dataset, model, metric)
# %%

dataset = datasets.Elec2().take(3000)

model = ensemble.BOLEClassifier(
    model=drift.DriftRetrainingClassifier(
        model=tree.HoeffdingTreeClassifier(),
        drift_detector=drift.binary.DDM()
    ),
    n_models=10,
    seed=42
)

metric = metrics.Accuracy()

evaluate.progressive_val_score(dataset, model, metric)
# %%
model._wrapped_model
# %%

optimizers = [
    optim.SGD(0.01),
    optim.RMSProp(),
    optim.AdaGrad()
]

for optimizer in optimizers:

    dataset = datasets.TrumpApproval()
    metric = metrics.MAE()
    model = (
        preprocessing.StandardScaler() |
        linear_model.LinearRegression(
            optimizer=optimizer,
            intercept_lr=.1
        )
    )

    print(optimizer, evaluate.progressive_val_score(dataset, model, metric))
# %%
dataset = datasets.TrumpApproval()
metric = metrics.MAE()

model = (
    preprocessing.StandardScaler() |
    ensemble.EWARegressor(
        [
            linear_model.LinearRegression(optimizer=o, intercept_lr=.1)
            for o in optimizers
        ],
        learning_rate=0.005
    )
)

evaluate.progressive_val_score(dataset, model, metric)
# %%
metric = metrics.MAE()
model = (
    preprocessing.StandardScaler() |  # Normalize the features
    ensemble.EWARegressor(
        models=[
            linear_model.LinearRegression(intercept_lr=0.1),
            linear_model.BayesianLinearRegression(),
            linear_model.PARegressor(
                C=0.01,
                mode=2,
                eps=0.1,
                learn_intercept=False
            )
        ],
        learning_rate=0.1
    )
)

# Evaluate the model
evaluate.progressive_val_score(dataset, model, metric)
# %%
for x, y in dataset:
    model.learn_one(x, y)
    y_pred = model.predict_one(x)
    metric.update(y, y_pred)
    print(metric)
    print(f"Y true: {y}, Predicted: {y_pred}")
# %%

dataset = datasets.Phishing()

model = pp.StandardScaler() | ensemble.StackingClassifier(
    [
        lm.LogisticRegression(),
        linear_model.LogisticRegression(optimizer=optim.SGD(.1)),
        lm.PAClassifier(mode=2, C=0.01),
        tree.ExtremelyFastDecisionTreeClassifier(
            grace_period=100,
            delta=1e-5,
            min_samples_reevaluate=100
        )
    ],
    meta_classifier=lm.LogisticRegression()
)


metric = metrics.F1()

evaluate.progressive_val_score(dataset, model, metric)
# %%
model[1].models
# %%
from river import ensemble
from river import evaluate
from river import metrics
from river.datasets import synth
from river import tree

dataset = synth.ConceptDriftStream(
    seed=42,
    position=500,
    width=50
).take(1000)

base_model = tree.HoeffdingTreeClassifier(
    grace_period=50, delta=0.01,
    nominal_attributes=['age', 'car', 'zipcode']
)
model = ensemble.SRPClassifier(
    model=base_model, n_models=3, seed=42,
)

metric = metrics.Accuracy()

evaluate.progressive_val_score(dataset, model, metric)
# %%
model
# %%
model.models
# %%
from river import ensemble
from river import evaluate
from river import metrics
from river.datasets import synth
from river import tree

dataset = synth.FriedmanDrift(
    drift_type='gsg',
    position=(350, 750),
    transition_window=200,
    seed=42
).take(1000)

base_model = tree.HoeffdingTreeRegressor(grace_period=50)
model = ensemble.SRPRegressor(
    model=base_model,
    training_method="patches",
    n_models=3,
    seed=42
)

metric = metrics.R2()

evaluate.progressive_val_score(dataset, model, metric)
# %%
from river import datasets
from river import ensemble
from river import evaluate
from river import linear_model
from river import metrics
from river import naive_bayes
from river import preprocessing
from river import tree

dataset = datasets.Phishing()

model = (
    preprocessing.StandardScaler() |
    ensemble.VotingClassifier([
        linear_model.LogisticRegression(),
        tree.HoeffdingTreeClassifier(),
        naive_bayes.GaussianNB()
    ])
)

metric = metrics.F1()

evaluate.progressive_val_score(dataset, model, metric)
# %%
