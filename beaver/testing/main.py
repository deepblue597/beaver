# %%

from pipeline import Pipeline
from river import linear_model
from river import drift
from river import metrics
from river import optim
from river import compose
from river import preprocessing
from quixstreams.kafka import ConnectionConfig
from quixstreams.models import TopicConfig
from quixstreams import Application
import sys


# %%

# Define metrics
testMetric1 = metrics.AdjustedRand()
testMetric2 = metrics.CohenKappa()

# Define optimizers
optim1 = optim.AdaDelta()

preproc1 = preprocessing.AdaptiveStandardScaler()
preproc2 = preprocessing.FeatureHasher(
    n_features=10,
    seed=42)
testAlgo = drift.binary.DDM()

preprocessor_testData = preproc1 | preproc2
testPipeline_pipeline = preprocessor_testData | testAlgo
testPipeline_metrics = [testMetric1, testMetric2]

# %%
testPipeline = Pipeline(model=testPipeline_pipeline, metrics_list=testPipeline_metrics,
                        name="testPipeline", output_topic="tester_topic")

# %%

print(testPipeline.metrics)
# %%
testPipeline.metrics
# %%
print(testPipeline)
# %%
