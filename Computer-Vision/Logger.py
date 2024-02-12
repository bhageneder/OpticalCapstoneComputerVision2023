from loguru import logger
import sqlite3
from datetime import datetime
import os


class Logger:
    DEFAULT_LOG_FILE_PATH = 'logger.db'
    def __init__(self, log_file_path = None):
        self.log_file_path = self.DEFAULT_LOG_FILE_PATH

        
        # Check if the database file exists, if not, create it
        if not os.path.exists(self.log_file_path):
            if self.create_database():
                print("Database Created Successfully: {self.log_file_path}")
            else:
                print("Database Creation Failed: {self.log_file_path}")

    # Set loguru to use SQLite sink
        logger.add(self.log_file_path, table='log_table', 
                   format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | <ID: {record[id]}> | "
                        "<Timestamp: {record[timestamp]}> | <Process ID: {record[process_id]}> | " 
                        "<Module: {record[module_name]}> | <Category: {record[category]}> | " 
                        "<Message: {record[message]}>", 
                    level='INFO', enqueue=True, serialize=True)
        
        # Create / open database existing on disk
        self.sqliteConnection = sqlite3.connect(self.log_file_path)
        # Add cursor to retrieve data from database using queries
        self.cursor = self.sqliteConnection.cursor()
        
        # Define the table
        log_table = ''' Create Table event_Log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            time TEXT,
            level TEXT,
            process_id INTEGER,
            module_name TEXT,
            category TEXT,
            message TEXT
        )'''
        
        # Get the process ID and module name
        pid = os.getpid()
        # Used to store the full path of the script file in the log_table as a way to identify which script or module inserted a particular log entry
        modname = __file__ 

        # Execute the table 
        # Use cursor execute to populate all desired data into table
        print("Collected Data: ") # --> not really necessary
        # To select specific column replace * with the column name(s) ('''SELECT * FROM log_table''')
        events = self.cursor.execute(log_table)
       
    
    def create_database(self):
        try:
            # Create an empty database file if it doesn't exist
            with open(self.log_file_path, 'w'):
                pass
            return True
        except Exception as e:
            print("Error creating database: {e}")
            return False


    # Commit Changes to Database
    def close_connection(self):        
        self.sqliteConnection.commit()
    # Close SQL connection
        self.sqliteConnection.close()