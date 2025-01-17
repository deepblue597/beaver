# %%
import matplotlib.pyplot as plt
import datetime as dt

from river import datasets
from river import evaluate
from river import metrics
from river import preprocessing  # we are going to use that later
from river.datasets import synth  # we are going to use some synthetic datasets too
from river import tree
import graphviz
# %%
dataset = datasets.Phishing()
dataset
# %%
# %%time

model = tree.HoeffdingTreeClassifier(grace_period=50)

for x, y in dataset:
    model.learn_one(x, y)

model
# %%
model.summary
# %%
model.to_dataframe().iloc[:5, :5]
# %%
model.draw()
# %%
x, y = next(iter(dataset))  # Let's select the first example in the stream
x, y
# %%
print(model.debug_one(x))
# %%
"""
Some additional hints:

the max_depth parameter is our friend when building HTs that need to be constantly inspected. 
This parameter, which is available for every HT variant, triggers a pre-pruning mechanism 
that stops tree growth when the given depth is reached.
we can also limit the depth when using the draw method.
in the case of tree ensembles, individual trees can be accessed using the [index] operator. 
Then, the same set of inspection tools are available to play with!

"""


def plot_performance(dataset, metric, models):
    metric_name = metric.__class__.__name__

    # To make the generated data reusable
    dataset = list(dataset)
    fig, ax = plt.subplots(figsize=(10, 5), nrows=3, dpi=300)
    for model_name, model in models.items():
        step = []
        error = []
        r_time = []
        memory = []

        for checkpoint in evaluate.iter_progressive_val_score(
            dataset, model, metric, measure_time=True, measure_memory=True, step=100
        ):
            step.append(checkpoint["Step"])
            error.append(checkpoint[metric_name].get())

            # Convert timedelta object into seconds
            r_time.append(checkpoint["Time"].total_seconds())
            # Make sure the memory measurements are in MiB
            raw_memory = checkpoint["Memory"]
            memory.append(raw_memory * 2**-20)

        ax[0].plot(step, error, label=model_name)
        ax[1].plot(step, r_time, label=model_name)
        ax[2].plot(step, memory, label=model_name)

    ax[0].set_ylabel(metric_name)
    ax[1].set_ylabel('Time (seconds)')
    ax[2].set_ylabel('Memory (MiB)')
    ax[2].set_xlabel('Instances')

    ax[0].grid(True)
    ax[1].grid(True)
    ax[2].grid(True)

    ax[0].legend(
        loc='upper center', bbox_to_anchor=(0.5, 1.25),
        ncol=3, fancybox=True, shadow=True
    )
    plt.tight_layout()
    plt.close()

    return fig


# %%
plot_performance(
    synth.Friedman(seed=42).take(10_000),
    metrics.MAE(),
    {
        "Unbounded HTR": (
            preprocessing.StandardScaler() |
            tree.HoeffdingTreeRegressor(splitter=tree.splitter.EBSTSplitter())
        )
    }
)
# %%
plot_performance(
    synth.Friedman(seed=42).take(10_000),
    metrics.MAE(),
    {
        "Restricted HTR": (
            preprocessing.StandardScaler()
            | tree.HoeffdingTreeRegressor(
                splitter=tree.splitter.EBSTSplitter(),
                max_size=5,
                memory_estimate_period=500
            )
        )
    }
)
# %%
plot_performance(
    synth.RandomRBF(seed_model=7, seed_sample=42).take(10_000),
    metrics.Accuracy(),
    {
        "HTC + Exhaustive splitter": tree.HoeffdingTreeClassifier(
            splitter=tree.splitter.ExhaustiveSplitter(),
            leaf_prediction="mc"
        ),
        "HTC + Histogram splitter": tree.HoeffdingTreeClassifier(
            splitter=tree.splitter.HistogramSplitter()
        ),
        "HTC + Gaussian splitter": tree.HoeffdingTreeClassifier(
            splitter=tree.splitter.GaussianSplitter()
        )
    }
)
# %%
plot_performance(
    synth.Friedman(seed=42).take(10_000),
    metrics.MAE(),
    {
        "HTR + E-BST": (
            preprocessing.StandardScaler() | tree.HoeffdingTreeRegressor(
                splitter=tree.splitter.EBSTSplitter()
            )
        ),
        "HTR + TE-BST": (
            preprocessing.StandardScaler() | tree.HoeffdingTreeRegressor(
                splitter=tree.splitter.TEBSTSplitter()
            )
        ),
        "HTR + QO": (
            preprocessing.StandardScaler() | tree.HoeffdingTreeRegressor(
                splitter=tree.splitter.QOSplitter()
            )
        ),

    }
)
# %%
