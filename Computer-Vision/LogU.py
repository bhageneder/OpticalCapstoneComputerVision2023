from math import e
import sqlite3
import datetime
import os
import csv
import logging
import psutil


class LogU:
    DEFAULT_DB = 'logU.db'


    def __init__(self, logFilePath = None):
        if logFilePath == None:
           logFilePath = self.DEFAULT_DB

        self.conn = sqlite3.connect(logFilePath)    
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """ CREATE TABLE IF NOT EXISTS eventTable (
                ID INTEGER PRIMARY KEY,
                Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                ProcessID INTEGER,
                Tag VARCHAR(10), 
                Module  VARCHAR(10),
                LevelNum INTEGER,
                Message VARCHAR(255)
            )"""
        )

        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS cpuTable (
                ID INTEGER PRIMARY KEY,
                Utilization DECIMAL(2), 
                Speed DECIMAL(2),
                Processes INTEGER,
                Threads   INTEGER,
                Uptime    TIME(6)
        
            )""" )
        
        # Try to access table
        try:
            # Table already exists
            self.cursor.execute ('''SELECT LevelType FROM levelTable ''')
        except:
            # Table doesn't exist, create and insert data
            self.cursor.execute(""" CREATE TABLE IF NOT EXISTS levelTable (
                LevelType  VARCHAR(10),
                            LevelNum INTEGER
                )""" )
            
            self.cursor.execute('''INSERT OR IGNORE INTO levelTable (LevelType, LevelNum) VALUES ('DEBUG', '0')
                            ''')
            self.cursor.execute('''INSERT OR IGNORE INTO levelTable (LevelType, LevelNum) VALUES ('INFO', '1'), ('WARNING', '2'), 
                            ('ERROR', '3'), ('CRITICAL', '4')''') 
                                                                                 
        self.conn.commit() 

        self.logger = logging.getLogger(__name__) # maybe change to .addEvent for ease
        
    def addEvent(self, tag, module, levelNum, message):
       # instantiantion method detection = logging.getLogger(Detect)
        
     timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
     event = (timestamp, tag, module, levelNum, message)
     self.cursor.execute('''INSERT INTO eventTable (Timestamp, Tag, Module, LevelNum, Message) VALUES (?, ?, ?, ?, ?)''', (event))
     self.conn.commit() 
    def addData(self, utilization, speed, processes, threads, uptime):
        utilization = psutil.cpu_percent()
        speed = psutil.cpu_freq().current
        processes= 0
        for _ in psutil.process_iter():
            processes+= 1

        #avgLoad = psutil.getloadavg() [0]
        threads = psutil.cpu_count(logical=True)
        uptime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%H:%M:%S")
        cpuData = (utilization, speed, processes, threads, uptime)
        self.cursor.execute('''INSERT INTO cpuTable (Utilization, Speed, Processes, Threads, Uptime) VALUES (?, ?, ?, ?, ?)''', (cpuData))
           
        self.conn.commit()

        

    