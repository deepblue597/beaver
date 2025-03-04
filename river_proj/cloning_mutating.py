# %%
from river.utils.rolling import Rollable
import inspect
import importlib
from river_proj import datasets, linear_model, optim, preprocessing

model = (
    preprocessing.StandardScaler() |
    linear_model.LinearRegression(
        optimizer=optim.SGD(3e-2)
    )
)

for x, y in datasets.TrumpApproval():
    model.predict_one(x)
    model.learn_one(x, y)

model[-1].weights
# %%
clone = model.clone()
clone[-1].weights
# %%
# You may also specify parameters you want changed.
# For instance, let's say we want to clone the model,
# but we want to change the optimizer:

clone = model.clone({"LinearRegression": {"optimizer": optim.Adam()}})
clone[-1].optimizer
# %%
'''
Mutating attributes¶
Cloning a model can be useful, but the fact that it essentially 
resets the model may not be desired. Instead, 
you might want to change a attribute while preserving the model's state. 
For example, let's change the l2 attribute, and the optimizer's lr attribute.
'''

model.mutate({
    "LinearRegression": {
        "l2": 0.1,
        "optimizer": {
            "lr": optim.schedulers.Constant(25e-3)
        }
    }
})

print(repr(model))
# %%
model[-1].weights

# %%


for submodule in importlib.import_module("river.api").__all__:
    for _, obj in inspect.getmembers(
        importlib.import_module(
            f"river.{submodule}"), lambda x: isinstance(x, Rollable)
    ):
        print(f'{submodule}.{obj.__name__}')
# %%
