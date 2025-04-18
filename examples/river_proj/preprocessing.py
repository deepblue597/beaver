# %%
from river import metrics
from river import linear_model
from river import evaluate
from river import datasets
import string
import random
from pprint import pprint
from river import feature_extraction
from river import compose
from river import stats
from river import preprocessing
import river


hasher = river.preprocessing.FeatureHasher(n_features=10, seed=42)

X = [
    {'dog': 1, 'cat': 1, 'elephant': 4},
    {'dog': 3, 'run': 5}
]
for x in X:
    print(hasher.transform_one(x))
# %%

imputer = preprocessing.PreviousImputer()

imputer.learn_one({'x': 1, 'y': 2})
imputer.transform_one({'y': None})
# %%

X = [
    {'temperature': 1},
    {'temperature': 8},
    {'temperature': 3},
    {'temperature': None},
    {'temperature': 4}
]

imp = preprocessing.StatImputer(('temperature', stats.Mean()))

for x in X:
    imp.learn_one(x)
    print(imp.transform_one(x))
# %%

X = [
    {'weather': 'sunny'},
    {'weather': 'rainy'},
    {'weather': 'sunny'},
    {'weather': None},
    {'weather': 'rainy'},
    {'weather': 'rainy'},
    {'weather': None}
]

imp = preprocessing.StatImputer(('weather', 'missing'))

for x in X:
    imp.learn_one(x)
    print(imp.transform_one(x))
    {'weather': 'sunny'}
    {'weather': 'rainy'}
    {'weather': 'sunny'}
    {'weather': 'missing'}
    {'weather': 'rainy'}
    {'weather': 'rainy'}
    {'weather': 'missing'}
# %%

X = [
    'weather cold',
    'weather hot dry',
    'weather cold rainy',
    'weather hot',
    'weather cold humid',
]

lda = compose.Pipeline(
    feature_extraction.BagOfWords(),
    preprocessing.LDA(
        n_components=2,
        number_of_documents=60,
        seed=42
    )
)

for x in X:
    lda.learn_one(x)
    topics = lda.transform_one(x)
    print(topics)
# %%

random.seed(42)
alphabet = list(string.ascii_lowercase)
X = [
    {
        'c1': random.choice(alphabet),
        'c2': random.choice(alphabet),
    }
    for _ in range(4)
]
pprint(X)
# %%

oh = preprocessing.OneHotEncoder()
for x in X[:2]:
    oh.learn_one(x)
    print(oh.transform_one(x))
# %%

# Create a one-hot encoder
oh = preprocessing.OneHotEncoder()

# Input data
X = [
    {'color': 'red', 'size': 'M'},
    {'color': 'blue', 'size': 'L'},
    {'color': 'green', 'size': 'S'}
]

# Learn and transform each instance
for x in X:
    oh.learn_one(x)
    print(oh.transform_one(x))
# %%
oh = preprocessing.OneHotEncoder(drop_zeros=True)

for x in X:
    oh.learn_one(x)
    print(oh.transform_one(x))
# %%

X = [
    {"country": "France", "place": "Taco Bell"},
    {"country": None, "place": None},
    {"country": "Sweden", "place": "Burger King"},
    {"country": "France", "place": "Burger King"},
    {"country": "Russia", "place": "Starbucks"},
    {"country": "Russia", "place": "Starbucks"},
    {"country": "Sweden", "place": "Taco Bell"},
    {"country": None, "place": None},
]

encoder = preprocessing.OrdinalEncoder()
for x in X:
    print(encoder.transform_one(x))
    encoder.learn_one(x)
# %%

dataset = datasets.TrumpApproval()
model = preprocessing.GaussianRandomProjector(
    n_components=5,
    seed=42
)

for x, y in dataset:
    x = model.transform_one(x)
    print(x)
    break
# %%

dataset = datasets.TrumpApproval()
model = (
    preprocessing.StandardScaler() |
    preprocessing.TargetStandardScaler(
        regressor=linear_model.LinearRegression(intercept_lr=0.15)
    )
)
metric = metrics.MSE()

evaluate.progressive_val_score(dataset, model, metric)
# %%

# Create a Binarizer instance with a threshold of 0.0
binarizer = preprocessing.Binarizer(threshold=0.0, dtype=bool)

# Input data
X = [
    {'feature1': -1.5, 'feature2': 2.3},
    {'feature1': 0.0, 'feature2': -0.7},
    {'feature1': 1.2, 'feature2': 0.0},
    {'feature1': -0.3, 'feature2': 0.8}
]

# Transform each instance
for x in X:
    transformed_x = binarizer.transform_one(x)
    print(f"Original: {x}, Transformed: {transformed_x}")
# %%

random.seed(42)
X = [{'x': random.uniform(8, 12), 'y': random.uniform(8, 12)}
     for _ in range(6)]
for x in X:
    print(x)
# %%
scaler = preprocessing.StandardScaler()

for x in X:
    scaler.learn_one(x)
    print(scaler.transform_one(x))
# %%

random.seed(42)
X = [{'x': random.uniform(8, 12)} for _ in range(5)]
for x in X:
    print(x)
# %%
scaler = preprocessing.MinMaxScaler()

for x in X:
    scaler.learn_one(x)
    print(scaler.transform_one(x))
# %%

random.seed(42)
X = [{'x': random.uniform(8, 12)} for _ in range(5)]
for x in X:
    print(x)
# %%
scaler = preprocessing.MaxAbsScaler()
scaled = []
for x in X:
    scaler.learn_one(x)
    print(scaler.transform_one(x))


scaler.abs_max

# %%
scaler = preprocessing.RobustScaler()

for x in X:
    scaler.learn_one(x)
    print(scaler.transform_one(x))

# %%
