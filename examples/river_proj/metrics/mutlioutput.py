# %%
from river import metrics

y_true = [
    {0: False, 1: True, 2: True},
    {0: True, 1: True, 2: False},
    {0: True, 1: True, 2: False},
]

y_pred = [
    {0: True, 1: True, 2: True},
    {0: True, 1: False, 2: False},
    {0: True, 1: True, 2: False},
]

metric = metrics.multioutput.ExactMatch()
for yt, yp in zip(y_true, y_pred):
    metric.update(yt, yp)

metric
# %%
# %%
cm = metrics.multioutput.MultiLabelConfusionMatrix()

for yt, yp in zip(y_true, y_pred):
    cm.update(yt, yp)

cm


# %%
sample_jaccard = metrics.multioutput.MacroAverage(metrics.Jaccard())

for yt, yp in zip(y_true, y_pred):
    sample_jaccard.update(yt, yp)

sample_jaccard
# %%
