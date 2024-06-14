import pandas as pd
from collections import Counter
import fetch

# Example data creation (replace with actual fetch function)
data = fetch.fetch_users()
# Load data into DataFrame
df = pd.DataFrame(data)

print("Original DataFrame:")
print(df)

# Convert ActivityDateTime to datetime
df['ActivityDateTime'] = pd.to_datetime(df['ActivityDateTime'])

# Convert ActivityName to numerical indices
activity_counter = Counter(df['ActivityName'])
activity_to_index = {activity: index for index, activity in enumerate(activity_counter.keys())}
index_to_activity = {index: activity for activity, index in activity_to_index.items()}
df['Activity_index'] = df['ActivityName'].map(activity_to_index)

print("\nDataFrame with Activity Indices:")
print(df)

# Set ActivityDateTime as index and sort
df = df.set_index('ActivityDateTime').sort_index()

print("\nDataFrame after setting index and sorting:")
print(df)

# Remove any duplicate entries to avoid reindexing errors
df = df[~df.index.duplicated(keep='first')]

print("\nDataFrame after removing duplicates:")
print(df)

# Define a function to find the mode in a series of indices
def mode(series):
    if series.empty:
        return None
    return Counter(series).most_common(1)[0][0]

# Ensure the index is a datetime-like index
df.index = pd.to_datetime(df.index)

# Group by UserID and apply rolling window of 2 minutes
result = df.groupby('UserID')['Activity_index'].rolling('2T', closed='both').apply(lambda x: mode(x), raw=False)

print("\nRolling Window Result with Activity Indices:")
print(result)

# Reset index to make it more readable
result = result.reset_index()

# Convert the numerical indices back to activity names
result['Most_Frequent_Activity'] = result['Activity_index'].map(index_to_activity)

# Rename the result series for clarity
result = result[['ActivityDateTime', 'UserID', 'Most_Frequent_Activity']]

# Set ActivityDateTime as index and sort, removing any duplicates
result = result.set_index('ActivityDateTime').sort_index()
result = result[~result.index.duplicated(keep='first')]

print("\nResult after setting index and removing duplicates:")
print(result)

# Resample the result to show changes on an hourly basis
resampled_result = result.groupby('UserID').resample('H').ffill().reset_index(level=0, drop=True)

print("\nResampled Result:")
print(resampled_result)

# Reset index to make sure 'UserID' is back as a column
filtered_result = resampled_result.reset_index()

print("\nRolling Window Result with Most Frequent Activity (resampled hourly):")
print(filtered_result)

# Write the filtered result to a CSV file
filtered_result.to_csv('filtered_result.csv', index=False)

print("\nFiltered result has been written to 'filtered_result.csv'")

# Load the filtered result from the CSV file
loaded_result = pd.read_csv('filtered_result.csv')

print("\nLoaded Filtered Result:")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print(loaded_result)
