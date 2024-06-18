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
    # For numerical columns, use mean imputation
    df['hour'].fillna(df['hour'].mean(), inplace=True)
    df['minute'].fillna(df['minute'].mean(), inplace=True)

    # For UserID, use mode imputation
    df['UserID'].fillna(df['UserID'].mode()[0], inplace=True)

    # For Most_Frequent_Activity, use mode imputation
    mode_activity = df['Most_Frequent_Activity'].mode()[0]
    df['Most_Frequent_Activity'].fillna(mode_activity, inplace=True)

    # Encode Most_Frequent_Activity to numerical labels
    df['Activity_label'] = df['Most_Frequent_Activity'].astype('category').cat.codes

    # Features and labels
    X = df[['UserID', 'hour', 'minute']]
    y = df['Activity_label']

    return X, y, df

def train_classifier(X, y):
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the classifier with 100 trees
    clf = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the classifier
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Decode the activity labels for the classification report
    activity_names = y.astype('category').cat.categories

    # Evaluate the model's performance
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=activity_names)

    return clf, accuracy, report, activity_names, X_train

def predict_activity(model, X_train, activity_names, user_id, timestamp):
    # Extract hour and minute from timestamp
    timestamp = pd.to_datetime(timestamp)
    hour = timestamp.hour
    minute = timestamp.minute

    # Add a new test record for a specific period and activity
    new_test_data = pd.DataFrame({
        'UserID': [user_id],
        'hour': [hour],
        'minute': [minute]
    })

    # Extract features from the new test record
    X_new_test = new_test_data[['UserID', 'hour', 'minute']]

    # Align the new test record with the training data columns
    X_new_test = X_new_test.reindex(columns=X_train.columns, fill_value=0)

    # Predict the activity for the new test record
    new_pred = model.predict(X_new_test)
    new_pred_activity = activity_names[new_pred[0]]

    return new_pred_activity

if __name__ == "__main__":
    # Load and prepare data
    X, y, df = load_and_prepare_data('filtered_result.csv')

    # Train the classifier
    model, accuracy, report, activity_names, X_train = train_classifier(X, y)

    # Print the evaluation results
    print(f"\nRandom Forest Classifier Accuracy: {accuracy:.2f}")
    print("\nRandom Forest Classifier Classification Report:")
    print(report)

    # Extract and print only the activity name and activity index
    activity_df = df[['Most_Frequent_Activity', 'Activity_label']].drop_duplicates().reset_index(drop=True)
    print("\nActivity Names and Activity Indices:")
    print(activity_df)

    # Predict the activity for a new user and timestamp
    user_id = 52
    timestamp = '2024-05-03 21:53:43'
    predicted_activity = predict_activity(model, X_train, activity_names, user_id, timestamp)

    print(f"\nPredicted Most Frequent Activity for User ID {user_id} at {timestamp}: {predicted_activity}")
