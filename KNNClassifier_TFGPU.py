import tensorflow as tf

class KNNClassifier:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        """
        Stores the training data as TensorFlow tensors for GPU acceleration.
        
        Args:
        X: Training features, should be a 2D NumPy array or TensorFlow tensor.
        y: Training labels, should be a 1D NumPy array or TensorFlow tensor.
        """
        self.X_train = tf.constant(X, dtype=tf.float32)
        self.y_train = tf.constant(y, dtype=tf.int32)

    def euclidean_distance(self, x1, x2):
        """
        Calculates the Euclidean distance between two points using TensorFlow.
        
        Args:
        x1: First point, a 1D TensorFlow tensor.
        x2: Second point, a 1D TensorFlow tensor.
        
        Returns:
        A scalar TensorFlow tensor representing the distance.
        """
        return tf.sqrt(tf.reduce_sum(tf.square(x1 - x2), axis=-1))

    def predict(self, X):
        """
        Predicts the class for each point in the input dataset.
        
        Args:
        X: Input features, should be a 2D NumPy array or TensorFlow tensor.
        
        Returns:
        A 1D NumPy array of predicted class labels.
        """
        X_test = tf.constant(X, dtype=tf.float32)

        # Compute pairwise distances using broadcasting
        distances = tf.norm(
            tf.expand_dims(X_test, axis=1) - tf.expand_dims(self.X_train, axis=0), axis=2
        )

        # Get indices of the k smallest distances for each test point
        k_indices = tf.argsort(distances, axis=1)[:, :self.k]

        # Gather the labels of the k nearest neighbors
        k_nearest_labels = tf.gather(self.y_train, k_indices)

        # Majority vote: find the most common class among the k neighbors
        predictions = tf.map_fn(
            lambda x: tf.math.bincount(x, minlength=tf.reduce_max(self.y_train) + 1).numpy().argmax(),
            k_nearest_labels,
            fn_output_signature=tf.int64
        )

        return predictions.numpy()
