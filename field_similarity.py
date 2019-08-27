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
				
			if len(field)>1:
				storage=field[0]
				stream=field[1]
				field=str(storage+'/'+stream)
				self.hwp_field_size[field]=field_size

			else:
				field=str(field[0])
				self.hwp_field_size[field]=field_size
		
	def get_field_similarity(self):
		
		'''
		field_list=[]
		for key in self.hwp_field_size:
			field_list.append(key)
			
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
			
		for i in range(len(field_list)):
			string=cri_content[i]
			string_hex=string.encode("hex")
			hex_list=[string_hex[i:i+2] for i in range(0,len(string_hex),2)]
					
			tmp=""
			for i in range(len(hex_list)):
				string2=str(hex_list[i])
				tmp=tmp+string2
				tmp=tmp+" "

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
		'''
		sim_list=[0.7531850679972913, 0.7520634519649734, 0.7520634519649734, 0.7531850679972913, 0.7520609882377844, 0.7520383862249519, 0.7520634519649734, 0.7520678269353063, 0.7520823623131251, 0.7520170524884937, 0.7520680544116995, 0.7520913863739592, 0.7520475401501633, 0.7520609882377844, 0.7520363672822715, 0.7519714352132031, 0.7531741868436511, 0.7520609882377844, 0.752191691477739, 0.7519874451367012, 0.752039601597253, 0.752191691477739, 0.7520475401501633, 0.752191691477739, 0.7519874451367012, 0.7520746155964967, 0.7519855282144253, 0.7519512155230983, 0.7520428410029579, 0.7520746155964967, 0.7520132122581088, 0.7521891433044997, 0.7523216482366528, 0.7531850679972913, 0.7531420122735177, 0.7519829977104278, 0.752191691477739, 0.7521934790680064, 0.752191691477739, 0.7520403383367412, 0.7520570479790764, 0.7520132122581088, 0.7521597455887402, 0.7519998108059579, 0.7531850679972913, 0.7520632387984796, 0.7520532816661187, 0.7506306238356343, 0.752191691477739, 0.7522482423334452, 0.752159494645454, 0.7520986412587444, 0.7531420122735177, 0.7520957232409067, 0.7531415231858, 0.7519512155230983, 0.752039601597253, 0.7531850679972913, 0.7519657495558434, 0.7519632996379942, 0.7521907656135097, 0.7531741868436511, 0.7520132122581088, 0.7520609882377844, 0.7531850679972913, 0.7531850679972913, 0.7532553792169425, 0.7532193425464356, 0.7521827725091849, 0.753095115029563, 0.7520609882377844, 0.7521907656135097, 0.7521891433044997, 0.7531850679972913, 0.752027088574161, 0.7520802665760502, 0.7520634519649734, 0.7520132122581088, 0.7521734749707213, 0.7521884595058841, 0.7520347265297813, 0.7531363821249525, 0.7506676772583122, 0.7520338800031761, 0.7521796718011108, 0.7531311748414237, 0.7519980769443947, 0.7532400429425257, 0.7521203902780123, 0.7531850679972913, 0.7531474989665305, 0.752159494645454, 0.7531741868436511, 0.7520746155964967, 0.7519745026973813, 0.7520475401501633, 0.7520680544116995, 0.7531376027617446, 0.7520823623131251, 0.7532235783665236]

		sim_cov_dic={}
		cov_dic=get_distribution.get_dict(CSV,self.n)
		new_cov_dic={}
		tmp=""

		return sim_list

if __name__=="__main__":
	

	sim=similarity()
	sim.seed_analyzer()
	sim.get_field_similarity()
