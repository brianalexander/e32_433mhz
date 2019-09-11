from ..message import Message
from ..message import OP_TO_FMT_STR

from struct import unpack

message = Message(op_code=2, data=[11, 12, 13, 14, 15])

msg_built = message.bytes

print(len(msg_built))
print(msg_built)
op_code, length, one, two, three, four, five, checksum = unpack(
    '! 2B 5I B', msg_built)

print(type(checksum))
print(checksum)
print(op_code ^ length ^ one ^ two ^ three ^ four ^ five ^ checksum)
