import pandas as pd
from datetime import datetime, timedelta
import mysql.connector
import json

# Step 1: Read the CSV file containing the attendance data
csv_file = 'attendance_late.csv'
attendance_data = pd.read_csv(csv_file)

# Convert AttendanceDateTime to datetime
attendance_data['AttendanceDateTime'] = pd.to_datetime(attendance_data['AttendanceDateTime'])
# print("Attendance CSV File:")
# print(attendance_data)

# Step 2: Fetch input parameters from an SQL table in JSON format
def fetch_input_parameters(cursor):
    query = "SELECT AnalysisInput FROM analysis_settings_inputs WHERE AnalysisType = 'LateWise';"  # Example query
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        print("No parameter found")
        return None
    json_input = result[0]
    input_params = json.loads(json_input)
    print("Fetched input parameters:", input_params)  # Debugging line
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

# Fetch input parameters
input_params = fetch_input_parameters(cursor)
if input_params is None:
    cursor.close()
    conn.close()
    raise ValueError("No input parameters found")
if 'WTC' not in input_params or 'AT' not in input_params or 'PT' not in input_params:
    cursor.close()
    conn.close()
    raise ValueError("Missing required parameters (WTC, AT, PT) in input parameters")

# Step 3: Analyze the attendance
def analyze_late_attendance(attendance_data, weeks, threshold, prob_threshold):
    manual_current_date = attendance_data['AttendanceDateTime'].max() 
    print("Manual Current Date:", manual_current_date)
    start_date = manual_current_date - timedelta(days=weeks*7)
    
    # Filter records for the specified period
    relevant_data = attendance_data[(attendance_data['AttendanceDateTime'] >= start_date) & (attendance_data['AttendanceDateTime'] <= manual_current_date)]
    
    if relevant_data.empty:
        print("No attendance data found for the specified period.")
        return pd.DataFrame()  # Return an empty DataFrame if no data is found
    
    # Count the number of late occurrences for each student by day of the week
    relevant_data['Weekday'] = relevant_data['AttendanceDateTime'].dt.day_name()
    late_counts = relevant_data.groupby(['AcademicID', 'Weekday']).size().reset_index(name='LateCount')
    
    # Print the late counts DataFrame
    # print("Late Count Table:")
    # print(late_counts)
    
    # Determine the probability of future lateness
    total_days = (manual_current_date - start_date).days
    late_counts['Probability'] = late_counts['LateCount'] / total_days * 7  # Multiply by 7 to get weekly probability
    
    # Identify frequently late students on specific days
    frequent_offenders = late_counts[(late_counts['LateCount'] > threshold) & (late_counts['Probability'] > prob_threshold)]
    
    return frequent_offenders

# Step 4: Insert analysis results into the existing table
def insert_analysis_results(cursor, analysis_results):
    for row in analysis_results.itertuples(index=False):
        cursor.execute("""
            INSERT INTO analysis_latewise (AcademicID, PredictedLateDay)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE PredictedLateDay = %s;
        """, (row.AcademicID, row.Weekday, row.Weekday))
    
    conn.commit()

# Extract thresholds from input parameters
weeks_to_analyze = int(input_params['WTC'])  # Use the value from input parameters
threshold = int(input_params['AT'])
prob_threshold = float(input_params['PT'])

# Perform the analysis
analysis_results = analyze_late_attendance(attendance_data, weeks_to_analyze, threshold, prob_threshold)

# Insert the analysis results into the existing table
insert_analysis_results(cursor, analysis_results)

# Close the cursor and MySQL connection
cursor.close()
conn.close()

# Print results (for debugging purposes)
print("Analysis Results:")
print(analysis_results)
