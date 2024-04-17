from LogU import LogU

while True:
    logger = LogU()
    logger.addEvent('transceiverID', 'detector', '1', 'tester') 
    logger.interfacesData('addrFamily', 'addrType', 'localAddr', 'remAddr', 'tcpStatus')
    logger.memEMCData('onStatus', 'bandwidthUsed', 'minFreq', 'maxFreq', 'currFreq')
    logger.gpuData('load', 'temp', 'type', 'memUsed', 'minFreq', 'maxFreq', 'currFreq', 'uptime')



    logger.memIRAMCData('total', 'used', 'freeBlock')
    logger.engData('onStatus', 'minFreq', 'maxFreq', 'currFreq')
    logger.sensorsData('speed', 'coreName', 'temperature')
    logger.diskData('total', 'available', 'used')

    logger.processesData('pid', 'procName', 'cpuPercent', 'memRss', 'memVms', 'memShared', 'priority', 'status', 'threads')
    logger.cpuData ('minFreq', 'maxFreq', 'currFreq', 'infoFreq', 'user', 'nice', 'system', 'idle')
    logger.memRAMData('total', 'used', 'free', 'buffers', 'cached', 'shared')
    logger.memSWAPData('total', 'used', 'cached', 'available')
