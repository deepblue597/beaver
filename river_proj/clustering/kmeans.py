# %%
import matplotlib.pyplot as plt
from river import cluster

# Example 2D points
data = [
    {"x": 1, "y": 2},
    {"x": 1, "y": 4},
    {"x": 1, "y": 0},
    {"x": -4, "y": 2},
    {"x": -4, "y": 4},
    {"x": -4, "y": 0}
]

# Initialize online KMeans with 3 clusters
model = cluster.KMeans(n_clusters=2, halflife=0.1, sigma=1, seed=42)
# Plot setup
plt.figure(figsize=(8, 6))

# Colors for clusters
colors = ['red', 'blue']

# Collect data points for plotting
points_x = []
points_y = []
cluster_assignments = []

# Learn clusters incrementally
for point in data:
    # Extract coordinates
    x, y = point["x"], point["y"]
    points_x.append(x)
    points_y.append(y)

    # Learn the point and predict cluster
    model.learn_one(point)
    cluster_assignments.append(model.predict_one(point))

# Plot data points color-coded by cluster
for i, (x, y) in enumerate(zip(points_x, points_y)):
    plt.scatter(x, y, color=colors[cluster_assignments[i]], s=100)

# Plot centroids
centroids = model.centers
for idx, (center_name, center) in enumerate(centroids.items()):
    plt.scatter(center["x"], center["y"], color=colors[idx],
                marker='X', s=200, edgecolor='black')

plt.title("K-Means Clustering Results")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.show()

# %%
