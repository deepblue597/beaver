# %%
from river.datasets import synth

# dataset = synth.Agrawal(
#     classification_function=0,
#     seed=42
# )

# dataset

# %%
from river.datasets import synth
from river import evaluate
from river import metrics
from river import tree

gen = synth.Agrawal(classification_function=0, seed=42)
dataset = iter(gen.take(1000))

model = tree.HoeffdingTreeClassifier(
    grace_period=100,
    delta=1e-1,
    nominal_attributes=['elevel', 'car', 'zipcode']
)

metric = metrics.Accuracy()

evaluate.progressive_val_score(dataset, model, metric)

# %%
