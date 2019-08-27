#-*-coding:utf-8-*-
#잘덮어씌어짐~~~

from multiprocessing import *
from pwn import *
import olefile
import logging
import commands
import psutil
import random
import sys
import threading
import os
import time
import re

ole = olefile.OleFileIO('test2.hwp', write_mode=True)
stream1 = ole.openstream('FileHeader')
stream2 = ole.openstream('BodyText/Section0')

data1=stream1.read()
print hexdump(data1)
print '\n\n'
print len(data1)
#data1=data1+data1
#data2=stream2.read()
#print '\n\n'
print len(data1)
#print hexdump(data1)
print '\n\n'
#print hexdump(data2)
#print ole.get_size('FileHeader')

stream1.seek(0)
stream2.seek(0)
#data1=stream1.read(10)
data1=data1*5
print len(data1)
data2=stream2.read(256)
#print hexdump(data)

ole.write_stream('FileHeader', data2)
#print hexdump(data1)
ole.close()

