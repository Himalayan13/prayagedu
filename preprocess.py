# preprocess.py
import fetch
import pandas as pd

def preprocess_data(data):
    """ Preprocess the fetched data """
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(data)
    
    # Indicate that preprocessing has started
    print("Starting preprocessing...")

    # Debugging: print the DataFrame to inspect its structure
    print("Data before preprocessing:")
    print(df.head())  # Print the first few rows to inspect

    # Example preprocessing steps:
    # 1. Handle missing values
    df.fillna({'ActivityName': 'Unknown'}, inplace=True)
    
      
    # 3. Create a new column 'Hour' to indicate the hour of the activity
    df['Hour'] = df['ActivityDateTime'].dt.hour
    
    # 4. Create a new column 'DayOfWeek' to indicate the day of the week of the activity
    df['DayOfWeek'] = df['ActivityDateTime'].dt.dayofweek
    
    # 5. Create a new column 'IsWeekend' to indicate if the activity was on a weekend
    df['IsWeekend'] = df['ActivityDateTime'].apply(lambda x: x.weekday() >= 5)
    
    # Indicate that preprocessing has finished
    print("Preprocessing completed.")

    # Debugging: print the DataFrame after preprocessing
    print("Data after preprocessing:")
    print(df.head())  # Print the first few rows to inspect

    return df

if __name__ == "__main__":
    data = fetch.fetch_users()
    if data:
        processed_data = preprocess_data(data)
        print("Processed data:")
        print(processed_data[['ActivityName', 'UserID', 'Hour', 'DayOfWeek', 'IsWeekend']].head())
    else:
        print("No data fetched")
