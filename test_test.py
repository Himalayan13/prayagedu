import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Provided dataset
data = {
    'ActivityDateTime': [
        '2024-05-02 16:54:30', '2024-05-03 21:54:30', '2024-05-03 21:54:30',
        '2024-05-02 23:05:30', '2024-05-02 23:05:30', '2024-05-04 12:21:00',
        '2024-05-04 13:48:30', '2024-05-04 14:03:30', '2024-05-04 14:03:30'
    ],
    'UserID': [2, 38, 38, 52, 104, 199, 430, 683, 683],
    'Most_Frequent_Activity': [
        'RemarkScreen', 'StudentAttendanceScreen', 'StudentAttendanceScreen',
        'OthersInfo', 'NoticeBord', 'studentAssignment', 'StudentHomePage',
        'StudentAttendanceScreen', 'StudentAttendanceScreen'
    ]
}
df = pd.DataFrame(data)

print("Original DataFrame:")
print(df)

# Convert ActivityDateTime to datetime
df['ActivityDateTime'] = pd.to_datetime(df['ActivityDateTime'])

# Extract time-based features
df['hour'] = df['ActivityDateTime'].dt.hour
df['minute'] = df['ActivityDateTime'].dt.minute

# Encode Most_Frequent_Activity to numerical labels
df['Activity_label'] = df['Most_Frequent_Activity'].astype('category').cat.codes

# Print the prepared DataFrame
print("\nPrepared DataFrame:")
print(df)

# Features and labels
X = df[['UserID', 'hour', 'minute']]
y = df['Activity_label']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Print the shapes of the splits
print(f"\nTraining set shape: {X_train.shape}, Testing set shape: {X_test.shape}")

# Initialize the classifier with 100 trees
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the classifier
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Decode the activity labels for the classification report
activity_names = df['Most_Frequent_Activity'].astype('category').cat.categories

# Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=activity_names, labels=np.unique(y_pred))

# Print the evaluation results
print(f"\nAccuracy: {accuracy:.2f}")
print("\nClassification Report:")
print(report)

# Add a new test record
new_test_data = pd.DataFrame({
    'ActivityDateTime': [pd.to_datetime('2024-05-02 23:05:30')],
    'UserID': [52],
    'hour': [23],
    'minute': [5]
})

# Extract features from the new test record
X_new_test = new_test_data[['UserID', 'hour', 'minute']]

# Predict the activity for the new test record
new_pred = clf.predict(X_new_test)
new_pred_activity = activity_names[new_pred[0]]

print(f"\nNew Test Record Prediction:")
print(f"ActivityDateTime: {new_test_data['ActivityDateTime'].iloc[0]}, UserID: {new_test_data['UserID'].iloc[0]}")
print(f"Predicted Most Frequent Activity: {new_pred_activity}")
