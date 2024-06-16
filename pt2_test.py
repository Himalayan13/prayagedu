import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
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

# Aggregate data by time periods (e.g., hourly)
df['time_period'] = df['hour'].apply(lambda x: f'{x:02d}-{(x+1)%24:02d}')

# Print the prepared DataFrame
print("\nPrepared DataFrame (after handling missing values and time period extraction):")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print(df)

# Features and labels
X_period = df[['UserID', 'time_period']]
y_period = df['Activity_label']

# One-hot encode the time_period feature
X_period = pd.get_dummies(X_period, columns=['time_period'])

# Split the dataset into training and testing sets
X_train_period, X_test_period, y_train_period, y_test_period = train_test_split(X_period, y_period, test_size=0.2, random_state=42)

# Print the shapes of the splits
print(f"\nTraining set shape: {X_train_period.shape}, Testing set shape: {X_test_period.shape}")

# Initialize the GradientBoostingClassifier
clf_period_gb = GradientBoostingClassifier(random_state=42)

# Train the GradientBoostingClassifier
clf_period_gb.fit(X_train_period, y_train_period)

# Make predictions on the test set using GradientBoostingClassifier
y_pred_period_gb = clf_period_gb.predict(X_test_period)

# Decode the activity labels for the classification report
activity_names = df['Most_Frequent_Activity'].astype('category').cat.categories

# Evaluate the GradientBoostingClassifier's performance
accuracy_period_gb = accuracy_score(y_test_period, y_pred_period_gb)
report_period_gb = classification_report(y_test_period, y_pred_period_gb, target_names=activity_names, labels=np.unique(y_pred_period_gb))

# Print the evaluation results for GradientBoostingClassifier
print(f"\nGradient Boosting Classifier Accuracy: {accuracy_period_gb:.2f}")
print("\nGradient Boosting Classifier Classification Report:")
print(report_period_gb)

# Add a new test record for a specific period
new_period_test_data = pd.DataFrame({
    'UserID': [52],
    'time_period': ['11-12']
})

# One-hot encode the new test record's time_period feature
X_new_period_test = pd.get_dummies(new_period_test_data, columns=['time_period'])

# Align the new test record with the training data columns
X_new_period_test = X_new_period_test.reindex(columns=X_train_period.columns, fill_value=0)

# Predict the activity for the new test record using GradientBoostingClassifier
new_period_pred_gb = clf_period_gb.predict(X_new_period_test)
new_period_pred_activity_gb = activity_names[new_period_pred_gb[0]]

print(f"\nNew Period Test Record Prediction using GradientBoostingClassifier:")
print(f"UserID: {new_period_test_data['UserID'].iloc[0]}, Time Period: {new_period_test_data['time_period'].iloc[0]}")
print(f"Predicted Most Frequent Activity: {new_period_pred_activity_gb}")
