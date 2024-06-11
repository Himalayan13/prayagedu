import csv
import mysql.connector
import connect  # Import the connect module

def fetch_users():    
    """ Fetch and return specific columns from the user table """
    connection = connect.connect_to_mysql()
    if connection and connection.is_connected():
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT ActivityName, UserID, ActivityDateTime 
                FROM administration_activity_logs limit 500
            """
            cursor.execute(query)
            records = cursor.fetchall()
            
            # Debugging: print the fetched records
            # print("Fetched records:")
            # for record in records:
            #     print(record)
                
            return records
        except mysql.connector.Error as e:
            print(f"The error '{e}' occurred while fetching data")
            return None
        finally:
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return None

def write_to_csv(data, filename):
    """ Write fetched data to a CSV file """
    if data:
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['ActivityName', 'UserID', 'ActivityDateTime']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            print(f"Data written to '{filename}' successfully")
        except Exception as e:
            print(f"An error occurred while writing to CSV: {e}")

if __name__ == "__main__":
    data = fetch_users()
    if data:
        write_to_csv(data, 'activity_logs.csv')
    else:
        print("No data fetched")
