from LogU import LogU


logger = LogU()
logger.addEvent('transceiverID', 'detector', '1', 'tester') 
logger.cpuData ('minFreq', 'maxFreq', 'currFreq', 'infoFreq', 'user', 'nice', 'system', 'idle')
logger.gpuData('load', 'temp', 'type', 'memUsed', 'minFreq', 'maxFreq', 'currFreq', 'uptime')
logger.memRAMData('total', 'used', 'free', 'buffers', 'cached', 'shared', 'freeBlock')
logger.memSWAPData('total', 'used', 'cached', 'available')
logger.memEMCData('onStatus', 'bandwidthUsed', 'minFreq', 'maxFreq', 'currFreq')
logger.memIRAMCData('total', 'used', 'freeBlock')
logger.engData('onStatus', 'minFreq', 'maxFreq', 'currFreq')
logger.fanData('speed', 'rpm', 'profile', 'governor', 'control')
logger.diskData('total', 'available', 'used')
logger.interfacesData('hostname', 'interfaces')
logger.processesData('pid', 'procName', 'gpuUsed', 'cpuPercent', 'memory', 'priority', 'state', 'threads', 'gpuMemUsed')
