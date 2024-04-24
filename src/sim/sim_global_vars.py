import threading
import queue

'''
Contains simulator global variables that will be used across all simulator files
'''
def init():
    global IPs
    IPs = [x for x in range(10,245)]

    global usableIPs
    usableIPs = IPs.copy()

    global usedIPs
    usedIPs = list()

    global detectionThreshold
    detectionThreshold = 500

    global commsThreshold
    commsThreshold = 300

    global data_mutex
    data_mutex = threading.Lock()

    global listOfDataQ
    listOfDataQ = []

    # Each robot gets their own data queue
    # can be accessed using the last few digits of their IP (i.e. 10.0.0.XXX) offset by the range (-10)
    for _ in IPs:
        listOfDataQ.append(queue.Queue())
