import struct
import zlib
from io import BytesIO

import olefile

ole = olefile.OleFileIO('test.hwp')
stream = ole.openstream('Section0')
stream = BytesIO(zlib.decompress(stream.read(), -15))
'''
while True:
    header = stream.read(4)
    if not header:
        break

    header = struct.unpack('<I', header)[0]

    tag_id = header & 0x3ff
    level = (header >> 10) & 0x3ff
    size = (header >> 20) & 0xfff
    if size == 0xfff:
        size = struct.unpack('<I', stream.read(4))[0]

    payload = stream.read(size)

    print('Tag ID: %d, Level: %d, Size: %d(bytes)' % (
        tag_id, level, size
    ))

'''
