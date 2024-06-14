import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def load_and_prepare_data(file_path):
    # Load the filtered result from the CSV file
    df = pd.read_csv(file_path)

    # Convert ActivityDateTime to datetime
    df['ActivityDateTime'] = pd.to_datetime(df['ActivityDateTime'])

    # Extract time-based features
    df['hour'] = df['ActivityDateTime'].dt.hour
    df['minute'] = df['ActivityDateTime'].dt.minute

    # Handle missing values
    df['hour'].fillna(df['hour'].mean(), inplace=True)
    df['minute'].fillna(df['minute'].mean(), inplace=True)
    df['UserID'].fillna(df['UserID'].mode()[0], inplace=True)
    mode_activity = df['Most_Frequent_Activity'].mode()[0]
    df['Most_Frequent_Activity'].fillna(mode_activity, inplace=True)

    # Encode Most_Frequent_Activity to numerical labels
    df['Activity_label'] = df['Most_Frequent_Activity'].astype('category').cat.codes
    activity_mapping = dict(enumerate(df['Most_Frequent_Activity'].astype('category').cat.categories))

    # Features and labels
    X = df[['UserID', 'hour', 'minute']]
    y = df['Activity_label']

    return X, y, activity_mapping

def train_model(X, y):
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the classifier with 100 trees
    clf = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the classifier
    clf.fit(X_train, y_train)

    return clf, X_train

def predict_activity(model, X_train, user_id, timestamp, activity_mapping):
    # Extract hour and minute from timestamp
    hour = timestamp.hour
    minute = timestamp.minute

    # Prepare the new test record
    new_test_data = pd.DataFrame({
        'UserID': [user_id],
        'hour': [hour],
        'minute': [minute]
    })

    # Predict the activity for the new test record
    new_pred = model.predict(new_test_data)

    # Decode the predicted activity label to activity name
    predicted_activity = activity_mapping[new_pred[0]]

    return predicted_activity

# Example usage:
if __name__ == "__main__":
    # Load and prepare data
    X, y, activity_mapping = load_and_prepare_data('filtered_result.csv')

    # Train the classifier
    model, X_train = train_model(X, y)

    # Add a new test record
    new_timestamp = pd.to_datetime('2024-05-02 22:50:50')
    user_id = 104
    predicted_activity = predict_activity(model, X_train, user_id, new_timestamp, activity_mapping)

    print(f"\nNew Test Record Prediction:")
    print(f"Timestamp: {new_timestamp}, UserID: {user_id}")
    print(f"Predicted Most Frequent Activity: {predicted_activity}")
