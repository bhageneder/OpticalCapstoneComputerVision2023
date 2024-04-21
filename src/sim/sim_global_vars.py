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