# %%
import matplotlib.pyplot as plt
from river import cluster
from river import stream

# Input data
X = [
    [1, 0.5], [1, 0.625], [1, 0.75], [1, 1.125], [1, 1.5], [1, 1.75],
    [4, 1.5], [4, 2.25], [4, 2.5], [4, 3], [4, 3.25], [4, 3.5]
]

# Initialize DBSTREAM
dbstream = cluster.DBSTREAM(
    clustering_threshold=1.5,
    fading_factor=0.05,
    cleanup_interval=4,
    intersection_factor=0.5,
    minimum_weight=1
)

# Train the model and store cluster assignments
cluster_assignments = []
for x, _ in stream.iter_array(X):
    dbstream.learn_one(x)
    cluster_id = dbstream.predict_one(x)
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

# Add labels and legend
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('DBSTREAM Clustering')
plt.legend()
plt.grid(True)
plt.show()

# %%

dbstream.centers
# %%

# %%
