import pandas as pd
import json
from sqlalchemy import create_engine
from MLTTest_Timewise import load_and_prepare_data, train_classifier, predict_activity

def fetch_analysis_inputs():
    # Database connection details
    host = 'localhost'
    database = 'prayagedu'
    user = 'root'
    password = ''

    # Create a connection to the database
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')
    
    # Query to fetch the analysis inputs (timestamps)
    query = "SELECT AnalysisInput FROM analysis_settings_inputs"

    # Read the data into a DataFrame
    df = pd.read_sql(query, engine)

    # Parse JSON strings to extract timestamps
    timestamps = []
    for json_string in df['AnalysisInput']:
        try:
            data = json.loads(json_string)
            timestamp = data.get('Timestamp')
            if timestamp:
                timestamps.append(timestamp)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {str(e)}")

    return timestamps

def insert_analysis_data(engine, user_id, timestamp, predicted_activity):
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

def main():
    # Database connection details
    host = 'localhost'
    database = 'prayagedu'
    user = 'root'
    password = ''

    # Create a connection to the database
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')

    try:
        # Fetch all timestamps from the database
        timestamps = fetch_analysis_inputs()

        # Define a predefined user ID
        user_id = 52    

        # Load and prepare data
        X, y, activity_names = load_and_prepare_data('filtered_result.csv')

        # Train the classifier
        model, accuracy, X_train_columns = train_classifier(X, y)

        # Iterate through each fetched timestamp and predict the activity name
        for timestamp in timestamps:
            predicted_activity = predict_activity(model, X_train_columns, activity_names, user_id, timestamp)
            print(f"\nPredicted Activity for User ID {user_id} and Timestamp '{timestamp}': {predicted_activity}")

            # Insert predicted data into analysis_timewise table
            insert_analysis_data(engine, user_id, timestamp, predicted_activity)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        engine.dispose()  # Dispose of the engine to close all connections

if __name__ == "__main__":
    main()
