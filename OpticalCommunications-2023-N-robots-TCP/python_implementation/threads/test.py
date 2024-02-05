from ReceiveUART import ReceiveUART
import threading

conn = ReceiveUART("/dev/ttyUSB9")

thread = threading.Thread(target=conn.readSerial, daemon=True, name=f"uart")

thread.start()

while True:
	#print(conn.getTransceiver())
	continue