# %%
from river import evaluate
from river import forest
from river import metrics
from river.datasets import synth

dataset = synth.ConceptDriftStream(
    seed=42,
    position=500,
    width=40
).take(1000)

model = forest.ARFClassifier(seed=8, leaf_prediction="mc")

metric = metrics.Accuracy()

evaluate.progressive_val_score(dataset, model, metric)
# %%
model.n_warnings_detected(), model.n_drifts_detected()
# %%
