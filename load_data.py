#-*- coding: utf-8 -*-
import os
import olefile
import numpy as np
import binascii

root_dir='C:\\Users\\SANS_PC0\\Desktop\\test\\'
dir_list=os.listdir(root_dir)
file_num=1000
perc=int(file_num*0.1)
field='BinData/BIN0005.bmp'
field_size=101430 #BinData/BIN0005.bmp

class HWP:
	
	def __init__(self):
		
		self.index_cov_dict={}
		self.index_file_dict={}
		self.file_list=[]
		self.sort_file_list=[] #**
		self.im_file=[] #top coverage file + coredump file
		self.cov_list=[]
		self.i=7
		
	def select_file(self):
		
		length=0
		file=root_dir+'coverage.txt'
		f=open(file)
		data=f.read()
		tmp1=data.split('\n')
		for t in tmp1:
			tmp2=t.split(' ')
			self.cov_list.append(int(tmp2[1]))
			self.file_list.append(tmp2[0])
		length=len(self.cov_list)
		length_10=int(length*0.1)
		
		index=[]
		#make index
		for i in range(length):
			index.append(i)
			
		for i in range(length):
			key=index[i]
			value=self.file_list[i]
			self.index_file_dict[key]=value

		sort_index=sorted(range(len(self.cov_list)),reverse=True,key=self.cov_list.__getitem__)
		self.cov_list.sort(reverse=True)

		for index in sort_index:
			key=self.index_file_dict[index]
			self.sort_file_list.append(key)
	
		self.im_file=self.sort_file_list[:perc]
		
		#append core dump file
		file=root_dir+'coredump.txt'
		f=open(file)
		data=f.read()
		tmp=data.split('\n')
		
		for file in tmp:
			if file in self.im_file:
				pass
			else:
				self.im_file.append(file)
		
	def load_data(self):
		tmp_list=[]	
		hex_content=[]
		total=[]
		hex_arr=[]
		total_list=[]
		total_arr=[]

		#check if olefile
		for file in self.im_file:
			im_file='hwp_seeds\\'+file
			
			if not olefile.isOleFile(im_file):
				self.im_file.remove(file)
		
		for file in self.im_file:
			ole=olefile.OleFileIO(im_file,write_mode=True)
			stream=ole.openstream(field)
			data=stream.read()
			stream.seek(0)
			hex_content.append(data) 
		#print(len(hex_content)) #274
		
		for string_hex in hex_content:
			string_hex=binascii.hexlify(string_hex)
			hex_list=[int(string_hex[i:i+2],16) for i in range(0,len(string_hex),2)]
			hex_arr=np.asarray(hex_list)
			total_list.append(hex_arr)
		total_arr=np.asarray(total_list)
		print(total_arr.shape) #(290,101430)
			

if __name__=="__main__":
	
	h=HWP()
	h.select_file()
	h.load_data()
