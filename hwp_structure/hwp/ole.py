import olefile
import os
from pwn import *
import sys

filename=sys.argv[1]

hwp_field_size={}
ole=olefile.OleFileIO(filename,write_mode=True)
hwp_field=ole.listdir()

for i in range(len(hwp_field)):
	field=hwp_field[i]
	field_size=ole.get_size(hwp_field[i])
	print field, field_size

	if len(field)>1:
		storage=field[0]
		stream=field[1]
		field=str(storage+'/'+stream)
		hwp_field_size[field]=field_size

	else:
		field=str(field[0])
		hwp_field_size[field]=field_size

stream = ole.openstream(fieldname)
data = stream.read()
print hexdump(data)

'''
print '\n'
stream.seek(10)
data=stream.read(ole.get_size('FIleHeader'))
print hexdump(stream)
#ole.write_stream('FileHeader',data)
#print hexdump(stream)
'''
