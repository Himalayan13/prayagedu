import pandas as pd
from collections import Counter
import fetch

# Example data creation
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
result['Most_Frequent_Activity'] = result['Activity_index'].map(index_to_activity)

# Rename the result series for clarity
result = result[['ActivityDateTime', 'UserID', 'Most_Frequent_Activity']]

# Filter the results to show changes at every 2-minute interval
filtered_result = result[result['ActivityDateTime'].dt.second % 120 == 0]

print("\nRolling Window Result with Most Frequent Activity (filtered at 2-minute intervals):")
print(filtered_result)

# Write the filtered result to a CSV file
filtered_result.to_csv('filtered_result.csv', index=False)

print("\nFiltered result has been written to 'filtered_result.csv'")

# Load the filtered result from the CSV file
loaded_result = pd.read_csv('filtered_result.csv')

print("\nLoaded Filtered Result:")
print(loaded_result.head())
