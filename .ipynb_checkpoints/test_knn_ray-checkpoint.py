import numpy as np
import ray

@ray.remote
class KNNClassifier:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def euclidean_distance(self, x1, x2):
        diff = (x1 - x2)
        sqr_diff = diff ** 2
        sqr_diff_sum = np.sum(sqr_diff)
        return np.sqrt(sqr_diff_sum)

    def predict(self, X):
        # Use ray remote tasks for parallel predictions
        predictions = ray.get([self._predict.remote(x) for x in X])
        return np.array(predictions)

    @ray.remote
    def _predict(self, x):
        # Calculate distances from the input point to all training points
        distances = [self.euclidean_distance(x, x_train) for x_train in self.X_train]
        # Sort by distance and return indices of the first k neighbors
        k_indices = np.argsort(distances)[:self.k]
        # Extract the labels of the k nearest neighbor training samples
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        # Return the most common class label among the k nearest neighbors
        most_common = np.bincount(k_nearest_labels).argmax()
        return most_common

# Initialize Ray
ray.init()

# Total cluster resources
total_resources = ray.cluster_resources()
print("Total cluster resources:", total_resources)

# Available resources
available_resources = ray.available_resources()
print("Available resources:", available_resources)

# # Example usage
# if __name__ == "__main__":
# Create and fit the model
rows = 100000
cols = 500
np.random.seed(699)
X_train = np.random.rand(rows*cols).reshape((rows,cols))
y_train = np.random.randint(2, size=rows)

knn = KNNClassifier.remote(k=2)
ray.get(knn.fit.remote(X_train, y_train))

test_size = 1000
X_test = np.random.randint(rows, size=test_size)

# Make predictions
predictions = ray.get(knn.predict.remote(X_test))
print(predictions)

# Shutdown Ray when done
ray.shutdown()
