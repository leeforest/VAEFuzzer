#-*-coding:utf-8-*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import get_distribution
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CSV='results/test.csv'
n=5

#get features of mutated file
def get_similarity(n):
	content=[]
	file_list=[]
	for i in range(n):
		file_list.append('m'+str(i))
		
	#get hex data of mutated file 
	for i in range(n):
		print 'read m'+str(i)+'.hwp'
		filename='hwp_seeds/try_5/m'+str(i)+'.hwp'
		f=open(filename,'r')
		data=f.read()
		content.append(data)
    
	print '--------------------------------------------'

	hex_content=[]
	
	print "get m0.hwp"
	string=content[0]
	string_hex=string.encode("hex")
	hex_list=[string_hex[i:i+2] for i in range(0,len(string_hex),2)]
	hex_array=np.asarray(hex_list)
	m0_hex_array=hex_array.reshape(1,-1)
	
	for i in range(n):
		print "get m"+str(i)+'.hwp'
		string=content[i]
		string_hex=string.encode("hex")
		hex_list=[string_hex[i:i+2] for i in range(0,len(string_hex),2)]
		hex_array=np.asarray(hex_list)
		hex_array=hex_array.reshape(1,-1)

		print cosine_similarity(m0_hex_array,hex_array)
		

	'''
		tmp=""
		for i in range(len(hex_list)):
			string2=str(hex_list[i])
			tmp=tmp+string2
			tmp=tmp+" "

		hex_content.append(tmp)	
	
	#get coverage information in result directory	
	coverage_dict=get_distribution.get_dict(CSV,n)
	indexs=[]

	#generate indexs
	for i in range(n):
		index='m'+str(i)+'.hwp'
		indexs.append(index)
	'''
		



	'''
	file_index=[]
	file_sim=[]
	file_coverage=[]
	file_sim_dict={}
	for i in range(n):
		key=df.index[i]
		file_index.append(key)

	for i in range(n):
		key=file_index[i]
		value=df[0][key]
		file_sim.append(value)
	for i in range(n):
		file_index[i]="m"+str(file_index[i])+".hwp"
	
	for i in range(n):
		key=file_index[i]
		value=file_sim[i]
		file_sim_dict[key]=value
	
	for i in range(n):
		key=file_index[i]
		value=coverage_dict[key]
		file_coverage.append(value)
	
	print file_index,file_sim
	
	return file_index,file_sim,file_coverage,file_sim_dict
	'''

if __name__=="__main__":
	
	#sort_indexs,sort_sim,file_sim_dict=get_similarity(n)
	get_similarity(n)
