import config.global_vars as g

def add_data_to_log_file(data, robot_link_name):
    if data == "":
        return
    file_path = g.working_dir + f"robot_link_packets/{robot_link_name}.txt"
    with open(file_path, "a") as f:
        f.write(data)
        f.write('\n')

def escape(packet):
    return packet.replace(g.ESCAPE, g.ESCAPE + g.ESCAPE)\
            .replace(g.START_OF_PACKET, b'\x01' + g.ESCAPE + b'\x01')\
            .replace(g.END_OF_PACKET, b'\x02' + g.ESCAPE + b'\x02')

def unescape(packet):
    return packet.replace(b'\x02' + g.ESCAPE + b'\x02', g.END_OF_PACKET)\
            .replace(b'\x01' + g.ESCAPE + b'\x01', g.START_OF_PACKET)\
            .replace(g.ESCAPE + g.ESCAPE, g.ESCAPE)

def nested_getattr(obj, attr, default=None):
    attrs = attr.split('.')
    for a in attrs:
        obj = getattr(obj, a, None)
        if obj is None:
            return default
    return obj
