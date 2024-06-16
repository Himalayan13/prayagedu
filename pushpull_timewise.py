import pandas as pd
import json
from sqlalchemy import create_engine
from dummytestes import load_and_prepare_data, train_classifier, predict_activity_name

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

    # Fetch all timestamps
    timestamps = df['AnalysisInput'].tolist()

    return timestamps

def insert_analysis_data(engine, user_id, timestamp, predicted_activity):
    # Create a connection to the database
    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()
        # Insert data into analysis_activitywise table
        insert_query = """
        INSERT INTO analysis_timewise (UserID, Timestamp, PredActivity)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, timestamp, predicted_activity))
        connection.commit()
        print(f"Inserted data for User ID {user_id}, Timestamp '{timestamp}', Predicted Activity '{predicted_activity}' successfully.")
    finally:
        connection.close()

def main():
    # Fetch all timestamps from the database
    timestamps = fetch_analysis_inputs()

    # Define a predefined user ID
    user_id = 487

    # Load and prepare data
    X, y = load_and_prepare_data('new_filtered_result.csv')

    # Train the classifier
    model, X_train = train_classifier(X, y)

    # Iterate through each timestamp and predict the activity name
    for timestamp in timestamps:
        predicted_activity = predict_activity_name(model, X_train, user_id, timestamp)
        print(f"\nPredicted Activity for User ID {user_id} and Timestamp '{timestamp}': {predicted_activity}")

        # Insert predicted data into analysis_activitywise table
        insert_analysis_data(engine, user_id, timestamp, predicted_activity)

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
