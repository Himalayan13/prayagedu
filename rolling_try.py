import pandas as pd
from collections import Counter
import fetch  # Assuming this is a custom module to fetch user data

# Fetch user data
data = fetch.fetch_users()
df = pd.DataFrame(data)

print("Original DataFrame:")
print(df.head())

# Convert ActivityDateTime to datetime if not already
df['ActivityDateTime'] = pd.to_datetime(df['ActivityDateTime'])

# Convert ActivityName to numerical indices
activity_counter = Counter(df['ActivityName'])
activity_to_index = {activity: index for index, activity in enumerate(activity_counter.keys())}
index_to_activity = {index: activity for activity, index in activity_to_index.items()}
df['Activity_index'] = df['ActivityName'].map(activity_to_index)

print("\nDataFrame with Activity Indices:")
print(df.head())

# Set ActivityDateTime as index and sort
df = df.set_index('ActivityDateTime').sort_index()

# Remove any duplicate entries to avoid reindexing errors
df = df[~df.index.duplicated(keep='first')]

# Define a function to find the mode in a series of indices
def mode(series):
    if series.empty:
        return None
    return Counter(series).most_common(1)[0][0]

# Ensure the index is a datetime-like index
df.index = pd.to_datetime(df.index)

# Group by UserID and apply rolling window of 2 minutes
result = df.groupby('UserID')['Activity_index'].rolling('2T', closed='both').apply(lambda x: mode(x), raw=False)

# Reset index to make it more readable
result = result.reset_index()

# Convert the numerical indices back to activity names
result['Activity_index'] = result['Activity_index'].astype(int)  # Ensure indices are integers for mapping
result['Most_Frequent_Activity'] = result['Activity_index'].map(index_to_activity)

# Rename the result series for clarity
result = result[['ActivityDateTime', 'UserID', 'Most_Frequent_Activity']]

print("\nRolling Window Result with Most Frequent Activity (Original Time Periods):")
print(result)

# Write the new filtered result to a new CSV file
result.to_csv('new_filtered_result.csv', index=False)

print("\nNew filtered result has been written to 'new_filtered_result.csv'")
