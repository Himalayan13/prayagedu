import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load the filtered result from the CSV file
df = pd.read_csv('filtered_result.csv')

print("Original DataFrame:")
print(df)

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

# Print the prepared DataFrame
print("\nPrepared DataFrame (after handling missing values):")
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

# Extract and print only the activity name and activity index
activity_df = df[['Most_Frequent_Activity', 'Activity_label']].drop_duplicates().reset_index(drop=True)
print("\nActivity Names and Activity Indices:")
print(activity_df)

# Add a new test record
new_test_data = pd.DataFrame({
    'ActivityDateTime': [pd.to_datetime('2024-05-23 20:15:07')],
    'UserID': [429],
    'hour': [20],
    'minute': [15]
})

# Extract features from the new test record
X_new_test = new_test_data[['UserID', 'hour', 'minute']]

# Predict the activity for the new test record
new_pred = clf.predict(X_new_test)
new_pred_activity = activity_names[new_pred[0]]

print(f"\nNew Test Record Prediction:")
print(f"ActivityDateTime: {new_test_data['ActivityDateTime'].iloc[0]}, UserID: {new_test_data['UserID'].iloc[0]}")
print(f"Predicted Most Frequent Activity: {new_pred_activity}")
