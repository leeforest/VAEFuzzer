import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import binascii
from tensorflow.examples.tutorials.mnist import input_data
import olefile
root_dir=os.getcwd()+'/'

dir_list=os.listdir(root_dir)
perc=50
class HWP:
	
	def __init__(self):
		
		self.index_cov_dict={}
		self.index_file_dict={}
		self.file_list=[]
		self.sort_file_list=[] #**
		self.im_file=[] #top coverage file + coredump file
		self.cov_list=[]
		
	def select_file(self):
		'''
		length=0
		file='real_results\\seg_1\\seg_1_coverage_count.txt'
		f=open(file)
		data=f.read()
		tmp1=data.split('\n')
		for t in tmp1:
			tmp2=t.split(' ')
			self.cov_list.append(int(tmp2[1]))
			self.file_list.append(tmp2[0])
		length=len(self.cov_list)
		print(len(self.cov_list))
		print(sum(self.cov_list)/length)
		
		self.cov_list=[]
		length=0
		file='real_results\\top_file_coverage_count.txt'
		f=open(file)
		data=f.read()
		tmp1=data.split('\n')
		for t in tmp1:
			tmp2=t.split(' ')
			self.cov_list.append(int(tmp2[1]))
			self.file_list.append(tmp2[0])
		length=len(self.cov_list)
		print(len(self.cov_list))
		print(sum(self.cov_list)/length)		
		'''
		length=0
		file='real_results\\seg_1\\top_file_list+cov.txt'
		f=open(file)
		data=f.read()
		tmp1=data.split('\n')
		for t in tmp1:
			tmp2=t.split(' ')
			self.cov_list.append(int(tmp2[1]))
			self.file_list.append(tmp2[0])
		length=len(self.cov_list)
		
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
		print(self.cov_list)

		for i,cov in enumerate(self.cov_list):
			print(i,cov)
		
def main():
	h=HWP()
	h.select_file()

if __name__ == '__main__':
	main()
	