
def calculate_checksum_simple(message):
    return sum(message)

def calculate_checksum(message):
    checksum = 0x00
    for byte in message:
        checksum ^= byte
    return checksum


# HEADER_0 = 0xAA
# HEADER_1 = 0x55
# BASE_CONTROL_IDENTIFIER = 0x01
# BASE_CONTROL_LENGTH = 0x04
# ZERO_BYTE = 0x00


# # SETTING FOR NOW
# speed = 0x0A # = 10 in mm/s
# radius = 0x00 # to move straight

# # payload_length = 6 # number of bytes for total payload (calculate this automatically later?)

# payload = bytearray([BASE_CONTROL_IDENTIFIER, BASE_CONTROL_LENGTH, speed, ZERO_BYTE, radius, ZERO_BYTE])
# print(payload)
# payload_length = len(payload)
# message = bytearray([HEADER_0, HEADER_1, payload_length]) + payload
# print(message)

# checksum = calculate_checksum(message[2:]) # [2:] skips the first two bytes in the message, those are not used for checksum
# print(checksum)
# print(hex(checksum))

# checksum = calculate_checksum_simple(message[2:]) # [2:] skips the first two bytes in the message, those are not used for checksum
# print(checksum)
# print(hex(checksum))

# message += checksum.to_bytes(1, byteorder='little')
# print(message)
