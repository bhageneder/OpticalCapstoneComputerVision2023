
from loguru import logger
import sqlite3
from datetime import datetime
import os
import csv
import logging
from enum import Enum

class Level(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

class Logger:
    DEFAULT_LOG_FILE = 'logger.db'
    DEFAULT_CSV_FOLDER = 'csvFolder.csv'

    def __init__(self, logFilePath = None):
        self.logFilePath = 'logger.db' or self.DEFAULT_LOG_FILE
        self.logger = logging.getLogger(__name__)
        
        # Obtain sql database connection
        self.sqliteConnection = self.createDatabaseConnection()
        print(self.sqliteConnection)

        # Add cursor to retrieve data from database using queries
        self.cursor = self.sqliteConnection.cursor()

    # Logger Class Deconstructor
    def __del__(self):
        print("Commiting changes to Database and Deconstructing Logger")
        
        # Close sql connection 
        self.sqliteConnection.close()

    # Create / open database existing on disk and return database connection
    def createDatabaseConnection(self):
        try:
            self.conn = sqlite3.connect(self.logFilePath)
            #conn.row = sqlite3.Row #to access column by name
            return self.conn
    
            #conn.row = sqlite3.Row #to access column by name
            
        except sqlite3.Error as sqliteError:
            print("Error connecting to SQLite database at path: {}".format(self.logFilePath))
            print(sqliteError)
            return None
        except Exception as e:
            print("FATAL ERROR connecting to database: {e}")
            return None
        
    def createTable(self, tableDefinition):
        try:
            self.conn.cursor()
            self.conn.execute(tableDefinition)
            self.sqliteConnection.commit()
        except sqlite3.Error as sqliteError:
            print("Error creating table: {sqliteError}")
 
    def tableDefinition(self):
        # Define the event table
        self.eventTable =  """ CREATE TABLE IF NOT EXISTS eventLog (
                ID INTEGER PRIMARY KEY,
                Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                ProcessID INTEGER,
                Tag VARCHAR(10), 
                Module  VARCHAR(10),
                LevelNum INTEGER,
                Message VARCHAR(255)
            )"""

        self.levelTable = """ CREATE TABLE IF NOT EXISTS levelTable (
                LevelNum INTEGER PRIMARY KEY,
                Level VARCHAR(10)
            )"""
        print(self.levelTable)
        #self.conn = createDatabaseConnection()
        self.logSetup()
    def populateLevelTable(self):
        try:
            for level in Level:
                self.cursor.execute("INSERT OR IGNORE INTO levelTable (LevelNum, Level) VALUES (?, ?)",
                                    (level.value, level.name))
            self.sqliteConnection.commit()
        except sqlite3.Error as sqliteError:
            print("Error populating levelTable: {sqliteError}")       
    
    def logSetup(self):
        # Get the process ID and module name
        #pid = os.getpid()
        # Used to store the full path of the script file in the eventTable as a way to identify which script or module inserted a particular log entry
        #modname = __file__ 
        
        # Export logs to CSV when an instance is created (previous log?)
        csvFilePath = self.exportCsv()
        self.logger.info('Logs exported to CSV: {csvFilePath}')

        # Execute the tables
        # Use cursor execute to populate all desired data into table
        print("Current Tables: ") # --> not really necessary
        # To select specific column replace * with the column name(s) ('''SELECT * FROM eventTable''')
        
        # Set loguru to use SQLite sink
        logger.add(self.logFilePath, serialize=True,
                   format = " <ID: {record[id]}> | <Timestamp: {record[timestamp]}> | <Process ID: {record[processID]}> | "
                        "<Tag:{record[tag]}> | <Module: {record[module]}> | <Level:{record[level]}>   |" 
                        " |<Message: {record[message]}> ", 
                    enqueue=True)
        # Commit Changes to Database
        self.sqliteConnection.commit()

    def addEvent(self, tag, module, LevelNum, message):
       # instantiantion method detection = logging.getLogger(Detect)
        
       try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            sqlite3.connect(self.DEFAULT_LOG_FILE)
            self.cursor.execute("INSERT INTO eventLog (Timestamp, Tag, Module, LevelNum, Message) VALUES (?, ?, ?, ?, ?)", (timestamp, tag, module, LevelNum, message))
            self.sqliteConnection.commit()

       except Exception as e:
            print("Error inserting log to eventTable: {e}")
        
            


    def exportCsv(self, csvFilePath = 'eventLogs.csv'):
        try:
            # Retrieve all logs from the database
            self.cursor.execute("SELECT * FROM eventTable")
            self.sqliteConnection.commit()
            rows = self.cursor.fetchall()
            
            # Create a folder for storing CSV files if it doesn't exist
            csvFolder = os.path.join(os.path.dirname(self.logFilePath), self.DEFAULT_CSV_FOLDER)
            os.makedirs(csvFolder, exist_ok=True)

            # Write logs to a CSV file
            with open(csvFilePath, 'w', newline='') as csvFile:
                csvWriter = csv.writer(csvFilePath)
                header = ["ID", "Timestamp", "Process ID", "Tag", "Module", "Level", "Message"]
                csvWriter.writerow(header)
                csvWriter.writerows(rows) 
        
            # Update the database with the CSV file path
            self.cursor.execute("UPDATE eventTable SET csvFilePath = ?", (csvFilePath))
            self.sqliteConnection.commit()

            print("Logs exported to CSV: {csvFilePath}")

            return csvFilePath

        except Exception as e:
            print("Error exporting logs to CSV: {e}") #eventually change to self.logger.error
