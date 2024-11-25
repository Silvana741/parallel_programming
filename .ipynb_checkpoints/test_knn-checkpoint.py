from KNNClassifier import KNNClassifier
import numpy as np
import time 
import pprint
# Example with random data
rows = 100000
cols = 500
np.random.seed(699)
X_train = np.random.rand(rows*cols).reshape((rows,cols))
y_train = np.random.randint(2, size=rows)
print(f'X_train shape {X_train.shape} - y_train shape {y_train.shape}')

knn = KNNClassifier(k=2)
knn.fit(X_train, y_train)

# Create random indices to test
test_size = 1000
X_test = np.random.randint(rows, size=test_size)

# Generate Predictions
num_runs = 30
real_times = []
cpu_times = []
for _ in range(num_runs):
    start_real = time.time()
    start_cpu = time.process_time()
    
    predictions = knn.predict(X_train[X_test])
    #print(f'Prediction {predictions}')
    #print(f'Label      {y_train[X_test]}')
    # Calculate the number of equal elements
    print(f'correct {np.sum(y_train[X_test] == predictions)}')

    end_real = time.time()
    end_cpu = time.process_time()
        
    real_times.append(end_real - start_real)
    cpu_times.append(end_cpu - start_cpu)

avg_real_time = np.mean(real_times)
std_real_time = np.std(real_times)
avg_cpu_time = np.mean(cpu_times)
std_cpu_time = np.std(cpu_times)

results = {
    "avg_real_time": np.mean(real_times),
    "std_real_time": np.std(real_times),
    "avg_cpu_time": np.mean(cpu_times),
    "std_cpu_time": np.std(cpu_times)
}

pprint.pprint(f"The results for sequential run are ", results)

import matplotlib.pyplot as plt

plt.hist(real_times, bins=10, alpha=0.5, label='Real Time')
plt.hist(cpu_times, bins=10, alpha=0.5, label='CPU Time')
plt.legend()
plt.title('Benchmark Time Distribution')
plt.xlabel('Time (s)')
plt.ylabel('Frequency')
plt.show()

    
