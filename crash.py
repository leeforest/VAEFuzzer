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

#ITER=
SEED_DIR='vae_hwp_sum'
RESULT_DIR='real_results/'+SEED_DIR
SEED_PATH='hwp_seeds/'+SEED_DIR+'/'
SEED_PATH_='hwp_seeds/'+SEED_DIR
FULL_SEED_PATH='/home/forest/fuzzer/'+SEED_PATH
RESULT_SEG=RESULT_DIR+'/'+SEED_DIR+'_seg_list.txt'

class fuzzer:
		
	def __init__(self,exe):
		self.exe=exe
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
		self.im_field=[]
		#self.n=ITER	
	
	
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
		queue=manager.list()
		jobs=[]
		
		for i in range(0,1000):

			sproc=Process(target=self.start_debugger,args=(i,coverage_dict,X,Y,im_field,segfault_list,queue))
			mproc=Process(target=self.monitor_debugger)

			jobs.append(sproc)
			sproc.start()
			mproc.start()

			sproc.join()
			mproc.join()

			####################
			
			self.iteration+=1
		
		print '\ncrash count: %d\n' %len(segfault_list)
		

	def start_debugger(self,i,coverage_dict,X,Y,im_field,segfault_list,queue):
		
		f3=open(RESULT_SEG,'a')
		
		print "\n[*] iteration: %d" %self.iteration
		test_file=SEED_PATH+'m'+str(self.iteration)+'.hwp'
	
		command=self.exe+' '+test_file		
		(status,result)=commands.getstatusoutput(command)
		
		if self.iteration !=0:
			if 'fault' in result:
				print 'segmentation fault'
				print '--------------------------------------------------'
				print result
				print '--------------------------------------------------'
				segfault_list.append(test_file)
				f3.write(test_file+'\n')
		
		print segfault_list
		f3.close()
	
	def monitor_debugger(self):
		time.sleep(5)

		#exe와 관련된 프로세스의 pid 가져오기
		command='ps -ef | grep '+self.exe+' | grep -v grep | awk \'{print $2}\''
		(num,pid)=commands.getstatusoutput(command)
		
		#kill해야 하는 pid 구하기
		pid=pid.split()
		pid=max(pid)
		
		#실행중인 프로세스 kill 하기
		kill_command="kill -15 "+pid
		os.system(kill_command)
		print '- pid: ',pid


exe='hwpviewer'

fuzz=fuzzer(exe)
fuzz.fuzz()
