#-*-coding:utf-8-*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import get_distribution
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import *
from pyZZUF import *
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
import random_mutate
import matplotlib.pyplot as plt
import clustering
import signal
import get_distribution

CSV='results/try_5_hwp_coverage_softmax_100.csv'
EXE='hwpviewer'
DIR='hwp_seeds/try_5/'
SEED=DIR+'m50.hwp'
n=100

class similarity:
	
	def __init__(self):
		
		self.exe=EXE
		self.seed=SEED
		self.pid=1
		self.mutated_file=None
		self.count=1
		self.seeds=[]
		self.coverage={}
		self.num=0
		self.hwp_field=[]
		self.hwp_field_size={}
		self.ole=None
		self.coverage={}
		self.n=100


	def seed_analyzer(self):			
			
		self.ole=olefile.OleFileIO(self.seed,write_mode=True)
		self.hwp_field=self.ole.listdir()
				
		print '\n'
		print '[*] HWP Seed info\n'

		#hwp field와 그 field의 size를 딕셔너리에 저장
		for i in range(len(self.hwp_field)):
			field=self.hwp_field[i]
			field_size=self.ole.get_size(self.hwp_field[i])
			print field,field_size		
			if len(field)>1:
				storage=field[0]
				stream=field[1]
				field=str(storage+'/'+stream)
				self.hwp_field_size[field]=field_size

			else:
				field=str(field[0])
				self.hwp_field_size[field]=field_size
		
	
	def get_field_similarity(self):
		
		field_list=[]
		new_field_list=[]
		for key in self.hwp_field_size:
			field_list.append(key)
	
		for field in field_list:
			if 'JScript' in field:
				new_field_list.append(field)

		field_list=new_field_list
		print field_list
		file_list=[]
		for i in range(n):
			file_list.append('m'+str(i)+'.hwp')

		#criteria: test.hwp
		criteria='hwp_seeds/test.hwp'
		ole=olefile.OleFileIO(criteria,write_mode=True)
		
		cri_content=[]
		cri_hex_content=[]
		for field in field_list:
			stream=ole.openstream(field)
			data=stream.read()
			stream.seek(0)
			size=self.hwp_field_size[field]
			cri_content.append(data)
		
		for content in cri_content:
			print content
			string_hex=content.encode("hex")
			hex_list=[string_hex[i:i+2] for i in range(0,len(string_hex),2)]
			print '\n'
			print hex_list
			tmp=""
			for i in range(len(hex_list)):
				string2=str(hex_list[i])
				tmp=tmp+string2
				tmp=tmp+" "
			print '\n'
			print tmp
			cri_hex_content.append(tmp)	
			
		cri_vec=TfidfVectorizer()
		cri_matrix=cri_vec.fit_transform(cri_hex_content)
	
		for i in range(len(cri_hex_content)):
			print len(cri_hex_content[i])

		sim_list=[]
		#compare with each mutated file 
		for m_file in file_list:
			print m_file
			m_file=DIR+str(m_file)
			self.ole=olefile.OleFileIO(m_file,write_mode=True)

			content=[]
			hex_content=[]
			for field in field_list:
				stream=self.ole.openstream(field)
				data=stream.read()
				stream.seek(0)
				size=self.hwp_field_size[field]
				content.append(data)

			for i in range(len(field_list)):
				string=content[i]
				string_hex=string.encode("hex")
				hex_list=[string_hex[i:i+2] for i in range(0,len(string_hex),2)]

				tmp=""
				for i in range(len(hex_list)):
					string2=str(hex_list[i])
					tmp=tmp+string2
					tmp+=" "
				
				hex_content.append(tmp)
			
			############################################	
			#for i in range(len(hex_content)):
			#	print len(hex_content[i])

			vec=TfidfVectorizer()
			matrix=vec.fit_transform(hex_content)
			sim=cosine_similarity(matrix,cri_matrix)
			sim=sim[0]
			
			sum=0
			length=len(sim)
			for s in sim:
				sum+=s
			
			sim_ave=float(sum)/length
			print sim_ave

			sim_list.append(sim_ave)
				
		print sim_list
		
		f=open('results/try_5_sim')
		for sim in sim_list:
			f.write(str(sim))

		sim_cov_dic={}
		cov_dic=get_distribution.get_dict(CSV,self.n)
		new_cov_dic={}
		tmp=""

		return sim_list

if __name__=="__main__":
	

	sim=similarity()
	sim.seed_analyzer()
	sim.get_field_similarity()
