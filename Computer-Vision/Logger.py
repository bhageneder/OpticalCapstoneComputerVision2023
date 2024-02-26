from tkinter import NONE
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

    def __init__(self, logFilepath = None):
        self.logFilepath = self.DEFAULT_LOG_FILE
        self.logger = logger.getLogger(__name__)
       
        
        # Obtain sql database connection
        self.sqliteConnection = self.createDatabaseConnection(self)

        # Add cursor to retrieve data from database using queries
        self.cursor = self.sqliteConnection.cursor()

        # Define the event table
        self.eventTable =  """ CREATE TABLE eventLog(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
            ProcessID INTEGER,
            Tag VARCHAR(10), 
            Module  VARCHAR(10),
            Level INTEGER,
            Message VARCHAR(255),
        )"""

        self.levelTable = """ CREATE TABLE levelTable(
            Level# INTEGER
            Level  VARCHAR(10)
        )"""

    # Logger Class Deconstructor
    def __del__(self):
        print("Commiting changes to Database and Deconstructing Logger")
        
        # Close sql connection 
        self.sqliteConnection.close()

    # Create / open database existing on disk and return database connection
    def createDatabaseConnection(self):
        try:
            # Check if connection exists 
            conn = sqlite3.connect(self.logFilepath)
            return conn
        except sqlite3.Error as sqliteError:
            print("Error connecting to SQLite database at path: {}".format(self.logFilePath))
            print(sqliteError)
            return NONE
        except Exception as e:
            print("FATAL ERROR connecting to database: {e}")
            return NONE
      
    def logSetup(self):
        # Get the process ID and module name
        #pid = os.getpid()
        # Used to store the full path of the script file in the eventTable as a way to identify which script or module inserted a particular log entry
        #modname = __file__ 

        # Export logs to CSV when an instance is created
        csvFilepath = self.export_to_csv()
        logger.INFO('Logs exported to CSV: {csvFilepath}')

        # Execute the tables
        # Use cursor execute to populate all desired data into table
        print("Collected Data: ") # --> not really necessary
        # To select specific column replace * with the column name(s) ('''SELECT * FROM eventTable''')
        event = self.cursor.execute(self.eventTable)
        
        # Set loguru to use SQLite sink
        logger.add(self.logFilepath, table='eventTable', 
                   format=" <ID: {record[id]}> | <Timestamp: {record[timestamp]}> | <Process ID: {record[processID]}> | "
                        "<Tag:{record[tag]}> | <Module: {record[module_name]}> | <Level:{record[level]}>   |" 
                        " |<Message: {record[message]}> ", 
                    level='INFO', enqueue=True, serialize=True)
        # Commit Changes to Database
        self.sqliteConnection.commit()

    def addEvent(self,id, timestamp, pid, tag, module, level, message):
       # instantiantion method detection = logging.getLogger(Detect)

        try:
            self.cursor.execute("INSERT INTO eventTable (id, timestamp, ProcessID, Tag, Module, Level, Message) VALUES (?, ?, ?, ?, ?, ?, ?)", (id, timestamp, pid, tag, module, level, message))
            self.sqliteConnection.commit()

        except Exception as e:
            print("Error inserting log to eventTable: {e}")

            


    def exportCsv(self, csvFilepath):
        try:
            # Retrieve all logs from the database
            self.cursor.execute("SELECT * FROM eventTable")
            self.sqliteConnection.commit()
            rows = self.cursor.fetchall()
            
            # Create a folder for storing CSV files if it doesn't exist
            csvFolder = os.path.join(os.path.dirname(self.logFilepath), self.DEFAULT_CSV_FOLDER)
            os.makedirs(csvFolder, exist_ok=True)

            # Write logs to a CSV file
            with open(csvFilepath, 'w', newline='') as csvFile:
                csvWriter = csv.writer(csvFile)
                header = ["ID", "Timestamp", "Process ID", "Tag", "Module", "Level", "Message"]
                csvWriter.writerow(header)
                csvWriter.writerows(rows) #need to create separate csv for data table 
        
            # Update the database with the CSV file path
            self.cursor.execute("UPDATE eventTable SET csvFilepath = ?", (csvFilepath))
            self.sqliteConnection.commit()

            print("Logs exported to CSV: {csvFilepath}")

            return csvFilepath

        except Exception as e:
            print("Error exporting logs to CSV: {e}")