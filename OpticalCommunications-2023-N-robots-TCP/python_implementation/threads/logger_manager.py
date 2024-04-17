import threading 
import time
from LogU import LogU


def logger_manager():
    thread_name = threading.current_thread().name
    while True:
        logger = LogU()
        logger.interfacesData('hostname', 'interfaces')
        logger.memEMCData('onStatus', 'bandwidthUsed', 'minFreq', 'maxFreq', 'currFreq')
        logger.gpuData('load', 'temp', 'type', 'memUsed', 'minFreq', 'maxFreq', 'currFreq', 'uptime')



        logger.memIRAMCData('total', 'used', 'freeBlock')
        logger.engData('onStatus', 'minFreq', 'maxFreq', 'currFreq')
        logger.fanData('speed', 'rpm', 'profile', 'governor', 'control')
        logger.diskData('total', 'available', 'used')

        logger.processesData('pid', 'procName', 'gpuUsed', 'cpuPercent', 'memory', 'priority', 'state', 'threads', 'gpuMemUsed')
        logger.cpuData ('minFreq', 'maxFreq', 'currFreq', 'infoFreq', 'user', 'nice', 'system', 'idle')
        logger.memRAMData('total', 'used', 'free', 'buffers', 'cached', 'shared')
        logger.memSWAPData('total', 'used', 'cached', 'available')
        time.sleep(30)
