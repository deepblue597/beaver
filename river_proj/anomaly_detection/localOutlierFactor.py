# %%
import pandas as pd
from river_proj import anomaly
from river_proj import datasets

cc_df = pd.DataFrame(datasets.CreditCard())

lof = anomaly.LocalOutlierFactor(n_neighbors=20)

for x, _ in datasets.CreditCard().take(500):
    lof.learn_one(x)

lof.learn_many(cc_df[501:1000])

# %% i dont understand why 406 is 0 while it is an outlier based on the db
scores = []
for x in cc_df[0][404:408]:
    scores.append(lof.score_one(x))

[round(score, 3) for score in scores]

# %%
cc_df[0][406]
# %%
datasets.CreditCard()
# %%
X = [0.5, 0.45, 0.43, 0.44, 0.445, 0.45, 0.0]
lof = anomaly.LocalOutlierFactor()

for x in X[:3]:
    lof.learn_one({'x': x})  # Warming up

for x in X:
    features = {'x': x}
    print(
        f'Anomaly score for x={x:.3f}: {lof.score_one(features):.3f}')
    lof.learn_one(features)
# %%
