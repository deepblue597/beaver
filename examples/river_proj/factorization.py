#%%

from river import facto

dataset = (
    ({'user': 'Alice', 'item': 'Superman', 'time': .12}, 8),
    ({'user': 'Alice', 'item': 'Terminator', 'time': .13}, 9),
    ({'user': 'Alice', 'item': 'Star Wars', 'time': .14}, 8),
    ({'user': 'Alice', 'item': 'Notting Hill', 'time': .15}, 2),
    ({'user': 'Alice', 'item': 'Harry Potter ', 'time': .16}, 5),
    ({'user': 'Bob', 'item': 'Superman', 'time': .13}, 8),
    ({'user': 'Bob', 'item': 'Terminator', 'time': .12}, 9),
    ({'user': 'Bob', 'item': 'Star Wars', 'time': .16}, 8),
    ({'user': 'Bob', 'item': 'Notting Hill', 'time': .10}, 2)
)

model = facto.FFMRegressor(
    n_factors=10,
    intercept=5,
    seed=42,
)

for x, y in dataset:
    model.learn_one(x, y)

model.predict_one({'user': 'Bob', 'item': 'Harry Potter', 'time': .14})
# %%
model.weights
# %%
model.latents
# %%
report = model.debug_one({'user': 'Bob', 'item': 'Harry Potter', 'time': .14})

print(report)
# %%
from river import facto

dataset = (
    ({'user': 'Alice', 'item': 'Superman', 'time': .12}, True),
    ({'user': 'Alice', 'item': 'Terminator', 'time': .13}, True),
    ({'user': 'Alice', 'item': 'Star Wars', 'time': .14}, True),
    ({'user': 'Alice', 'item': 'Notting Hill', 'time': .15}, False),
    ({'user': 'Alice', 'item': 'Harry Potter ', 'time': .16}, True),
    ({'user': 'Bob', 'item': 'Superman', 'time': .13}, True),
    ({'user': 'Bob', 'item': 'Terminator', 'time': .12}, True),
    ({'user': 'Bob', 'item': 'Star Wars', 'time': .16}, True),
    ({'user': 'Bob', 'item': 'Notting Hill', 'time': .10}, False)
)

model = facto.FFMClassifier(
    n_factors=10,
    intercept=.5,
    seed=42,
)

for x, y in dataset:
    model.learn_one(x, y)

model.predict_one({'user': 'Bob', 'item': 'Harry Potter', 'time': .14})
# %%
model._multiclass
# %%
from river import facto

dataset = (
    ({'user': 'Alice', 'item': 'Superman'}, 8),
    ({'user': 'Alice', 'item': 'Terminator'}, 9),
    ({'user': 'Alice', 'item': 'Star Wars'}, 8),
    ({'user': 'Alice', 'item': 'Notting Hill'}, 2),
    ({'user': 'Alice', 'item': 'Harry Potter '}, 5),
    ({'user': 'Bob', 'item': 'Superman'}, 8),
    ({'user': 'Bob', 'item': 'Terminator'}, 9),
    ({'user': 'Bob', 'item': 'Star Wars'}, 8),
    ({'user': 'Bob', 'item': 'Notting Hill'}, 2)
)

model = facto.FMRegressor(
    n_factors=10,
    intercept=5,
    seed=42,
)

for x, y in dataset:
    model.learn_one(x, y)

model.predict_one({'Bob': 1, 'Harry Potter': 1})
# %%
report = model.debug_one({'Bob': 1, 'Harry Potter': 1})

print(report)
# %%
from river import metrics, facto

# Define a dataset
dataset = (
    ({'user': 'Alice', 'item': 'Superman'}, 8),
    ({'user': 'Alice', 'item': 'Terminator'}, 9),
    ({'user': 'Bob', 'item': 'Superman'}, 8),
    ({'user': 'Bob', 'item': 'Notting Hill'}, 2)
)

# Initialize the model and metric
model = facto.FMRegressor(n_factors=10, intercept=5, seed=42)
metric = metrics.MAE()  # Mean Absolute Error

# Train the model and update the metric
for x, y in dataset:
    y_pred = model.predict_one(x)  # Make a prediction
    metric.update(y_true=y, y_pred=y_pred)  # Update the metric
    model.learn_one(x, y)  # Train the model

# Print the final metric
print(f"MAE: {metric.get()}")
# %%
from river import facto

dataset = (
    ({'user': 'Alice', 'item': 'Superman', 'time': .12}, 8),
    ({'user': 'Alice', 'item': 'Terminator', 'time': .13}, 9),
    ({'user': 'Alice', 'item': 'Star Wars', 'time': .14}, 8),
    ({'user': 'Alice', 'item': 'Notting Hill', 'time': .15}, 2),
    ({'user': 'Alice', 'item': 'Harry Potter ', 'time': .16}, 5),
    ({'user': 'Bob', 'item': 'Superman', 'time': .13}, 8),
    ({'user': 'Bob', 'item': 'Terminator', 'time': .12}, 9),
    ({'user': 'Bob', 'item': 'Star Wars', 'time': .16}, 8),
    ({'user': 'Bob', 'item': 'Notting Hill', 'time': .10}, 2)
)

model = facto.HOFMRegressor(
    degree=3,
    n_factors=10,
    intercept=5,
    seed=42,
)

for x, y in dataset:
    model.learn_one(x, y)

model.predict_one({'user': 'Bob', 'item': 'Harry Potter', 'time': .14})
# %%
from river import facto

dataset = (
    ({'user': 'Alice', 'item': 'Superman', 'time': .12}, True),
    ({'user': 'Alice', 'item': 'Terminator', 'time': .13}, True),
    ({'user': 'Alice', 'item': 'Star Wars', 'time': .14}, True),
    ({'user': 'Alice', 'item': 'Notting Hill', 'time': .15}, False),
    ({'user': 'Alice', 'item': 'Harry Potter ', 'time': .16}, True),
    ({'user': 'Bob', 'item': 'Superman', 'time': .13}, True),
    ({'user': 'Bob', 'item': 'Terminator', 'time': .12}, True),
    ({'user': 'Bob', 'item': 'Star Wars', 'time': .16}, True),
    ({'user': 'Bob', 'item': 'Notting Hill', 'time': .10}, False)
)

model = facto.HOFMClassifier(
    degree=3,
    n_factors=10,
    intercept=.5,
    seed=42,
)

for x, y in dataset:
    model.learn_one(x, y)

model.predict_one({'user': 'Bob', 'item': 'Harry Potter', 'time': .14})
# %%
