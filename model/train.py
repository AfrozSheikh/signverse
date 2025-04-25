import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from collections import Counter

# Load data
data_dict = pickle.load(open('./data6.pickle', 'rb'))

# Analyze the data shapes
print(f"Total data points: {len(data_dict['data'])}")
print(f"Total labels: {len(data_dict['labels'])}")

# First, let's examine what our data looks like
shapes = []
for i, data_point in enumerate(data_dict['data'][:1000]):  # Check first 1000 points to get an idea
    try:
        if isinstance(data_point, (list, np.ndarray)):
            shape = np.asarray(data_point).shape
            shapes.append(shape)
        else:
            print(f"Data point {i} is not a list or array but a {type(data_point)}")
    except Exception as e:
        print(f"Error with data point {i}: {e}")

# Display the most common shapes
print("Most common shapes:", Counter(shapes).most_common(5))

# Let's find the most common shape and filter to only keep data points with that shape
if shapes:
    most_common_shape = Counter(shapes).most_common(1)[0][0]
    print(f"Most common shape: {most_common_shape}")
    
    # Filter data to keep only items with the most common shape
    filtered_data = []
    filtered_labels = []
    
    for i, data_point in enumerate(data_dict['data']):
        try:
            np_data = np.asarray(data_point)
            if np_data.shape == most_common_shape:
                filtered_data.append(np_data)
                filtered_labels.append(data_dict['labels'][i])
        except Exception as e:
            print(f"Skipping data point {i} due to: {e}")
    
    print(f"Filtered data size: {len(filtered_data)}")
    print(f"Filtered labels size: {len(filtered_labels)}")
    
    # Convert filtered data to numpy array
    if filtered_data:
        # Stack the arrays instead of using np.array() directly
        data = np.stack(filtered_data)
        labels = np.array(filtered_labels)
        
        # Proceed with model training
        print(f"Final data shape: {data.shape}")
        print(f"Final labels shape: {labels.shape}")
        
        if len(np.unique(labels)) > 1:
            x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.1, 
                                                             shuffle=True, stratify=labels)
            
            model = RandomForestClassifier()
            model.fit(x_train, y_train)
            
            y_predict = model.predict(x_test)
            score = accuracy_score(y_predict, y_test)
            
            print('{}% of samples were classified correctly!'.format(score * 100))
            
            f = open('model6.p', 'wb')
            pickle.dump({'model6': model}, f)
            f.close()
        else:
            print("Not enough class labels for stratification.")
    else:
        print("No valid data points to train the model.")
else:
    print("Could not determine consistent shapes in the data.")