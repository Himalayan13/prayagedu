# main.py
import pandas as pd
import json
from sqlalchemy import create_engine
from ml_try import load_and_prepare_data, train_classifier, predict_time_period

def fetch_analysis_inputs():
    # Database connection details
    host = 'localhost'
    database = 'prayagedu'
    user = 'root'
    password = ''

    # Create a connection to the database
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')
    
    # Query to fetch the analysis inputs
    query = "SELECT AnalysisInput FROM analysis_settings_inputs"

    # Read the data into a DataFrame
    df = pd.read_sql(query, engine)

    # Fetch all activity names
    df['AnalysisInput'] = df['AnalysisInput'].apply(json.loads)
    activities = df['AnalysisInput'].apply(lambda x: x['FrequentActivity']).tolist()

    return activities

def insert_analysis_data(engine, user_id, activity, predicted_time_period):
    # Create a connection to the database
    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()
        # Insert data into analysis_activitywise table
        insert_query = """
        INSERT INTO analysis_activitywise (UserID, ActivityName,PreferredActivityTime)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, activity, predicted_time_period))
        connection.commit()
        print(f"Inserted data for User ID {user_id} and Activity '{activity}' successfully.")
    finally:
        connection.close()

def main():
    # Fetch all activities from the database
    activities = fetch_analysis_inputs()

    # Define a predefined user ID
    user_id = 487

    # Load and prepare data
    X, y = load_and_prepare_data('new_filtered_result.csv')

    # Train the classifier
    model, X_train = train_classifier(X, y)

    # Iterate through each activity and predict the time period
    for activity in activities:
        predicted_time_period = predict_time_period(model, X_train, user_id, activity)
        print(f"\nPredicted Time Period for User ID {user_id} and Activity '{activity}': {predicted_time_period}")

        # Insert predicted data into analysis_activitywise table
        insert_analysis_data(engine, user_id, activity, predicted_time_period)

if __name__ == "__main__":
    # Database connection details
    host = 'localhost'
    database = 'prayagedu'
    user = 'root'
    password = ''

    # Create a connection to the database
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')

    # Execute main function
    main()
