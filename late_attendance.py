import pandas as pd
from datetime import datetime, timedelta
import mysql.connector
import json

# Step 1: Read the CSV file containing the attendance data
csv_file = 'attendance_late.csv'
attendance_data = pd.read_csv(csv_file)

# Convert AttendanceDateTime to datetime
attendance_data['AttendanceDateTime'] = pd.to_datetime(attendance_data['AttendanceDateTime'])

# Step 2: Fetch input parameters from an SQL table in JSON format
def fetch_input_parameters(cursor):
    query = "SELECT json_input FROM input_table WHERE id = 1;"  # Example query
    cursor.execute(query)
    json_input = cursor.fetchone()[0]
    input_params = json.loads(json_input)
    return input_params

# Example MySQL connection function
def connect_to_mysql(host, username, password, database):
    conn = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )
    return conn

# Example MySQL connection parameters
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'prayagedu'

# Connect to MySQL
conn = connect_to_mysql(db_host, db_user, db_password, db_name)
cursor = conn.cursor()

# Step 3: Analyze the attendance data
def analyze_late_attendance(attendance_data, weeks):
    manual_current_date = attendance_data['AttendanceDateTime'].max()
    start_date = manual_current_date - timedelta(weeks=weeks*7)
    
    # Filter records for the specified period
    relevant_data = attendance_data[(attendance_data['AttendanceDateTime'] >= start_date) & (attendance_data['AttendanceDateTime'] <= manual_current_date)]
    
    # Count the number of late occurrences for each student by day of the week
    relevant_data['Weekday'] = relevant_data['AttendanceDateTime'].dt.day_name()
    late_counts = relevant_data.groupby(['AcademicID', 'Weekday']).size().reset_index(name='LateCount')
    
    # Determine the probability of future lateness
    total_weeks = (manual_current_date - start_date).days / 7
    late_counts['Probability'] = late_counts['LateCount'] / total_weeks
    
    # Identify frequently late students on specific days
    threshold = 1  # Can be adjusted based on requirements
    frequent_offenders = late_counts[late_counts['LateCount'] > threshold]
    
    return frequent_offenders

# Step 4: Create a new table to store the analysis results
def create_analysis_table(cursor, analysis_results):
    cursor.execute("DROP TABLE IF EXISTS late_attendance_analysis;")
    cursor.execute("""
        CREATE TABLE late_attendance_analysis (
            AcademicID INT,
            Weekday VARCHAR(20),
            LateCount INT,
            Probability FLOAT
        );
    """)
    
    for row in analysis_results.itertuples(index=False):
        cursor.execute("""
            INSERT INTO late_attendance_analysis (AcademicID, Weekday, LateCount, Probability)
            VALUES (%s, %s, %s, %s);
        """, (row.AcademicID, row.Weekday, row.LateCount, row.Probability))
    
    conn.commit()

# Perform the analysis
weeks_to_analyze = 4  # Example value from input_params['weeks']
analysis_results = analyze_late_attendance(attendance_data, weeks_to_analyze)

# Create the new table with analysis results
create_analysis_table(cursor, analysis_results)

# Close the cursor and MySQL connection
cursor.close()
conn.close()

# Print results (for debugging purposes)
print("Analysis Results:")
print(analysis_results)
