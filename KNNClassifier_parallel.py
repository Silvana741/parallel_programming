import numpy as np
from concurrent.futures import ProcessPoolExecutor

class KNNClassifier_parallel:
    def __init__(self, k=3, num_workers=4):
        self.k = k
        self.num_workers = num_workers  # Number of workers for parallelization

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def euclidean_distance(self, x1, x2):
        diff = (x1 - x2)
        sqr_diff = diff ** 2
        sqr_diff_sum = np.sum(sqr_diff)
        return np.sqrt(sqr_diff_sum)

    def predict(self, X):
        # Use ProcessPoolExecutor to parallelize prediction over multiple processes
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            y_pred = list(executor.map(self._predict, X))
        return np.array(y_pred)

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
