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
SEED_DIR='word_1'
RESULT_DIR='real_results/'+SEED_DIR
SEED_PATH='hwp_seeds/'+SEED_DIR+'/'
SEED_PATH_='hwp_seeds/'+SEED_DIR
FULL_SEED_PATH='/home/forest/fuzzer/'+SEED_PATH
RESULT_CSV=RESULT_DIR+'/'+SEED_DIR+'_coverage_count.txt'
RESULT_SEG=RESULT_DIR+'/'+SEED_DIR+'_seg_list.txt'
RESULT_FIELD=RESULT_DIR+'/'+SEED_DIR+'_field_info.txt'

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
		self.im_field=[]
		#self.n=ITER	
	
	def seed_analyzer(self):			
		
		if os.path.isdir(RESULT_DIR) is not True:
			command='mkdir '+RESULT_DIR
			os.system(command)
		elif os.path.isdir(SEED_PATH) is not True:
			command='mkdir '+SEED_PATH
			os.system(command)
		else:
			pass
	
		if os.path.isdir("hwp_seeds") is not True:
			os.system("mkdir hwp_seeds")
		else:
			pass
		command='cp '+self.seed+' '+SEED_PATH+'m'+str(self.iteration)+'.hwp'
		print(command)
		os.system(command)
		self.ole=olefile.OleFileIO(self.seed,write_mode=True)
		self.hwp_field=self.ole.listdir()
		#print self.hwp_field
		#self.hwp_field.remove(['FileHeader'])	
		
		print '\n'
		print '[*] HWP Seed info\n'
	
		#hwp field와 그 field의 size를 딕셔너리에 저장
		for i in range(len(self.hwp_field)):
			field=self.hwp_field[i]
			field_size=self.ole.get_size(self.hwp_field[i])
			print field, field_size
		
			if len(field)>1:
				storage=field[0]
				stream1=field[1]
				strema2=field[2]
				field=str(storage+'/'+stream1+'/'+stream2)
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
			#print segfault_list
		
		print '\ncrash count: %d\n' %len(segfault_list)
		
		'''
		f=open(RESULT_CSV,'a')
		for i in range(len(X)):
			xy=X[i]+" "+str(Y[i])+'\n'
			f.write(xy)
		f.close()
		f2.	close()
		'''
	
	def start_debugger(self,i,coverage_dict,X,Y,im_field,segfault_list,queue):
		
		f2=open(RESULT_FIELD,'a')
		f3=open(RESULT_SEG,'a')
		
		print "\n[*] iteration: %d" %self.iteration
		os.system('ulimit -c unlimited')
		test_file=SEED_PATH+'m'+str(self.iteration)+'.hwp'
		#before_file='hwp_seeds/m'+str(self.iteration-1)+'.hwp'
		path_dir=FULL_SEED_PATH
		if len(queue)==0:
			file_list=os.listdir(path_dir)
			rannum=random.randrange(0,len(file_list))
			random_file=file_list[rannum]
			random_file=SEED_PATH+str(random_file)
		else:
			#rannum=random.randrange(0,len(queue))
			random_file=str(queue[-1])
			#random_file=str(random_file)

		print 'selected file: ',random_file
		if self.iteration==0:
			pass
		else:
			command='cp '+random_file+' '+test_file
			os.system(command)
			#############
			field1,field2=self.mutation(test_file)
			self.field_info=str(field1)+'/'+str(field2)
		
		command=self.exe+' '+test_file		
		(status,result)=commands.getstatusoutput(command)
		#os.system(command)
		
		if self.iteration !=0:
			if 'fault' in result:
				print 'segmentation fault'
				print '--------------------------------------------------'
				print result
				print '--------------------------------------------------'
				im_field.append(self.field_info)
				segfault_list.append(test_file)
				f2.write(self.field_info+'\n')
				f3.write(test_file+'\n')

		print im_field
		print segfault_list
		
		f2.close()
		f3.close()

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
			rannum=random.randrange(2,4)
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
				
				tmp1=20
				tmp2=20
				if size1<20:
					tmp1=1
				if size2<20:
					tmp2=1

				size=min(size1,size2)/2
				rand_offset1=random.randrange(tmp1,size1-size-1)
				rand_offset2=random.randrange(tmp2,size2-size-1)
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
				tmp1=20
				tmp2=20
				if size1<20:
					tmp1=1
				if size2<20:
					tmp2=1

				rand_offset1=random.randrange(tmp1,size1-301)
				rand_offset2=random.randrange(tmp2,size2-301)
				
				data2_cut=data2[rand_offset2:rand_offset2+300]
				data1=data1[:rand_offset1]+data2_cut+data1[rand_offset1+300:]
				self.ole.write_stream(field1,data1)

		if rannum==3:
			if size1<300 or size2<300:
				
				tmp1=20
				tmp2=20
				if size1<20:
					tmp1=1
				if size2<20:
					tmp2=1
				
				size=min(size1,size2)/2
				rand_offset1=random.randrange(tmp1,size1-size-1)
				rand_offset2=random.randrange(tmp2,size2-size-1)
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
				tmp1=20
				tmp2=20
				if size1<20:
					tmp1=1
				if size2<20:
					tmp2=1
		
				rand_offset1=random.randrange(tmp1,size1-301)
				rand_offset2=random.randrange(tmp2,size2-301)
				#print hexdump(data1)
				
				data1_cut=data1[rand_offset1:rand_offset1+300]
				zzuf=pyZZUF(data1_cut)
				zzuf.set_seed(int(random.randrange(0,255)))
				zzuf.set_ratio(0.03)
				zzuf_data=zzuf.mutate()
				data1=data1[:rand_offset1]+str(zzuf_data)+data1[rand_offset1+300:]
				
				self.ole.write_stream(field1,data1)
		
		return field1,field2

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


exe="'C:\Program Files\Microsoft Office\Office16\WINWORD.EXE'"
seed='seed2.doc'

fuzz=fuzzer(exe,seed)
fuzz.seed_analyzer()
fuzz.fuzz()
