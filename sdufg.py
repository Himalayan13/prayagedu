import pandas as pd
from collections import Counter

# Example data creation (assuming you have a DataFrame 'df')
data = {
    'Activity_time': pd.date_range(start='2024-06-10 00:00:00', periods=100, freq='T'),
    'user_id': ['user1'] * 50 + ['user2'] * 50,
    'Activity_name': ['ActivityA', 'ActivityB', 'ActivityC', 'ActivityD'] * 25
}
df = pd.DataFrame(data)
print(df)