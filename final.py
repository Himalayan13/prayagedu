import pandas as pd
import json
from sqlalchemy import create_engine
from MLTTest_Timewise import load_and_prepare_data as load_and_prepare_data_timewise, train_classifier as train_classifier_timewise, predict_activity
from MLTest_Activitywise import load_and_prepare_data as load_and_prepare_data_actwise, train_classifier as train_classifier_actwise, predict_time_period

def fetch_analysis_inputs():
    # Database connection details
    host = 'localhost'
    database = 'prayagedu'
    user = 'root'
    password = ''

    # Create a connection to the database
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')
    
    # Query to fetch the analysis inputs and type
    query = "SELECT AnalysisInput, AnalysisType FROM analysis_settings_inputs"

    # Read the data into a DataFrame
    df = pd.read_sql(query, engine)

    # Parse JSON strings to extract analysis inputs and types
    analysis_inputs = []
    analysis_types = df['AnalysisType'].tolist()
    for json_string in df['AnalysisInput']:
        try:
            data = json.loads(json_string)
            analysis_inputs.append(data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {str(e)}")

    return analysis_inputs, analysis_types

def fetch_unique_user_ids(engine):
    # Query to fetch unique user IDs from the administration_activity_logs table
    query = "SELECT DISTINCT UserID FROM administration_activity_logs"
    user_ids = pd.read_sql(query, engine)['UserID'].tolist()
    return user_ids

def insert_analysis_data_timewise(engine, user_id, timestamp, predicted_activity):
    # Create a connection to the database
    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()
        # Insert data into analysis_timewise table
        insert_query = """
        INSERT INTO analysis_timewise (UserID, Timestamp, PredictedActivity)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, timestamp, predicted_activity))
        connection.commit()
        print(f"Inserted data for User ID {user_id}, Timestamp '{timestamp}', Predicted Activity '{predicted_activity}' successfully.")
    finally:
        connection.close()

def insert_analysis_data_actwise(engine, user_id, activity, predicted_time_period):
    # Create a connection to the database
    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()
        # Insert data into analysis_activitywise table
        insert_query = """
        INSERT INTO analysis_activitywise (UserID, ActivityName, PreferredActivityTime)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, activity, predicted_time_period))
        connection.commit()
        print(f"Inserted data for User ID {user_id} and Activity '{activity}' successfully.")
    finally:
        connection.close()

def main():
    # Database connection details
    host = 'localhost'
    database = 'prayagedu'
    user = 'root'
    password = ''

    # Create a connection to the database
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')

    try:
        # Fetch all analysis inputs and types from the database
        analysis_inputs, analysis_types = fetch_analysis_inputs()

        # Fetch unique user IDs from the administration_activity_logs table
        user_ids = fetch_unique_user_ids(engine)

        for user_id in user_ids:
            for input_data, analysis_type in zip(analysis_inputs, analysis_types):
                if analysis_type == 'TimeWise':
                    timestamp = input_data.get('Timestamp')

                    if not timestamp:
                        print("No timestamp found in input data.")
                        continue

                    # Load and prepare data for TimeWise analysis
                    X, y, activity_names = load_and_prepare_data_timewise('filtered_result.csv')

                    # Train the classifier for TimeWise analysis
                    model, accuracy, X_train_columns = train_classifier_timewise(X, y)

                    # Predict the activity for the given timestamp
                    predicted_activity = predict_activity(model, X_train_columns, activity_names, user_id, timestamp)
                    print(f"\nPredicted Activity for User ID {user_id} and Timestamp '{timestamp}': {predicted_activity}")

                    # Insert predicted data into analysis_timewise table
                    insert_analysis_data_timewise(engine, user_id, timestamp, predicted_activity)

                elif analysis_type == 'ActivityWise':
                    activity = input_data.get('FrequentActivity')

                    if not activity:
                        print("No activity found in input data.")
                        continue

                    # Load and prepare data for ActivityWise analysis
                    X, y = load_and_prepare_data_actwise('new_filtered_result.csv')

                    # Train the classifier for ActivityWise analysis
                    model, X_train = train_classifier_actwise(X, y)

                    # Predict the time period for the given activity
                    predicted_time_period = predict_time_period(model, X_train, user_id, activity)
                    print(f"\nPredicted Time Period for User ID {user_id} and Activity '{activity}': {predicted_time_period}")

                    # Insert predicted data into analysis_activitywise table
                    insert_analysis_data_actwise(engine, user_id, activity, predicted_time_period)

                else:
                    print(f"Unknown AnalysisType: {analysis_type}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        engine.dispose()  # Dispose of the engine to close all connections

if __name__ == "__main__":
    main()
