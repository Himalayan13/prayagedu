import pandas as pd
from collections import Counter
import fetch

# Example data creation
data = fetch.fetch_users()
df = pd.DataFrame(data)

print("Original DataFrame:")
print(df.head())

# Convert Activity_time to datetime if not already
df['ActivityDateTime'] = pd.to_datetime(df['ActivityDateTime'])

# Convert Activity_name to numerical indices
activity_counter = Counter(df['ActivityName'])
activity_to_index = {activity: index for index, activity in enumerate(activity_counter.keys())}
index_to_activity = {index: activity for activity, index in activity_to_index.items()}
df['Activity_index'] = df['ActivityName'].map(activity_to_index)

print("\nDataFrame with Activity Indices:")
print(df.head())

# Set Activity_time as index and sort
df = df.set_index('ActivityDateTime').sort_index()

# Resample to a higher frequency ?????
#df = df.resample('10S').ffill()

# Define a function to find the mode in a series of indices
def mode(series):
    if series.empty:
        return None
    return Counter(series).most_common(1)[0][0]

# Group by user_id and apply rolling window of 10 seconds
result = df.groupby('UserID')['Activity_index'].rolling(' ').apply(lambda x: mode(x), raw=False)

# Reset index to make it more readable
result = result.reset_index()

# Convert the numerical indices back to activity names
result['Most_Frequent_Activity'] = result['Activity_index'].map(index_to_activity)

# Rename the result series for clarity
result = result[['ActivityDateTime', 'UserID', 'Most_Frequent_Activity']]

# Filter the results to show changes at every 10-second interval
filtered_result = result[result['ActivityDateTime'].dt.second % 30 == 0]

print("\nRolling Window Result with Most Frequent Activity (filtered at 10-second intervals):")
print(filtered_result)

# Load the filtered result from the CSV file
filtered_result = pd.read_csv('filtered_result.csv')

print("Loaded Filtered Result:")
print(filtered_result)
