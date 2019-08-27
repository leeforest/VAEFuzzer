from olefile import *
import pwn

ole = OleFileIO("test.hwp")
field=ole.listdir()
#field2=str(field[1])
#print field
fin = ole.openstream('FileHeader')
fout = open('FileHeader', "wb")

while True:
	s = fin.read(100)
	print s
	if not s:
		break
	fout.write(s,b'\xFF\xFF\xFF')
	print '--------------'
	print s




