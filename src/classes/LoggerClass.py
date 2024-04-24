import sqlite3
import datetime
import csv
import logging
import psutil
import os
import time
from jtop import jtop


class Logger:
    DEFAULT_DB = 'logger.db'
    

    def __init__(self, logFilePath = None):
        self.__jetson = jtop()
        self.__jetson.start()

            
        if logFilePath == None:
           logFilePath = self.DEFAULT_DB


        self.conn = sqlite3.connect(logFilePath, check_same_thread = False)    
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
            );"""
        )

        self.cursor.execute(
            """ CREATE TABLE IF NOT EXISTS cpuTable (
                Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                minFreq INTEGER,
                maxFreq   INTEGER,
                currFreq   INTEGER,
                infoFreq VARCHAR(10),
                User FLOAT,
                Nice FLOAT,
                System FLOAT,
                Idle FLOAT
            );""" )
        
        

        try:
            # Table already exists
            self.cursor.execute ('''SELECT LevelType FROM levelTable ''')
        except:    
            self.cursor.execute(""" CREATE TABLE IF NOT EXISTS levelTable (
                LevelType  VARCHAR(10),
                LevelNum INTEGER
                );""" )
        

        self.cursor.execute('''INSERT OR IGNORE INTO levelTable (LevelType, LevelNum) VALUES ('DEBUG', '0'), ('INFO', '1'), ('WARNING', '2'), 
                        ('ERROR', '3'), ('CRITICAL', '4');''') 

    
        self.cursor.execute(
            """ CREATE TABLE IF NOT EXISTS gpuTable (
                Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                Load FLOAT,
                Temp FLOAT,           
                gpuType VARCHAR(10),                        
                memUsed DECIMAL(2),
                minFreq INTEGER,
                maxFreq INTEGER,
                currFreq INTEGER,            
                Uptime VARCHAR(10)
        
            );""" )   
    
       
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS memRAMTable (
                    Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                    Total INTEGER,
                    Used INTEGER,
                    Free INTEGER,
                    Buffers INTEGER,
                    Cached INTEGER,
                    Shared INTEGER
                );''') 

       
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS memSWAPTable (
                    Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                    Total INTEGER,
                    Used INTEGER,
                    Cached INTEGER,
                    Available INTEGER
                );''')

        
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS memEMCTable (
                    Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                    onStatus BOOLEAN,
                    bandwidthUsed INTEGER,
                    minFreq INTEGER,
                    maxFreq INTEGER,
                    currFreq INTEGER
                    
                );''') 
        
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS memIRAMTable (
                    Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                    Total INTEGER,
                    Used INTEGER,
                    freeBlock INTEGER
                );''')
       
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS engineTable (
                    Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                    onStatus BOOLEAN,
                    minFreq INTEGER,
                    maxFreq INTEGER,
                    currentFreq INTEGER
                );''')

 
       
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS diskTable (
                    Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                    Total INTEGER,
                    Available INTEGER,
                    Used INTEGER
                );''')

     
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS interfacesTable (
                    Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                    addressFamily VARCHAR(10),
                    addressType INTEGER,
                    localAddress VARCHAR(50), 
                    remoteAddress VARCHAR(50),
                    tcpStatus VARCHAR(20)
                    
                );''')


       
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS processesTable (
                    Timestamp TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                    processName VARCHAR(10),
                    cpuPercent FLOAT,
                    memRss INTEGER,
                    memVms INTEGER,
                    memShared INTEGER,
                    Priority INTEGER,
                    Status VARCHAR(10),
                    Threads INTEGER
                    
                );''')
        self.conn.commit()
        self.logger = logging.getLogger(__name__)

 

    def addEvent(self, tag, module, levelNum, message):
        # instantiantion method detection = logging.getLogger(Detect)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        event = (timestamp, tag, module, levelNum, message)
        self.cursor.execute('''INSERT INTO eventTable (Timestamp, Tag, Module, LevelNum, Message) VALUES (?, ?, ?, ?, ?);''', (event))
        self.conn.commit()

    def cpuData(self):
        
        cpuInfo = psutil.cpu_freq()
        #onStatus = psutil.cpu_stats().
        #governor = psutil.cpu_freq().
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        minFreq = cpuInfo.min
        maxFreq = cpuInfo.max
        currFreq = cpuInfo.current
        infoFreq = str(cpuInfo.min) + '-' + str(cpuInfo.max)
        cpuTimes = psutil.cpu_times()
        user = cpuTimes.user
        nice = cpuTimes.nice
        system = cpuTimes.system
        idle = cpuTimes.idle
        cpu = (timestamp, minFreq, maxFreq, currFreq, infoFreq, user, nice, system, idle)

        self.cursor.execute('''INSERT INTO cpuTable (Timestamp, minFreq, maxFreq, currFreq, infoFreq, user, nice, system, idle) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''', (cpu))
    
        self.conn.commit() 

    def gpuData(self):
        gpuInfo = self.__jetson.gpu_stats()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        load = gpuInfo['GPU utilization [%]']
        temp = gpuInfo['GPU temperature [°C]']
        gpuType = gpuInfo['GPU type']
        memUsed = gpuInfo['GPU memory used [MB]']
        minFreq = gpuInfo['GPU frequency range [MHz]']['min']
        maxFreq = gpuInfo['GPU frequency range [MHz]']['max']
        currFreq = gpuInfo['GPU frequency [MHz]']
        uptime = gpuInfo['Uptime']
        gpu = (timestamp, load, temp, type, memUsed, minFreq, maxFreq, currFreq, uptime)

        self.cursor.execute('''INSERT INTO gpuTable (Timestamp, Load, Temp, gpuType, memUsed, minFreq, maxFreq, currFreq, Uptime) VALUES (?, ?, ?, ?, ?, ?, ?, ?);''', (gpu))
        
        self.conn.commit()

    def memRAMData(self):
        memInfo = psutil.virtual_memory()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        total = memInfo.total
        used = memInfo.used
        free = memInfo.free
        buffers = memInfo.buffers
        cached = memInfo.cached
        shared = memInfo.shared
        #freeBlock = memInfo.inactive_file
        ram = (timestamp, total, used, free, buffers, cached, shared)
        self.cursor.execute('''INSERT INTO memRAMTable (Timestamp, Total, Used, Free, Buffers, Cached, Shared) VALUES (?, ?, ?, ?, ?, ?, ?);''', (ram))
        
        self.conn.commit()
            

    def memSWAPData(self):
        swapInfo = psutil.swap_memory()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        total = swapInfo.total
        used = swapInfo.used
        cached = swapInfo.sin
        available = swapInfo.free
        swap = (timestamp, total, used, cached, available)
        self.cursor.execute('''INSERT INTO memSWAPTable (Timestamp, Total, Used, Cached, Available) VALUES (?, ?, ?, ?, ?);''',
            (swap))
        
        self.conn.commit()

    def memEMCData(self):
        
        emc = (timestamp, onStatus, bandwidthUsed, minFreq, maxFreq, currFreq) 
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        onStatus = emcInfo['online']
        bandwidthUsed = emcInfo['bandwidth_used']
        minFreq = emcInfo['min_frequency']
        maxFreq = emcInfo['max_frequency']
        currFreq = emcInfo['frequency']
        emcInfo = self.__jetson.stats.mem.gpu.get() 

        self.cursor.execute('''INSERT INTO memEMCTable (Timestamp, onStatus, bandwidthUsed, minFreq, maxFreq, currFreq) VALUES (?, ?, ?, ?, ?, ?);''', (emc))
        
        self.conn.commit()

    def memIRAMData(self):
        
        iram = (timestamp, total, used, freeBlock)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        total = iramInfo['total']
        used = iramInfo['used']
        freeBlock = iramInfo['free']
        iramInfo = self.__jetson.stats.mem.iram.get()       
        self.cursor.execute('''INSERT INTO memIRAMTable (Timestamp, TotalBlock, UsedBlock, FreeBlock) VALUES (?, ?, ?, ?);''', (iram))
    
        self.conn.commit()

    def engData(self):
        engInfo = self.__jetson.stats.gpu.get()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        onStatus = engInfo['online']
        minFreq = engInfo['min_frequency']
        maxFreq = engInfo['max_frequency']
        currFreq = engInfo['frequency']
        eng = (timestamp, onStatus, minFreq, maxFreq, currFreq)

        self.cursor.execute(''' INSERT INTO engineData (Timestamp, OnlineStatus, MinFrequency, MaxFrequency, CurrentFrequency) VALUES (?, ?, ?, ?, ?);''', (eng))
        
        self.conn.commit()

  

    def diskData(self):
        diskInfo = psutil.disk_usage('/')
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        total = diskInfo.total
        available = diskInfo.free
        used  = diskInfo.used
        disk = (timestamp, total, available, used)

        self.cursor.execute('''INSERT INTO diskTable (Timestamp, Total, Available, Used) VALUES (?, ?, ?, ?);''', (disk))
        
        self.conn.commit()
        
    def interfacesData(self):
        netCons = psutil.net_connections(kind='inet')
        
        for conn in netCons:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            addrFamily = conn.family
            localAddr = conn.laddr
            remAddr = conn.raddr
            addrType = conn.type
            localAddrStr = ':'.join(str(x) for x in localAddr)
            remAddrStr = ':'.join(str(x) for x in remAddr)
            
            tcpStatus = conn.status
            network = (timestamp, addrFamily, addrType, localAddrStr, remAddrStr, tcpStatus)
            self.cursor.execute('''INSERT INTO interfacesTable (Timestamp, addressFamily, addressType, localAddress, remoteAddress, tcpStatus) VALUES (?, ?, ?, ?, ?, ?);''',
                        (network))

            
        self.conn.commit()

    def processesData(self):
        
        process = psutil.process_iter()

        for proc in process:
            #pid = proc.pid()
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            procName = proc.name()
            #gpuUsed = stats.processes[pid]['GPU']['usage']
            cpuPercent = proc.cpu_percent()
            memRss = proc.memory_info().rss / (1024 * 1024)  # Convert to MB
            memVms = proc.memory_info().vms
            memShared = proc.memory_info().shared
            priority = proc.nice()
            status = proc.status()
            threads = proc.num_threads()
        #gpuMemUsed = stats.processes[pid]['GPU']['memoryUsed'] / (1024 * 1024)  # Convert to MB
        processes = (timestamp, procName, cpuPercent, memRss, memVms, memShared, priority, status, threads)

        self.cursor.execute('''INSERT INTO processesTable (Timestamp, processName, cpuPercent, memRss, memVms, memShared, Priority, Status, Threads) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                (processes))
        
        self.conn.commit()
        

    def exportCsv(self, tableNames, rows):
        with open(f'{tableName}.csv', 'w', newline='') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow([description[0] for description in self.cursor.description])  # Write headers automatically
            csvWriter.writerows(rows)  

        tableNames = ['addEvent', 'cpuTable', 'gpuTable', 'memRAMTable', 'memSWAPTable', 
            'memEMCTable', 'memIRAMTable', 'engTable', 'sensorsTable', 'diskTable', 'interfaceTable', 'processesTable']

        for tableName in tableNames:
            self.cursor.execute("SELECT * FROM {tableName}")
            rows = self.cursor.fetchall()
            if rows:
                self.exportCsv(tableName, rows)

        self.conn.commit()

        

    def __del__(self):
        self.exportCsv(self.tableName, self.rows)
        self.conn.commit()
        print("Commiting changes to Database and Deconstructing Logger")
        try: 
            self.__jetson.close()
            # Close sql connection 
            self.conn.close()
        except:
            print("Error closing")
 

                                                                            
    
            
            
