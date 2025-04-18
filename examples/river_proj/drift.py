# %%
from river import tree
from river import metrics
from river import evaluate
from river import datasets
import random
from river import drift

rng = random.Random(12345)
adwin = drift.ADWIN()

data_stream = rng.choices([0, 1], k=1000) + rng.choices(range(4, 8), k=1000)

for i, val in enumerate(data_stream):
    adwin.update(val)
    print(adwin.n_detections)
    if adwin.drift_detected:
        print(f"Change detected at index {i}, input value: {val}")
# %%
adwin.estimation
# %%
adwin.total
# %%
adwin.width
# %%

dataset = datasets.Elec2().take(3000)

model = drift.DriftRetrainingClassifier(
    model=tree.HoeffdingTreeClassifier(),
    drift_detector=drift.binary.DDM()
)

metric = metrics.Accuracy()

# evaluate.progressive_val_score(dataset, model, metric)
# %%
for x, y in dataset:
    model.learn_one(x, y)
    y_pred = model.predict_one(x)
    if model.drift_detector.drift_detected:
        print(f"Drift detected at {x}")
    if model.drift_detector.warning_detected:
        print(f"Warning detected at {x}")

# %%

rng = random.Random(42)
ddm = drift.binary.DDM()

data_stream = rng.choices([0, 1], k=1000)
data_stream = data_stream + rng.choices([0, 1], k=1000, weights=[0.3, 0.7])

print_warning = True
for i, x in enumerate(data_stream):
    ddm.update(x)
    if ddm.warning_detected and print_warning:
        print(f"Warning detected at index {i}")
        print_warning = False
    if ddm.drift_detected:
        print(f"Change detected at index {i}")
        print_warning = True
# %%

ddm = drift.binary.DDM()

# Simulated binary classification results
data_stream = [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]

for i, x in enumerate(data_stream):
    ddm.update(x)
    if ddm.warning_detected:
        print(f"Warning detected at index {i}")
    if ddm.drift_detected:
        print(f"Drift detected at index {i}")
# %%

rng = random.Random(42)
eddm = drift.binary.EDDM(alpha=0.8, beta=0.75)

data_stream = rng.choices([0, 1], k=1000)
data_stream = data_stream + rng.choices([0, 1], k=1000, weights=[0.3, 0.7])
data_stream
# %%
print_warning = True
for i, x in enumerate(data_stream):
    eddm.update(x)
    if eddm.warning_detected and print_warning:
        print(f"Warning detected at index {i}")
        print_warning = False
    if eddm.drift_detected:
        print(f"Change detected at index {i}")
        print_warning = True
# %%

rng = random.Random(42)
fhddm = drift.binary.FHDDM()
fhddm_s = drift.binary.FHDDM(short_window_size=20)
data_stream = rng.choices([0, 1], k=250)
data_stream = data_stream + rng.choices([0, 1], k=250, weights=[0.9, 0.1])
for i, x in enumerate(data_stream):
    fhddm.update(x)
    fhddm_s.update(x)
    if fhddm.drift_detected or fhddm_s.drift_detected:
        print(f"Change detected at index {i}")
# %%

rng = random.Random(42)
hddm_a = drift.binary.HDDM_A()

data_stream = rng.choices([0, 1], k=1000)
data_stream = data_stream + rng.choices([0, 1], k=1000, weights=[0.3, 0.7])

print_warning = True
for i, x in enumerate(data_stream):
    hddm_a.update(x)
    if hddm_a.warning_detected and print_warning:
        print(f"Warning detected at index {i}")
        print_warning = False
    if hddm_a.drift_detected:
        print(f"Change detected at index {i}")
        print_warning = True
# %%
