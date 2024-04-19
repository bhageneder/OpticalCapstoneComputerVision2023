from Logger import Logger
import time

def logger_manager(): 
    logger = Logger()
    #thread_name = threading.current_thread().name
    while True:
        logger.cpuData()
        logger.memRAMData()
        logger.memSWAPData()
        #logger.sensorsData()
        logger.diskData()
        logger.interfacesData()
        logger.processesData()
   
        # Not logging ( method call issues)
       # logger.gpuData()
       # logger.memEMCData()
       #  logger.memIRAMCData()
        #logger.engData()

        
        time.sleep(30)

