import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Function to create features from time-indexed data
def create_features(data, window_size):
    # Select only numeric columns for rolling aggregations
    numeric_data = data.select_dtypes(include=['number'])
    
    rolling_data = numeric_data.rolling(window=window_size)
    features = pd.DataFrame(index=numeric_data.index)
    
    # Add rolling statistics as features
    for col in numeric_data.columns:
        features[f'{col}_mean'] = rolling_data[col].mean()
        features[f'{col}_std'] = rolling_data[col].std()
        features[f'{col}_min'] = rolling_data[col].min()
        features[f'{col}_max'] = rolling_data[col].max()
    
    # Additional time-based features
    features['hour'] = data.index.hour
    features['day_of_week'] = data.index.dayofweek
    
    return features.dropna()

# Example data preparation
data = pd.read_csv('activity_logs.csv', index_col='ActivityDateTime', parse_dates=True)

# Adding a hypothetical new feature
np.random.seed(42)  # For reproducibility
data['NewFeature'] = np.random.rand(len(data))  # Replace this with actual data

# Check the datatype of the index to confirm it is datetime
print(data.index.dtype)

# Encode activity names to numeric values
label_encoder = LabelEncoder()
data['ActivityName'] = label_encoder.fit_transform(data['ActivityName'])

# Create features with a rolling window of 15 minutes
X = create_features(data, window_size=15)

# Ensure y is aligned with the features after dropping NaN rows
y = data['ActivityName'].loc[X.index]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate the model
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy}")
