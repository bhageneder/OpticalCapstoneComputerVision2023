import sqlite3
import datetime
import time
import os
import csv
import logging
import psutil
from jtop import jtop

import socket


class LogU:
    DEFAULT_DB = 'logU.db'


    def __init__(self, logFilePath = None):
        self.__jetson = jtop()
        self.__jetson.start()

            
        if logFilePath == None:
           logFilePath = self.DEFAULT_DB

        self.conn = sqlite3.connect(logFilePath)    
        self.cursor = self.conn.cursor()

        self.conn.commit() 

    
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

        self.cursor.execute(
            """ CREATE TABLE IF NOT EXISTS cpuTable (
                ID INTEGER PRIMARY KEY,
                minFreq INTEGER,
                maxFreq   INTEGER,
                currFreq   INTEGER,
                infoFreq VARCHAR(10),
                User FLOAT,
                Nice FLOAT,
                System FLOAT,
                Idle FLOAT
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

        self.cursor.execute(
            """ CREATE TABLE IF NOT EXISTS gpuTable (
                ID INTEGER PRIMARY KEY,
                Load FLOAT,
                Temp FLOAT,           
                gpuType VARCHAR(10),                        
                memUsed DECIMAL(2),
                minFreq INTEGER,
                maxFreq INTEGER,
                currFreq INTEGER,            
                Uptime VARCHAR(10)
        
            )""" )   

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS memRAMTable (
                    ID INTEGER PRIMARY KEY,
                    Total INTEGER,
                    Used INTEGER,
                    Free INTEGER,
                    Buffers INTEGER,
                    Cached INTEGER,
                    Shared INTEGER,
                    freeBlock INTEGER
                )''')  

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS memSWAPTable (
                    ID INTEGER PRIMARY KEY,
                    Total INTEGER,
                    Used INTEGER,
                    Cached INTEGER,
                    Available INTEGER
                )''')

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS memEMCTable (
                    ID INTEGER PRIMARY KEY,
                    onStatus BOOLEAN,
                    bandwidthUsed INTEGER,
                    minFreq INTEGER,
                    maxFreq INTEGER,
                    currFreq INTEGER
                    
                )''') 
        
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS memIRAMTable (
                    ID INTEGER PRIMARY KEY,
                    Total INTEGER,
                    Used INTEGER,
                    freeBlock INTEGER
                )''')
        
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS engineTable (
                    ID INTEGER PRIMARY KEY,
                    onStatus BOOLEAN,
                    minFreq INTEGER,
                    maxFreq INTEGER,
                    currentFreq INTEGER
                )''')
        
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS fanTable (
                    ID INTEGER PRIMARY KEY,
                    Speed INTEGER,
                    RPM INTEGER,
                    Profile VARCHAR(10),
                    Governor VARCHAR(10),
                    Control VARCHAR(10)
                )''')
        
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS diskTable (
                    ID INTEGER PRIMARY KEY,
                    Total INTEGER,
                    Available INTEGER,
                    Used INTEGER
                )''')
        
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS interfacesTable (
                    ID INTEGER PRIMARY KEY,
                    Hostname VARCHAR(10),
                    Interface VARCHAR(20)
                )''')

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS processesTable (
                    ID INTEGER PRIMARY KEY,
                    PID INTEGER,
                    gpuUsed VARCHAR(10),
                    Priority INTEGER,
                    State VARCHAR(10),
                    Processes INTEGER,
                    cpuPercent FLOAT,
                    memUsed INTEGER,
                    gpuMemUsed INTEGER,
                    processName VARCHAR(10)
                )''')
        
        self.conn.commit()

        self.logger = logging.getLogger(__name__)
 

    def addEvent(self, tag, module, levelNum, message):
        # instantiantion method detection = logging.getLogger(Detect)
        
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            event = (timestamp, tag, module, levelNum, message)
            self.cursor.execute('''INSERT INTO eventTable (Timestamp, Tag, Module, LevelNum, Message) VALUES (?, ?, ?, ?, ?)''', (event))
            self.conn.commit()

    def cpuData(self, minFreq, maxFreq, currFreq, infoFreq, user, nice, system, idle):
            while True:
                cpu = (minFreq, maxFreq, currFreq, infoFreq, user, nice, system, idle)
                cpuInfo = psutil.cpu_freq()
                #onStatus = psutil.cpu_stats().
                #governor = psutil.cpu_freq().
                minFreq = cpuInfo.min
                maxFreq = cpuInfo.max
                currFreq = cpuInfo.current
                infoFreq = str(cpuInfo.min) + '-' + str(cpuInfo.max)
                cpuTimes = psutil.cpu_times()
                user = cpuTimes.user
                nice = cpuTimes.nice
                system = cpuTimes.system
                idle = cpuTimes.idle
        
                self.cursor.execute('''INSERT INTO cpuTable (minFreq, maxFreq, currFreq, infoFreq, user, nice, system, idle) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (cpu))
            
                time.sleep(30)
                self.conn.commit() 

    def gpuData(self, load, temp, type, memUsed, minFreq, maxFreq, currFreq, uptime):
            while True:
                gpuInfo = self.__jetson.gpu_stats()
                gpu = (load, temp, type, memUsed, minFreq, maxFreq, currFreq, uptime)
                load = gpuInfo['GPU utilization [%]']
                temp = gpuInfo['GPU temperature [°C]']
                gpuType = gpuInfo['GPU type']
                memUsed = gpuInfo['GPU memory used [MB]']
                minFreq = gpuInfo['GPU frequency range [MHz]']['min']
                maxFreq = gpuInfo['GPU frequency range [MHz]']['max']
                currFreq = gpuInfo['GPU frequency [MHz]']
                uptime = gpuInfo['Uptime']
                self.cursor.execute('''INSERT INTO gpuTable (Load, Temp, gpuType, memUsed, minFreq, maxFreq, currFreq, Uptime) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (gpu))
                
                time.sleep(30)
                self.conn.commit()

    def memRAMData(self, total, used, free, buffers, cached, shared, freeBlock):
            while True:
                memInfo = psutil.virtual_memory()
                ram = (total, used, free, buffers, cached, shared, freeBlock)
                total = memInfo.total
                used = memInfo.used
                free = memInfo.free
                buffers = memInfo.buffers
                cached = memInfo.cached
                shared = memInfo.shared
                #freeBlock = memInfo.inactive_file

                self.cursor.execute('''INSERT INTO memRAMTable (Total, Used, Free, Buffers, Cached, Shared) VALUES (?, ?, ?, ?, ?, ?)''', (ram))
                
                time.sleep(30)
                self.conn.commit()
            

    def memSWAPData(self, total, used, cached, available):
            while True:
                swapInfo = psutil.swap_memory()
                swap = (total, used, cached, available)
                total = swapInfo.total
                used = swapInfo.used
                cached = swapInfo.sin
                available = swapInfo.free

                self.cursor.execute('''INSERT INTO memSWAPTable (Total, Used, Cached, Available) VALUES (?, ?, ?, ?)''',
                    (swap))
                
                time.sleep(30)
                self.conn.commit()

    def memEMCData(self, onStatus, bandwidthUsed, minFreq, maxFreq, currFreq):
            while True:
                emcInfo = self.__jetson.stats.mem.gpu.get() 
                emc = (onStatus, bandwidthUsed, minFreq, maxFreq, currFreq) 
                onStatus = emcInfo['online']
                bandwidthUsed = emcInfo['bandwidth_used']
                minFreq = emcInfo['min_frequency']
                maxFreq = emcInfo['max_frequency']
                currFreq = emcInfo['frequency']

                self.cursor.execute("INSERT INTO memEMCTable (onStatus, bandwidthUsed, minFreq, maxFreq, currFreq) VALUES (?, ?, ?, ?, ?)", (emc))
                
                time.sleep(30)
                self.conn.commit()

    def memIRAMData(self, total, used, freeBlock):
            while True:
                iramInfo = self.__jetson.stats.mem.iram.get()
                iram = (total, used, freeBlock)
                total = iramInfo['total']
                used = iramInfo['used']
                freeBlock = iramInfo['free']

                self.cursor.execute('''INSERT INTO memIRAMTable (TotalBlock, UsedBlock, FreeBlock) VALUES (?, ?, ?)''', (iram))
            
            
                time.sleep(30)
                self.conn.commit()

    def engData(self, onStatus, minFreq, maxFreq, currFreq):
            while True:
                engInfo = self.__jetson.stats.gpu.get()
                eng = (onStatus, minFreq, maxFreq, currFreq)
                onStatus = engInfo['online']
                minFreq = engInfo['min_frequency']
                maxFreq = engInfo['max_frequency']
                currFreq = engInfo['frequency']

                self.cursor.execute(''' INSERT INTO engineData (OnlineStatus, MinFrequency, MaxFrequency, CurrentFrequency) VALUES (?, ?, ?, ?)''', (eng))
                
                time.sleep(30)
                self.conn.commit()

    def fanData(self, speed, rpm, profile, governor, control):
            while True:
                fanInfo = self.__jetson.stats.fan.get()
                fan = (speed, rpm, profile, governor, control)
                speed = fanInfo['speed']
                rpm = fanInfo['rpm']
                profile = fanInfo['profile']
                governor = fanInfo['governor']
                control = fanInfo['control']

                self.cursor.execute('''INSERT INTO fanTable (Speed, RPM, Profile, Governor, Control) VALUES (?, ?, ?, ?, ?)''', (fan))   
                
                time.sleep(30)
                self.conn.commit()

    def diskData(self, total, available, used):
            while True:
                diskInfo = psutil.disk_usage('/')
                disk = (total, available, used)
                total = diskInfo.total
                available = diskInfo.free
                used  = diskInfo.used

                self.cursor.execute('''INSERT INTO diskTable (Total, Available, Used) VALUES (?, ?, ?)''', (disk))
                
                time.sleep(30)
                self.conn.commit()
        
    def interfacesData(self, hostname, interfaces):
            while True:
                hostname = socket.gethostname()
                interfaces = [iface[1]['addr'] for iface in socket.if_nameindex()]
            
                for interface in interfaces:
                    self.cursor.execute('''INSERT INTO localInterfaces (Hostname, Interface) VALUES (?, ?)''',
                        (hostname, interface))

            
                time.sleep(30)
                self.conn.commit()

    def processesData(self, pid, procName, gpuUsed, cpuPercent, memory, priority, state, threads, gpuMemUsed):
            stats = self.__jetson.stats
            processesInfo = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'num_threads', 'nice', 'memory_percent', 'status'])
            processes = (pid, procName, gpuUsed, cpuPercent, memory, priority, state, threads, gpuMemUsed)
            for process in processesInfo:
                pid = process.info['pid']
                procName = process.info['name']
                gpuUsed = stats.processes[pid]['GPU']['usage']
                cpuPercent = process.info['cpu_percent']
                memory_info = process.info['memory_info']
                memory = memory_info.rss / (1024 * 1024)  # Convert to MB
                priority = process.info['nice']
                state = process.info['status']
                threads = process.info['num_threads']
                gpuMemUsed = stats.processes[pid]['GPU']['memoryUsed'] / (1024 * 1024)  # Convert to MB
            

                self.cursor.execute('''INSERT INTO processes (PID, gpuUsed, Priority, State, Processes, cpuPercent, memUsed, gpuMemUsed, processName) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (processes))
        

    def exportCsv(self, tableName, rows):
            with open('{table_name}.csv', 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([description[0] for description in self.cursor.description])  # Write headers automatically
                csv_writer.writerows(rows)  

            tableNames = ['addEvent', 'cpuTable', 'gputale', 'memRAMTable', 'memSWAPTable', 
                'memEMCTable', 'memIRAMCTable', 'engTable', 'fanTable', 'diskTable', 'interfaceTable', 'processesTable']

            for tableName in tableNames:
                self.cursor.execute("SELECT * FROM {tableName}")
                rows = self.cursor.fetchall()
                if rows:
                    self.exportCsv(tableName, rows)

    def __del__(self):
            print("Commiting changes to Database and Deconstructing Logger")
            self.__jetson.close()
            # Close sql connection 
            self.conn.close() 
                                                                            
    
            
            