import config.globals as globals
from classes import RobotLink

def add_data_to_log_file(data, robot_link_name):
    if data == "":
        return
    file_path = globals.working_dir + f"robot_link_packets/{robot_link_name}.txt"
    with open(file_path, "a") as f:
        f.write(data)
        f.write('\n')

def escape(packet):
    return packet.replace(globals.ESCAPE, globals.ESCAPE + globals.ESCAPE)\
            .replace(globals.START_OF_PACKET, b'\x01' + globals.ESCAPE + b'\x01')\
            .replace(globals.END_OF_PACKET, b'\x02' + globals.ESCAPE + b'\x02')

def unescape(packet):
    return packet.replace(b'\x02' + globals.ESCAPE + b'\x02', globals.END_OF_PACKET)\
            .replace(b'\x01' + globals.ESCAPE + b'\x01', globals.START_OF_PACKET)\
            .replace(globals.ESCAPE + globals.ESCAPE, globals.ESCAPE)

def nested_getattr(obj, attr, default=None):
    attrs = attr.split('.')
    for a in attrs:
        obj = getattr(obj, a, None)
        if obj is None:
            return default
    return obj
