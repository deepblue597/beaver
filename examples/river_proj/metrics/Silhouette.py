# %%
from river import cluster
from river import stream
from river import metrics
X = [
    [1, 2],
    [1, 4],
    [1, 0],
    [4, 2],
    [4, 4],
    [4, 0],
    [-2, 2],
    [-2, 4],
    [-2, 0]
]

k_means = cluster.KMeans(n_clusters=3, halflife=0.4, sigma=3, seed=0)
metric = metrics.Silhouette()

for x, _ in stream.iter_array(X):
    k_means.learn_one(x)
    y_pred = k_means.predict_one(x)
    metric.update(x, y_pred, k_means.centers)

metric
# %%
