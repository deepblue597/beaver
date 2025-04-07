# %%
import random
from river import drift

rng = random.Random(12345)
adwin = drift.ADWIN()

data_stream = rng.choices([0, 1], k=1000) + rng.choices(range(4, 8), k=1000)

for i, val in enumerate(data_stream):
    adwin.update(val)
    if adwin.drift_detected:
        print(f"Change detected at index {i}, input value: {val}")
# %%
