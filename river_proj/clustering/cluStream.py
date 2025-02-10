# %%
from river_proj import cluster
from river_proj import stream
import matplotlib.pyplot as plt

X = [
    [1, 2],
    [1, 4],
    [1, 0],
    [-4, 2],
    [-4, 4],
    [-4, 0],
    [5, 0],
    [5, 2],
    [5, 4],
    [0, 1]
]

clustream = cluster.CluStream(
    n_macro_clusters=3,
    max_micro_clusters=5,
    time_gap=3,
    seed=0,
    halflife=0.4
)

# Train the model and store cluster assignments
cluster_assignments = []
for x, _ in stream.iter_array(X):
    clustream.learn_one(x)
    cluster_id = clustream.predict_one(x)
    cluster_assignments.append(cluster_id)

# Separate data points by cluster
clusters = {}
for i, (x, cluster_id) in enumerate(zip(X, cluster_assignments)):
    if cluster_id not in clusters:
        clusters[cluster_id] = []
    clusters[cluster_id].append(x)

# Plot the clusters
plt.figure(figsize=(8, 6))
for cluster_id, points in clusters.items():
    points = list(zip(*points))  # Transpose the list of points
    plt.scatter(points[0], points[1], label=f'Cluster {cluster_id}')

# Plot the cluster centers
for cluster_id, center in clustream.centers.items():
    plt.scatter(center[0], center[1],
                marker='x', s=100, label='Center')

# Add labels and legend
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('clustream Clustering')
plt.legend()
plt.grid(True)
plt.show()

# %%
clustream.predict_one({0: 1, 1: 1})

# %%
clustream.centers
# %%
