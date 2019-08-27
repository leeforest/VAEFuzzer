
from collections import namedtuple
from struct import unpack

file_header_path = r"FileHeader.dmp"
data = file('/home/forest/fuzzer/hwp/test.hwp', "rb").read()

HEADER_MEMBER_NAME = ("Signature Version Flag Reserved")
HEADER_MEMBER_SIZE = "=32s2l216s"
file_header = namedtuple("FileHeader", HEADER_MEMBER_NAME)._make(unpack(HEADER_MEMBER_SIZE, data))
print file_header.Signature
print file_header.Flag
