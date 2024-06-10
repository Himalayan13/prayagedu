import pandas as pd
from collections import Counter

# Example data creation (assuming you have a DataFrame 'df')
data = {
    'Activity_time': pd.date_range(start='2024-06-10 00:00:00', periods=100, freq='T'),
    'user_id': ['user1'] * 50 + ['user2'] * 50,
    'Activity_name': ['ActivityA', 'ActivityB', 'ActivityC', 'ActivityD'] * 25
}
df = pd.DataFrame(data)

# Convert Activity_time to datetime if not already
df['Activity_time'] = pd.to_datetime(df['Activity_time'])

# Set Activity_time as index and sort
df = df.set_index('Activity_time').sort_index()

# Define a function to find the mode in a series
def mode(series):
    return Counter(series).most_common(1)[0][0] if not series.empty else None

# Group by user_id
grouped = df.groupby('user_id')

# Apply the resample method for a 30-minute window and find the mode
result = grouped.apply(lambda group: group.resample('30T').apply(lambda x: mode(x['Activity_name'])))

# Reset index to make it more readable
result = result.reset_index()

# Rename columns for clarity
result.columns = ['Activity_time', 'user_id', 'Most_Frequent_Activity']

print(result)
