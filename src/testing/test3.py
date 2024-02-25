import global_vars as global_vars
import time

global_vars.init()
print('Sending...')

print((global_vars.serial_ports.index(global_vars.serial_ports[7])).to_bytes(1, 'big'))


#globals.serial_ports[1].write(b"hello\n")
# time.sleep(0.2)
# print(globals.serial_ports[2].readline())
# print(globals.serial_ports[0].readline())
# 