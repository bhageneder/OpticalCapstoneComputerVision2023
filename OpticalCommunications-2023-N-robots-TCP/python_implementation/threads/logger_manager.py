import threading 
import time
from Logger import Logger


def logger_manager():
    thread_name = threading.current_thread().name
    while True:
        logger = LogU()
        logger.cpuData ('minFreq', 'maxFreq', 'currFreq', 'infoFreq', 'user', 'nice', 'system', 'idle')
        logger.memRAMData('total', 'used', 'free', 'buffers', 'cached', 'shared')
        logger.memSWAPData('total', 'used', 'cached', 'available')
        logger.sensorsData('speed', 'coreName', 'temperature')
        logger.diskData('total', 'available', 'used')
        logger.interfacesData('addrFamily', 'addrType', 'localAddr', 'remAddr', 'tcpStatus')
        logger.processesData('pid', 'procName', 'cpuPercent', 'memRss', 'memVms', 'memShared', 'priority', 'status', 'threads')

        
   
        # Not logging ( method call issues)
       # logger.gpuData('load', 'temp', 'type', 'memUsed', 'minFreq', 'maxFreq', 'currFreq', 'uptime')
       # logger.memEMCData('onStatus', 'bandwidthUsed', 'minFreq', 'maxFreq', 'currFreq')
       #  logger.memIRAMCData('total', 'used', 'freeBlock')
        #logger.engData('onStatus', 'minFreq', 'maxFreq', 'currFreq')

        
        time.sleep(30)
