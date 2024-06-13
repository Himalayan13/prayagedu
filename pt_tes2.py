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
X = df[['UserID', 'Most_Frequent_Activity']]
y = df['time_period']

# One-hot encode the Most_Frequent_Activity feature
X = pd.get_dummies(X, columns=['Most_Frequent_Activity'])

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Print the shapes of the splits
print(f"\nTraining set shape: {X_train.shape}, Testing set shape: {X_test.shape}")

# Initialize the GradientBoostingClassifier
clf_gb = GradientBoostingClassifier(random_state=42)

# Train the GradientBoostingClassifier
clf_gb.fit(X_train, y_train)

# Make predictions on the test set using GradientBoostingClassifier
y_pred_gb = clf_gb.predict(X_test)

# Evaluate the GradientBoostingClassifier's performance
accuracy_gb = accuracy_score(y_test, y_pred_gb)
report_gb = classification_report(y_test, y_pred_gb)

# Print the evaluation results for GradientBoostingClassifier
print(f"\nGradient Boosting Classifier Accuracy: {accuracy_gb:.2f}")
print("\nGradient Boosting Classifier Classification Report:")
print(report_gb)

# Add a new test record for a specific period and activity
new_test_data = pd.DataFrame({
    'UserID': [104],
    'Most_Frequent_Activity': ['Fees']
})

# One-hot encode the new test record's Most_Frequent_Activity feature
X_new_test = pd.get_dummies(new_test_data, columns=['Most_Frequent_Activity'])

# Align the new test record with the training data columns
X_new_test = X_new_test.reindex(columns=X_train.columns, fill_value=0)

# Predict the time period for the new test record using GradientBoostingClassifier
new_pred_gb = clf_gb.predict(X_new_test)

print(f"\nNew Test Record Prediction using GradientBoostingClassifier:")
print(f"UserID: {new_test_data['UserID'].iloc[0]}, Most Frequent Activity: {new_test_data['Most_Frequent_Activity'].iloc[0]}")
print(f"Predicted Time Period: {new_pred_gb[0]}")
