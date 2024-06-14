# connect.py
import mysql.connector

def connect_to_mysql():
    """ Connect to MySQL database and test the connection """
    try:
        connection = mysql.connector.connect(
            host='localhost',          
            database='prayagedu',     
            user='root',               
            password=''               
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Successfully connected to MySQL Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("Connected to database: ", record)
            return connection

    except mysql.connector.Error as e:
        print("Error while connecting to MySQL", e)
        return None
    finally:
        pass

