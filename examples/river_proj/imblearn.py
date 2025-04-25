# %%

from river import multiclass
from river import optim
from river import linear_model
from river import datasets
from river import evaluate
from river import imblearn
from river import metrics
from river import preprocessing
from river import rules

model = (
    preprocessing.StandardScaler() |
    imblearn.ChebyshevUnderSampler(
        regressor=rules.AMRules(
            n_min=50, delta=0.01,
        ),
        seed=42
    )
)

evaluate.progressive_val_score(
    datasets.TrumpApproval(),
    model,
    metrics.MAE(),
    print_every=500
)
# %%

model = (
    preprocessing.StandardScaler() |
    imblearn.ChebyshevOverSampler(
        regressor=rules.AMRules(
            n_min=50, delta=0.01
        )
    )
)

evaluate.progressive_val_score(
    datasets.TrumpApproval(),
    model,
    metrics.MAE(),
    print_every=500
)
# %%

model = (
    preprocessing.StandardScaler() |
    imblearn.HardSamplingRegressor(
        regressor=linear_model.LinearRegression(),
        p=.2,
        size=30,
        seed=42,
    )
)
model._supervised
# %%
evaluate.progressive_val_score(
    datasets.TrumpApproval(),
    model,
    metrics.MAE(),
    print_every=500
)
# %%

model = (
    preprocessing.StandardScaler() |
    imblearn.HardSamplingClassifier(
        classifier=linear_model.LogisticRegression(),
        p=0.1,
        size=40,
        seed=42,
    )
)

evaluate.progressive_val_score(
    dataset=datasets.Phishing(),
    model=model,
    metric=metrics.ROCAUC(),
    print_every=500,
)
# %%

model = imblearn.RandomUnderSampler(
    (
        preprocessing.StandardScaler() |
        linear_model.LogisticRegression()
    ),
    desired_dist={False: 0.4, True: 0.6},
    seed=42
)

dataset = datasets.CreditCard().take(3000)

metric = metrics.LogLoss()

evaluate.progressive_val_score(dataset, model, metric)
# %%

model = imblearn.RandomOverSampler(
    (
        preprocessing.StandardScaler() |
        linear_model.LogisticRegression()
    ),
    desired_dist={False: 0.4, True: 0.6},
    seed=42
)

dataset = datasets.CreditCard().take(3000)

metric = metrics.LogLoss()

evaluate.progressive_val_score(dataset, model, metric)
# %%

dataset = datasets.ImageSegments()

scaler = preprocessing.StandardScaler()
ovr = multiclass.OneVsRestClassifier(linear_model.LogisticRegression())
model = scaler | ovr

metric = metrics.MacroF1()

evaluate.progressive_val_score(dataset, model, metric)
# %%
