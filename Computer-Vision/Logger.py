
from loguru import logger
import sqlite3
import datetime
import os
import csv
import logging
import psutil


LOGLEVELS = [
    ('DEBUG', 0),
    ('INFO', 1),
    ('WARNING', 2),
    ('ERROR', 3),
    ('CRITICAL', 4)
]

class Logger:
    DEFAULT_LOG_FILE = 'logger.db'
    DEFAULT_CSV_FOLDER = 'csvLogFolder'

    def __init__(self, logFilePath = None):
        self.logFilePath = 'logger.db' or self.DEFAULT_LOG_FILE
        self.logger = logging.getLogger(__name__) # maybe change to .addEvent for ease
        
        # Obtain sql database connection
        self.conn = self.createDatabaseConnection()
        print(self.conn)

        # Add cursor to retrieve data from database using queries
        self.cursor = self.conn.cursor()
    
        self.logSetup()
        
        
    # Logger Class Deconstructor
    def __del__(self):
        print("Commiting changes to Database and Deconstructing Logger")
        
        # Close sql connection 
        self.conn.close()

    # Create / open database existing on disk and return database connection
    def createDatabaseConnection(self):
        try:
            self.conn = sqlite3.connect(self.logFilePath)
            return self.conn
            
        except sqlite3.Error as sqliteError:
            print("Error connecting to SQLite database at path: {}".format(self.logFilePath))
            print(sqliteError)
            return None
        except Exception as e:
            print(e)
            print("FATAL ERROR connecting to database: {e}")
            return None
        
    def createTable(self, tableDefinition):
        try:
            self.cursor()
            self.cursor.execute(tableDefinition)
            self.conn.commit() 

        except sqlite3.Error as sqliteError:
            print(sqliteError)
            print("Error creating table: {sqliteError}")
 
    def tableDefinition(self):
        # Define the tables
        self.eventTable =  """ CREATE TABLE IF NOT EXISTS eventTable (
                ID INTEGER PRIMARY KEY,
                Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                ProcessID INTEGER,
                Tag VARCHAR(10), 
                Module  VARCHAR(10),
                LevelNum INTEGER,
                Message VARCHAR(255)
            )"""

        self.levelTable = """ CREATE TABLE IF NOT EXISTS levelTable (
                Level VARCHAR(10) PRIMARY KEY,
                LevelNum INTEGER 
                
            )"""
        
        #Maybe a float instead for utilization
        self.cpuData =  """ CREATE TABLE IF NOT EXISTS cpuData (
                ID INTEGER PRIMARY KEY,
                Utilization DECIMAL(2), 
                Speed DECIMAL(2),
                Processes INTEGER,
                Threads   INTEGER,
                Uptime    TIME(6)
        
            )"""
        
         
    def populateLevelTable(self):
        self.tableDefinition()
        for Level in LOGLEVELS:
            try:
            
                self.cursor.execute("INSERT OR IGNORE INTO levelTable (Level, LevelNum) VALUES (?, ?)",
                                    (LOGLEVELS))
                self.conn.commit()
            
            except sqlite3.Error as sqliteError:
                print(sqliteError)
                print("Error populating levelTable: {sqliteError}")       
    
    def logSetup(self):
        # Get the process ID and module name
        #pid = os.getpid()
        # Used to store the full path of the script file in the eventTable as a way to identify which script or module inserted a particular log entry
        #modname = __file__ 
        
        # Export logs to CSV  (previous log?)
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
        
        self.setFilePermissions()
        self.tableDefinition()
        #self.createTable(self.eventTable)
        #self.createTable(self.levelTable)
        self.populateLevelTable()
        self.addData()
        #self.createTable(self.cpuData)
        # Commit Changes to Database
        self.conn.commit()

    def addEvent(self, tag, module, LevelNum, message):
       # instantiantion method detection = logging.getLogger(Detect)
        
       try:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            sqlite3.connect(self.DEFAULT_LOG_FILE)
            self.cursor.execute("INSERT INTO eventLog (Timestamp, Tag, Module, LevelNum, Message) VALUES (?, ?, ?, ?, ?)", (timestamp, tag, module, LevelNum, message))
            self.conn.commit()

       except Exception as e:
            print(e)
            print("Error inserting log to eventTable: {e}")
      
    def addData(self):
        utilization = psutil.cpu_percent()
        speed = psutil.cpu_freq().current
        processes= 0
        for _ in psutil.process_iter():
            processes+= 1

        #avgLoad = psutil.getloadavg() [0]
        threads = psutil.cpu_count(logical=True)
        uptime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%H:%M:%S")
        
    def recordData(self, utilization, speed, processes, threads, uptime): 
        try:
            #CPU percent for each core
            self.addData()
            sqlite3.connect(self.DEFAULT_LOG_FILE)
            self.cursor.execute("INSERT INTO cpuData (Utilization, Speed, Processes, Threads, Uptime) VALUES (?, ?, ?, ?, ?)", (utilization, speed, processes, threads, uptime))
            self.conn.commit()   

        except Exception as e: 
            print(e)
            print("Error inserting log to dataTable: {e}")     
            
  

    def exportCsv(self, csvFilePath = 'eventLogs.csv'):
        try:
            # Retrieve all logs from the database
            self.cursor.execute("SELECT * FROM eventLog")
            self.conn.commit()
            rows = self.cursor.fetchall()
            
            # Create a folder for storing CSV files if it doesn't exist
            csvFolder = os.path.join(os.path.dirname(self.logFilePath), self.DEFAULT_CSV_FOLDER)
            os.makedirs(csvFolder, exist_ok=True)

            # Write logs to a CSV file
            with open(csvFilePath, 'w', newline='') as csvFilePath:
                csvWriter = csv.writer(csvFilePath)
                header = ["ID", "Timestamp", "Process ID", "Tag", "Module", "Level", "Message"]
                csvWriter.writerow(header)
                csvWriter.writerows(rows) 
        
            # Update the database
            self.conn.commit()

            print("Logs exported to CSV: {csvFilePath}")

            return csvFilePath

        except Exception as e:
            print(e)
            print("Error exporting logs to CSV: {e}") #eventually change to self.logger.error

    def setFilePermissions(self):
        # Grant all privileges to all users on the file
        os.chmod(self.logFilePath, 0o777)