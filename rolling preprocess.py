import pandas as pd
from collections import Counter

# Example data creation
data = {
    'Activity_time': pd.date_range(start='2024-06-10 00:00:00', periods=100, freq='T'),
    'user_id': ['user1'] * 50 + ['user2'] * 50,
    'Activity_name': ['ActivityA', 'ActivityB', 'ActivityC', 'ActivityD'] * 25
}
df = pd.DataFrame(data)

print("Original DataFrame:")
print(df.head())

# Convert Activity_time to datetime if not already
df['Activity_time'] = pd.to_datetime(df['Activity_time'])

# Convert Activity_name to numerical indices
activity_counter = Counter(df['Activity_name'])
activity_to_index = {activity: index for index, activity in enumerate(activity_counter.keys())}
index_to_activity = {index: activity for activity, index in activity_to_index.items()}
df['Activity_index'] = df['Activity_name'].map(activity_to_index)

print("\nDataFrame with Activity Indices:")
print(df.head())

# Set Activity_time as index and sort
df = df.set_index('Activity_time').sort_index()

# Resample to a higher frequency
df = df.resample('10S').ffill()

# Define a function to find the mode in a series of indices
def mode(series):
    if series.empty:
        return None
    return Counter(series).most_common(1)[0][0]

# Group by user_id and apply rolling window of 10 seconds
result = df.groupby('user_id')['Activity_index'].rolling('10S').apply(lambda x: mode(x), raw=False)

# Reset index to make it more readable
result = result.reset_index()

# Convert the numerical indices back to activity names
result['Most_Frequent_Activity'] = result['Activity_index'].map(index_to_activity)

# Rename the result series for clarity
result = result[['Activity_time', 'Most_Frequent_Activity']]

# Filter the results to show changes at every 10-second interval
filtered_result = result[result['Activity_time'].dt.second % 10 == 0]

print("\nRolling Window Result with Most Frequent Activity (filtered at 10-second intervals):")
print(filtered_result.head(40))
