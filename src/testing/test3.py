import time
import config.global_vars as g

g.init()
print('Sending...')

print((g.serial_ports.index(g.serial_ports[7])).to_bytes(1, 'big'))


#g.serial_ports[1].write(b"hello\n")
# time.sleep(0.2)
# print(g.serial_ports[2].readline())
# print(g.serial_ports[0].readline())
#
