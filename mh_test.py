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
import similarity
import mh_sampling

ITER=100
SEED_DIR='try_5'
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
		self.n=ITER

	
	def seed_analyzer(self):			
		
		if os.path.isdir("hwp_seeds") is not True:
			os.system("mkdir hwp_seeds")
		else:
			pass
		command='cp '+self.seed+' '+SEED_PATH+'m'+str(self.iteration)+'.hwp'
		print command
		os.system(command)
		self.ole=olefile.OleFileIO(self.seed,write_mode=True)
		self.hwp_field=self.ole.listdir()
		
		print '\n'
		print '[*] HWP Seed info\n'
	
		#hwp field와 그 field의 size를 딕셔너리에 저장
		for i in range(len(self.hwp_field)):
			field=self.hwp_field[i]
			field_size=self.ole.get_size(self.hwp_field[i])
			print field, field_size
		
			if len(field)>1:
				storage=field[0]
				stream=field[1]
				field=str(storage+'/'+stream)
				self.hwp_field_size[field]=field_size

			else:
				field=str(field[0])
				self.hwp_field_size[field]=field_size
		
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
		jobs=[]
		
		for i in range(0,self.n):

			sproc=Process(target=self.start_debugger,args=(i,coverage_dict,X,Y,segfault_list))
			mproc=Process(target=self.monitor_debugger)

			jobs.append(sproc)
			sproc.start()
			mproc.start()

			sproc.join()
			mproc.join()

			####################
			self.iteration+=1
			print segfault_list
		
		print '\n\n[*] segfault_list'
		print segfault_list

		print '\ncrash count: %d\n' %len(segfault_list)
		f=open(RESULT_CSV,'a')
		
		'''
		#apply softmax
		for i in range(len(Y)):
			Y[i]=float(Y[i])/1000000
		Y=self.softmax(Y)
		for i in range(len(X)):
			xy=X[i]+" "+str(Y[i])+'\n'
			f.write(xy)
		f.close()
		'''
		
		for i in range(len(X)):
			xy=X[i]+" "+str(Y[i])+'\n'
			f.write(xy)
		f.close()


	def start_debugger(self,i,coverage_dict,X,Y,segfault_list):
		
		print "\n[*] iteration: %d" %self.iteration
		os.system('ulimit -c unlimited')
		test_file=SEED_PATH+'m'+str(self.iteration)+'.hwp'
		#before_file='hwp_seeds/m'+str(self.iteration-1)+'.hwp'
		path_dir=FULL_SEED_PATH
		file_list=os.listdir(path_dir)
		rannum=random.randrange(0,len(file_list))
		random_file=file_list[rannum]
		random_file=SEED_PATH+str(random_file)
		
		print 'selected file: ',random_file
		if self.iteration==0:
			pass
		else:
			#command='cp '+before_file+' '+test_file
			command='cp '+random_file+' '+test_file
			os.system(command)
			#############
			self.mutation(test_file)

		command='../pin/pin -t ../pin/source/tools/ManualExamples/obj-intel64/inscount1.so -- '+self.exe+' '+test_file		
		(status,result)=commands.getstatusoutput(command)
		#os.system(command)
		
		f=open('inscount.out','r')
		res=f.readline()

		coverage=re.search('count:(.*)',res)
		coverage=coverage.group(1)
		print "$ coverage measure: "+str(coverage)+"\n"
		
		key=test_file[10:]
		coverage_dict[key]=coverage
		
		X.append(key)
		Y.append(coverage)

		if 'core' in result:
			print result
			segfault_list.append(test_file)

		'''
		#core파일이 생기면 count 횟수에 맞춰 이름을 변경하고 crashes 디렉터리로 옮김
		if os.path.isfile("core"):
			print "\n[**] segmentation fault is detected"

			if os.path.isdir("crashes") is not True:
				os.system("mkdir crashes")
			else:
				pass
			core="core"+str(self.count)
			os.system("mv core "+core)
			os.system("mv "+core+" crashes")			
			self.count+=1
		'''

	def softmax(self,x):
		e_x=np.exp(x-np.max(x))
		return e_x/e_x.sum()


	def mutation(self,test_file):
		
		mutation_file=test_file
		print '- file name: ',mutation_file
		self.ole=olefile.OleFileIO(mutation_file,write_mode=True)
		
		#field1의 특정 오프셋부터 일정 바이트를 field2의 특정 오프셋부터 일정 바이트로 덮어쓸것
		field1,field2=self.hwp_field_select()
		print '- selected field: ',field1, field2

		#랜덤으로 선택된 필드 읽어들이기
		stream1=self.ole.openstream(field1)
		stream2=self.ole.openstream(field2)
		data1=stream1.read()
		data2=stream2.read()
		stream1.seek(0)
		stream2.seek(0)
		
		size1=self.hwp_field_size[field1]
		size2=self.hwp_field_size[field2]
		#print size1, size2

		if size1<5000 and size2<5000:
			rannum=random.randrange(1,4)
		else:
			rannum=random.randrange(2,4)

		if rannum==1:
			if size1>size2:
					
				#data1이 덮어씌어지기 전에 임시 buf에 저장
				temp_buf=data1
				temp_stream=stream1
				
				#1) field1 <--- field2
				#필드 사이즈 차이 계산해서 같은 크기로 맞추기
				num=size1/size2
				data2=data2*num
				sub=size1-len(data2)
					
				#data1과 data2의 사이즈가 같아짐
				data2=stream2.read(sub)+data2
				self.ole.write_stream(field1,data2)

				#2) field2 <--- field1
				#data1과 stream1을 원래대로 복구
				data1=temp_buf
				stream1=temp_stream
					
				#stream1을 size2만큼 읽어서 field2에 덮어쓰기
				data1=stream1.read(size2)
				self.ole.write_stream(field2,data1)

			elif size2>size1:
					
				temp_buf=data1
				temp_stream=stream1

				#1) field1 <--- field2
				data2=stream2.read(size1)
				self.ole.write_stream(field1,data2)
					
				#2) field2 <--- field1
				data1=temp_buf
				sream1=temp_stream
					
				num=size2/size1
				data1=data1*num
				sub=size2-len(data1)
				data1=stream1.read(sub)+data1
				self.ole.write_stream(field2,data1)

			else:
				pass

		if rannum==2:
			if size1<300 or size2<300:
			
				size=min(size1,size2)/2
				rand_offset1=random.randrange(1,size1-size-1)
				rand_offset2=random.randrange(1,size2-size-1)
				data2_cut=data2[rand_offset2:rand_offset2+size]
				data1=data1[:rand_offset1]+data2_cut+data1[rand_offset1+size:]
				
				self.ole.write_stream(field1,data1)
				'''
				if size1<20 or size2<20:
			
				size=min(size1,size2)/2
				rand_offset1=random.randrange(1,size1-11)
				rand_offset2=random.randrange(1,size2-11)
				data2_cut=data2[rand_offset2:rand_offset2+10]
				data1=data1[:rand_offset1]+data2_cut+data1[rand_offset1+10:]
				
				self.ole.write_stream(field1,data1)
				'''
			else:
				
				rand_offset1=random.randrange(1,size1-301)
				rand_offset2=random.randrange(1,size2-301)
				
				data2_cut=data2[rand_offset2:rand_offset2+300]
				data1=data1[:rand_offset1]+data2_cut+data1[rand_offset1+300:]
				self.ole.write_stream(field1,data1)

		if rannum==3:
			if size1<300 or size2<300:
				size=min(size1,size2)/2
				
				rand_offset1=random.randrange(1,size1-size-1)
				rand_offset2=random.randrange(1,size2-size-1)
				data1_cut=data1[rand_offset1:rand_offset1+size]
				zzuf=pyZZUF(data1_cut)
				zzuf.set_seed(int(random.randrange(0,255)))
				zzuf.set_ratio(0.03)
				zzuf_data=zzuf.mutate()
				data1=data1[:rand_offset1]+str(zzuf_data)+data1[rand_offset1+size:]
		
				self.ole.write_stream(field1,data1)
				
				'''
				if size1<20 or size2<20:
				rand_offset1=random.randrange(1,size1-11)
				rand_offset2=random.randrange(1,size2-11)
				data1_cut=data1[rand_offset1:rand_offset1+10]
				zzuf=pyZZUF(data1_cut)
				zzuf.set_seed(int(random.randrange(0,255)))
				zzuf.set_ratio(0.03)
				zzuf_data=zzuf.mutate()
				data1=data1[:rand_offset1]+str(zzuf_data)+data1[rand_offset1+10:]
		
				self.ole.write_stream(field1,data1)
				'''
			else:
				rand_offset1=random.randrange(1,size1-301)
				rand_offset2=random.randrange(1,size2-301)
				#print hexdump(data1)
				
				data1_cut=data1[rand_offset1:rand_offset1+300]
				zzuf=pyZZUF(data1_cut)
				zzuf.set_seed(int(random.randrange(0,255)))
				zzuf.set_ratio(0.03)
				zzuf_data=zzuf.mutate()
				data1=data1[:rand_offset1]+str(zzuf_data)+data1[rand_offset1+300:]
				
				self.ole.write_stream(field1,data1)
		


	def hwp_field_select(self):
		
		#hwp 필드를 랜덤으로 선택하는 부분
		random_field1=random.randrange(0,len(self.hwp_field))
		random_field2=random.randrange(0,len(self.hwp_field))
		
		field1=self.hwp_field[random_field1]
		field2=self.hwp_field[random_field2]
			
		if len(self.hwp_field[random_field1])>1:
			storage=self.hwp_field[random_field1][0]
			stream=self.hwp_field[random_field1][1]
			field1= storage+'/'+stream

		else:
			field1=self.hwp_field[random_field1][0]

	
		if len(self.hwp_field[random_field2])>1:
			storage=self.hwp_field[random_field2][0]
			stream=self.hwp_field[random_field2][1]
			field2= storage+'/'+stream

		else:
			field2=self.hwp_field[random_field2][0]

		return field1,field2


	def monitor_debugger(self):
		time.sleep(80)

		#exe와 관련된 프로세스의 pid 가져오기
		command='ps -ef | grep '+self.exe+' | grep -v grep | awk \'{print $2}\''
		(num,pid)=commands.getstatusoutput(command)
		
		#kill해야 하는 pid 구하기
		pid=pid.split()
		pid=max(pid)
		
		#실행중인 프로세스 kill 하기
		kill_command="kill -15 "+pid
		'''
		res=commands.getoutput(kill_command)
		coverage=re.search('count:(.*)',res)
		print '----------------'
		print res
		print '----------------'
		coverage=coverage.group(1)

		print "\n[*] coverage measure: "+coverage+"\n"
		'''
		os.system(kill_command)
		print '- pid: ',pid


exe=sys.argv[1]
seed=sys.argv[2]

fuzz=fuzzer(exe,seed)
fuzz.seed_analyzer()
fuzz.fuzz()
