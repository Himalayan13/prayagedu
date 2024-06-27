import pandas as pd
from datetime import datetime, timedelta
import fetch 

# Sample data to mimic database 
data = fetch.fetch_users()

df = pd.DataFrame(data)

df['AttendanceDateTime'] = pd.to_datetime(df['AttendanceDateTime'])

# Manually specify the current date
manual_current_date = datetime(2023, 3, 2)

# Calculate the date for one week ago
one_week_ago = manual_current_date - timedelta(days=7)

# Filter records for the last week
last_week_data = df[df['AttendanceDateTime'] >= one_week_ago]

# Count the number of late occurrences for each student
late_counts = last_week_data['AcademicID'].value_counts()

# Determine the threshold for being lat
threshold = 1
frequent_offenders = late_counts[late_counts > threshold]

# Output the results
print("Students who are frequently late in the last week (more than once):")
for student_id, count in frequent_offenders.items():
    print(f"Student ID {student_id} was late {count} times.")
