#-*-coding:utf-8-*-
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
import numpy as np
import clustering
import signal

ITER=4
SEED_DIR='try_7'
RESULT_DIR='results/'+SEED_DIR
SEED_PATH='hwp_seeds/'+SEED_DIR+'/'
SEED_PATH_='hwp_seeds/'+SEED_DIR
FULL_SEED_PATH='/home/forest/fuzzer/'+SEED_PATH
RESULT_CSV='results/'+SEED_DIR+'_hwp_coverage_softmax_'+str(ITER)+'.csv'


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
		self.coverage={}
		self.num=0
		self.hwp_field=[]
		self.hwp_field_size={}
		self.ole=None
		self.coverage={}
		self.field_info=""
		self.test_cov=[1,4,2,5]
		self.n=ITER
		
	def fuzz(self):
		
		print '\n'
		print '########################################################'
		print '#################Coverage Based Fuzzing#################'
		print '########################################################'	
		print '\n'
		print 'Start Fuzzing...'
		print 'Please wait for about 90 seconds per iteration\n'

		manager=Manager()
		coverage_dict=manager.dict()
		X=manager.list()
		Y=manager.list()
		segfault_list=manager.list()
		im_field=manager.list()
		jobs=[]
		
		for i in range(0,self.n):

			sproc=Process(target=self.start_debugger,args=(i,coverage_dict,X,Y,segfault_list,im_field))

			jobs.append(sproc)
			sproc.start()

			sproc.join()

			####################
			
			self.iteration+=1
		
		print '\n\n[*] segfault_list'
		print segfault_list

		print '\ncrash count: %d\n' %len(segfault_list)
		f=open(RESULT_CSV,'a')
		
	
	def start_debugger(self,i,coverage_dict,X,Y,segfault_list,im_field):
		
		print "\n[*] iteration: %d" %self.iteration
		os.system('ulimit -c unlimited')
		
		if self.iteration==0:
			pass
		else:
			field1,field2=self.mutation()
			self.field_info=str(field1)+'/'+str(field2)
		

		coverage=self.test_cov[self.iteration]
		print "$ coverage measure: "+str(coverage)+"\n"
		
		
		Y.append(coverage)

	
		if self.iteration !=0:
			if Y[self.iteration]>max(Y[0:-1]):
				print 'present coverage list'
				print Y
				print 'new coverage'
				print Y[self.iteration]
				im_field.append(str(self.field_info))
				print 'effect field'
				print im_field


	def mutation(self):
		
		return 'a','b'

exe=sys.argv[1]
seed=sys.argv[2]

fuzz=fuzzer(exe,seed)
fuzz.fuzz()
