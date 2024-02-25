from config.global_vars import global_vars

def add_data_to_log_file(data, robot_link_name):
    if data == "":
        return
    file_path = global_vars.working_dir + f"robot_link_packets/{robot_link_name}.txt"
    with open(file_path, "a") as f:
        f.write(data)
        f.write('\n')

def escape(packet):
    return packet.replace(global_vars.ESCAPE, global_vars.ESCAPE + global_vars.ESCAPE)\
            .replace(global_vars.START_OF_PACKET, b'\x01' + global_vars.ESCAPE + b'\x01')\
            .replace(global_vars.END_OF_PACKET, b'\x02' + global_vars.ESCAPE + b'\x02')

def unescape(packet):
    return packet.replace(b'\x02' + global_vars.ESCAPE + b'\x02', global_vars.END_OF_PACKET)\
            .replace(b'\x01' + global_vars.ESCAPE + b'\x01', global_vars.START_OF_PACKET)\
            .replace(global_vars.ESCAPE + global_vars.ESCAPE, global_vars.ESCAPE)

def nested_getattr(obj, attr, default=None):
    attrs = attr.split('.')
    for a in attrs:
        obj = getattr(obj, a, None)
        if obj is None:
            return default
    return obj
