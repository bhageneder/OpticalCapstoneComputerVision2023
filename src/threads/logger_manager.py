from classes.Logger import Logger
import time
import threading

def logger_manager(): 
    logger = Logger()
    thread_name = threading.current_thread().name
    if g.debug_logger: print(f'{thread_name}: Starting Logger')
    while True:
        logger.cpuData()
        logger.memRAMData()
        logger.memSWAPData()

        logger.diskData()
        logger.interfacesData()
        logger.processesData()
   
        # Not logging ( method call issues)
        #logger.gpuData()
        #logger.memEMCData()
        #logger.memIRAMCData()
        #logger.engData()
        #logger.sensorsData()
        
        time.sleep(30)

