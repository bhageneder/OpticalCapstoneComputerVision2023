import time
import threading
import config.global_vars as g

def logger_manager():
    logger = g.logger
    thread_name = threading.current_thread().name
    if g.debug_logger: print(f'{thread_name}: Starting Logger')
    while True:
        with g.logger_mutex:
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
    
