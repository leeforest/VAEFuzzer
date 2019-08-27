#-*-coding:utf-8-*-
import tensorflow as tf
import numpy as np
from tensorflow.python.keras._impl.keras.datasets.cifar10 import load_data
import os
import cv2
import olefile
import binascii

file1='C:\\Users\\SANS_PC0\\Desktop\\test\\hwp_seeds\\try_7\\m10.hwp'
file2='C:\\Users\\SANS_PC0\\Desktop\\test\\hwp_seeds\\try_7\\m11.hwp'
field1='Scripts/DefaultJScript'
field2='Scripts/JScriptVersion'

def load_data():
		tmp_list=[]	
		hex_content=[]
		total=[]
		hex_arr=[]
		total_list=[]
		total_arr=[]
		
		str=b'6\x19!#f\x15J[S\x03\x15(9\x1bo5N\x06c\x16X\x15b\x13{?V\x11j\x03GLX\x00#\x08m\x006\x00n\x04a12\x00I\x07M\x14e\x01T\tJ\x00)\x0cL\x02[\x12-\x1d\x16 \x0c\x03Q\nG\x04A\x03\x10\x0f-\nM9E\x01F)N\x12C\x00#\x00d\x1d%\x005)\x15:3\x07[\x00>\x19[\x01$\x00P\x0f.\x05^\x16b\x15/\x00Y,\\\x00p\x11>-P\x00^\x00[$A\x00I1c\x16H\x19C\x1c \x00\x1a\x00I\x12oD[M_dv\x1e@\x1b-\x01\x11\t\x03\x00\x00\x00,\x0c\x1a\x0f4\x00T<">5,9-%+\x0f\t\x06\x0e\x15\x1a\x05$\x04\x00.N\x1d p. \x0be62\x0e%\x00\x14\x00F\x17-\nH!%\x00\x15\x00\x06\x00\'\x02\x1b\x00MGg\x00\x1b\x00/0|\x00,!5\x18\x13\x1b\x0b\x00"\x00\x16\x07E2P\x085\x00Q\x1d\x0f\x07\x02\x0f\x11\x0b\x00\x00\x00\x00\x00\x00\x00\x00\xfb\xe1\xe4\xfe'
		ole1=olefile.OleFileIO(file1,write_mode=True)
		stream1=ole1.openstream(field1)
		data1=stream1.read()
		print(data1)

		ole1.write_stream(field1,str)
		stream1=ole1.openstream(field1)
		data1=stream1.read()
		print(data1)
		'''
		string_hex=b'O\x00\x00\x00v\x00a\x00'
		string_hex=binascii.hexlify(string_hex)
		print(string_hex)
		hex_list=[int(string_hex[i:i+2],16) for i in range(0,len(string_hex),2)]
		print(hex_list)
		'''
load_data()

