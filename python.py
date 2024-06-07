import fetch
import preprocess
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

class Node:
    def __init__(self, attribute=None, value=None, children=None, prediction=None):
        self.attribute = attribute  # Attribute used for splitting
        self.value = value  # Value of the attribute for current node
        self.children = children  # Dictionary of {attribute value: child node}
        self.prediction = prediction  # Prediction for leaf node (class label)


def calculate_entropy(labels):
    # Calculate entropy of a list of labels
    unique_labels, counts = np.unique(labels, return_counts=True)
    probabilities = counts / len(labels)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy


def calculate_information_gain(data, attribute, labels):
    # Calculate information gain for a given attribute
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


def id3(data, attributes, labels):
    # ID3 algorithm for building decision tree
    if len(np.unique(labels)) == 1:
        # If all labels are the same, return a leaf node with that label
        return Node(prediction=labels.iloc[0])

    if len(attributes) == 0:
        # If no more attributes left, return a leaf node with the majority label
        majority_label = labels.value_counts().idxmax()
        return Node(prediction=majority_label)

    # Select the best attribute for splitting
    information_gains = {attribute: calculate_information_gain(data, attribute, labels) for attribute in attributes}
    best_attribute = max(information_gains, key=information_gains.get)

    # Create a new internal node with the best attribute
    node = Node(attribute=best_attribute)

    # Recursively build the tree for each value of the best attribute
    for value in data[best_attribute].unique():
        subset_data = data[data[best_attribute] == value]
        subset_labels = labels[data[best_attribute] == value]
        if len(subset_data) == 0:
            # If no data for the value, return a leaf node with the majority label
            majority_label = labels.value_counts().idxmax()
            node.children[value] = Node(prediction=majority_label)
        else:
            # Recursively build the tree
            remaining_attributes = [attr for attr in attributes if attr != best_attribute]
            node.children[value] = id3(subset_data, remaining_attributes, subset_labels)

    return node


def predict(tree, instance):
    # Predict class label for a new instance
    if tree.prediction is not None:
        # If leaf node, return the prediction
        return tree.prediction
    else:
        # Traverse the tree recursively based on attribute values
        attribute_value = instance[tree.attribute]
        if attribute_value not in tree.children:
            # If unknown attribute value, return majority label
            return tree.prediction
        else:
            # Recursively predict using child node
            return predict(tree.children[attribute_value], instance)


if __name__ == "__main__":
    # Fetch and prepare data
    data = fetch.fetch_users()
    if data:
        # Preprocess the data
        processed_data = preprocess.preprocess_data(data)
        
        # Extract features and target variable
        X = processed_data[['UserID', 'IsWeekend']]
        y = processed_data['ActivityName']
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model using ID3 algorithm
        tree = id3(X_train, X_train.columns, y_train)
        
        # Make predictions on the test set
        y_pred = X_test.apply(lambda instance: predict(tree, instance), axis=1)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print("Model Accuracy:", accuracy)
    else:
        print("No data fetched")
