import config.globals as globals
import time

globals.init()
print('Sending...')

print((globals.serial_ports.index(globals.serial_ports[7])).to_bytes(1, 'big'))


#globals.serial_ports[1].write(b"hello\n")
# time.sleep(0.2)
# print(globals.serial_ports[2].readline())
# print(globals.serial_ports[0].readline())
# 