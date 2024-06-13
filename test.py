
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import fetch
import preprocess

# Define functions for entropy and information gain
def calculate_entropy(labels):
    unique_labels, counts = np.unique(labels, return_counts=True)
    probabilities = counts / len(labels)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

def calculate_information_gain(data, attribute, labels):
    entropy_before_split = calculate_entropy(labels)
    unique_attribute_values = np.unique(data[attribute])
    entropy_after_split = 0
    for value in unique_attribute_values:
        subset_labels = labels[data[attribute] == value]
        subset_entropy = calculate_entropy(subset_labels)
        weight = len(subset_labels) / len(labels)
        entropy_after_split += weight * subset_entropy
    information_gain = entropy_before_split - entropy_after_split
    return information_gain

# Define ID3 algorithm
def id3(data, attributes, labels):
    if len(np.unique(labels)) == 1:
        return labels.iloc[0]

    if len(attributes) == 0:
        return labels.mode()[0]

    information_gains = {attribute: calculate_information_gain(data, attribute, labels) for attribute in attributes}
    best_attribute = max(information_gains, key=information_gains.get)
    
    node = {best_attribute: {}}
    
    for value in data[best_attribute].unique():
        subset_data = data[data[best_attribute] == value]
        subset_labels = labels[data[best_attribute] == value]
        if len(subset_data) == 0:
            node[best_attribute][value] = labels.mode()[0]
        else:
            remaining_attributes = [attr for attr in attributes if attr != best_attribute]
            node[best_attribute][value] = id3(subset_data, remaining_attributes, subset_labels)
    
    return node

# Define predict function
def predict(tree, instance, default=None):
    if not isinstance(tree, dict):
        return tree
    for attribute in tree.keys():
        value = instance.get(attribute, None)
        subtree = tree[attribute].get(value, default)
        if subtree is None:
            return default
        return predict(subtree, instance, default)

# Main script
if __name__ == "__main__":
    # Fetch and preprocess the data
    data = fetch.fetch_users()
    if data:
        processed_data = preprocess.preprocess_data(data)

        # Extract features and target variable
        X = processed_data[['UserID', 'Hour', 'DayOfWeek', 'IsWeekend']]
        y = processed_data['ActivityName']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Build the decision tree using ID3 algorithm
        tree = id3(X_train, X_train.columns.tolist(), y_train)

        # Make predictions on the test set
        y_pred = X_test.apply(lambda instance: predict(tree, instance, default=y_train.mode()[0]), axis=1)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print("Model Accuracy:", accuracy)
        
        # Static input for prediction with new values
        input_instance = {'UserID': 365, 'Hour': 1, 'DayOfWeek': 5, 'IsWeekend': 1}
        predicted_activity = predict(tree, input_instance, default=y_train.mode()[0])
        print("Predicted activity for input instance:", predicted_activity)
    else:
        print("No data fetched")
    