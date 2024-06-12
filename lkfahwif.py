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

# Encode Most_Frequent_Activity to numerical labels
df['Activity_label'] = df['Most_Frequent_Activity'].astype('category').cat.codes

df['hour'].fillna(df['hour'].mean(), inplace=True)
df['minute'].fillna(df['minute'].mean(), inplace=True)

# For categorical columns, use mode imputation
df['UserID'].fillna(df['UserID'].mode()[0], inplace=True)
df['Most_Frequent_Activity'].fillna(df['Most_Frequent_Activity'].mode()[0], inplace=True)
df['Activity_label'].fillna(df['Activity_label'].mode()[0], inplace=True)

# Adjust display settings to show the entire DataFrame
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Print the prepared DataFrame
print("\nPrepared DataFrame:")
print(df)
