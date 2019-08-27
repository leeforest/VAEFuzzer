#-*-coding:utf-8-*-
#!/usr/bin/env python
from multiprocessing import *
from pyZZUF import *
from pwn import *
import signal
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
import numpy as np
import matplotlib.pyplot as plt
import clustering 
import random_mutate as mutation
import commands
import mh_sampling
import field_similarity
import get_distribution

CSV='results/try_5_hwp_coverage_softmax_100.csv'

class fuzzer:
	
	def __init__(self,exe,seed):
		self.exe=exe
		self.seed=seed
		self.crash=None
		self.pid=1
		self.mutated_file=None
		self.running=False
		self.iteration=0
		self.count=1
		self.seeds=[]
		self.num=0
		self.hwp_field=[]
		self.hwp_field_size={}
		self.ole=None
		self.coverage={}
		self.file_index=[]
		self.file_sim=[]
		self.file_coverage=[]
		self.file_sim_dict={}
		self.x=np.arange(101,dtype=float)
		self.x_=0
		self.N=100 #data number
		self.n=100 #iteration number

	def get_distribution(self):
		
		coverage_dic,cov_list=get_distribution.get_dict(CSV,self.n)
		new_cov_dic={}
		for key in coverage_dic:
			value=coverage_dic[key]
			tmp=key.replace('try_5/','')
			new_cov_dic[tmp]=value
		
		SIM=field_similarity.similarity()
		SIM.seed_analyzer()
		self.file_sim=SIM.get_field_similarity()
		
		sort_index=sorted(range(len(self.file_sim)),key=self.file_sim.__getitem__)
		self.file_sim.sort()
		
		sort_cov_list=[]
		for i in sort_index:
			sort_cov_list.append(cov_list[i])

		ind=[i for i in range(100)]
		fig=plt.figure(figsize=(30,10))
		ind=np.arange(len(self.file_sim))
		plt.bar(ind,sort_cov_list)
		#plt.bar(ind,cov_list)
		fig.savefig('plot/all_field_ave.png')

		#plt.bar(self.file_sim,self.file_coverage)
		plt.xlabel('similarity')
		plt.ylabel('coverage')
		plt.show()
	

	#target distribution
	def p(self,x):
		
		sim=x
		sim_index=self.file_sim.index(sim)
		coverage=self.file_coverage[sim_index]
		return coverage
		
		'''
		key_index=self.total_X.index(key)
		value=self.total_Y[key_index]
		return value
		'''

	#proposal distribution
	def q(self,x):
		
		sigma=0.1
		pick=np.random.normal(loc=x,scale=sigma)
		
		aux=[]
		for value in self.file_sim:
			aux.append(abs(pick-value))

		closest_index=aux.index(min(aux))
		closest_sim=self.file_sim[closest_index]
		print 'closest similarity: ',closest_sim
		
		return closest_sim
		

	def fuzz(self):
		
		manager=Manager()
		coverage_dict=manager.dict()
		X=manager.list()
		Y=manager.list()
		sample_list=manager.list()
		segfault_list=manager.list()
		jobs=[]
		
		for i in range(0,self.n):
			print "\n[*] iteration: %d" %self.iteration
			if self.iteration==0:
				first=float(np.random.normal(loc=0.5,scale=0.5))
				if first<0:
					first=-first
				aux=[]
				for value in self.file_sim:
					aux.append(abs(first-value))
				closest_index=aux.index(min(aux))
				closest_sim=self.file_sim[closest_index]
				self.x[0]=closest_sim
				
			r=np.random.uniform(low=0.,high=1.)
			self.x_=self.q(self.x[i])
	
			print 'self.x: ',self.x[i]
			print 'self.x_: ',self.x_
	
			if r<min(1,float(self.p(self.x_))/float(self.p(self.x[i]))):
				self.x[i+1]=self.x_
			else:
				self.x[i+1]=self.x[i]
			
			print 'self.x: ',self.x[i]
			print 'self.x_: ',self.x_
		
			index=self.file_sim.index(self.x[i+1])
			sample=str(self.file_index[index])
			sample_list.append(sample)
			print 'selected sample: ',sample
			
			sproc=Process(target=self.start_debugger,args=(i,coverage_dict,X,Y,sample_list,segfault_list))
			mproc=Process(target=self.monitor_debugger)
			
			jobs.append(sproc)
			sproc.start()
			mproc.start()

			sproc.join()
			mproc.join()

			self.iteration+=1
	
		print '\n\n[*] segfault_list\n\n'
		print segfault_list
		print '\ncrash count: %d' %len(segfault_list)

		f=open('results/mh_coverage_softmax_100.csv','a')
		
		'''
		#just count
		for i in range(len(X)):
			xy=X[i]+" "+str(Y[i])+'\n'
			f.write(xy)
		f.close()
		'''
		#apply softmax
		for i in range(len(Y)):
			Y[i]=float(Y[i])/1000
		Y=self.softmax(Y)
		for i in range(len(X)):
			xy=X[i]+" "+str(Y[i])+'\n'
			f.write(xy)
		f.close()
	
	def signal_detect(self):
		signal.signal(11,self.signal_handler)
		print 'detect'
		#sys.exit(0)
		os.system('ulimit -c unlimited')
	

	def signal_handler(self,signal,frame):
		print "\n\n\n\n*********\n\n\n\n"


	def start_debugger(self,i,coverage_dict,X,Y,sample_list,segfault_list):
		
		sample=sample_list[-1]
		
		sample='seeds/'+sample
		os.system('ulimit -c unlimited')
		test_file='seeds/mhstart_m'+str(self.iteration)
		
		command='touch '+test_file
		os.system(command)
		
		#open the sample and mutate that sample named test_file
		mutation.mutation(sample,test_file)
		
		#os.system('cd /home/forest/pin/source/tools/ManualExamples')
		command='../pin/pin -t ../pin/source/tools/ManualExamples/obj-intel64/inscount1.so -- ./'+self.exe+' '+test_file		
		#os.system(command)
		(status,result)=commands.getstatusoutput(command)
		print result
		#command='./'+self.exe+' '+test_file
		#os.system(command)

		f=open('inscount.out','r')
		res=f.readline()

		coverage=re.search('count:(.*)',res)
		coverage=coverage.group(1)
		
		print "$ coverage measure: "+str(coverage)+"\n"
		
		key=test_file[6:]
		coverage_dict[key]=coverage
	
		X.append(key)
		Y.append(coverage)
		
		if 'core' in result:			
			print '*******************************'
			
			segfault_list.append(test_file)

	
	def softmax(self,y):
		e_x=np.exp(y-np.max(y))
		return e_x/e_x.sum()

	def plot(self):
		X=list(map(int,range(0,99)))
		Y=list()
		for i in range(99):
			y=self.p(X[i])
			Y.append(y)
		plt.figure(1)
		plt.plot(X,Y)
		plt.title('target distribution')
		plt.show()

exe=sys.argv[1]
seed=sys.argv[2]

fuzz=fuzzer(exe,seed)
fuzz.get_distribution()
#fuzz.fuzz()
