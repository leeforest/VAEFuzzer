#-*-coding:utf-8-*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import get_distribution
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#get features of mutated file
def get_similarity(n):
	content=[]
	file_list=[]
	for i in range(n):
		file_list.append('m'+str(i))
		
	#get hex data of mutated file 
	for i in range(n):
		filename='seeds/m'+str(i)
		f=open(filename,'r')
		data=f.readline()
		content.append(data)

    	hex_content=[]
              
	for i in range(n):
		string=content[i]
		string_hex=string.encode("hex")
		hex_list=[string_hex[i:i+2] for i in range(0,len(string_hex),2)]
			
		tmp=""
		for i in range(len(hex_list)):
			string2=str(hex_list[i])
			tmp=tmp+string2
			tmp=tmp+" "

		hex_content.append(tmp)
	
	coverage_dict=get_distribution.get_dict('results/coverage_softmax_100.csv')
	indexs=[]
	for i in range(n):
		index='m'+str(i)
		indexs.append(index)
	
	vectorizer=TfidfVectorizer()
	vectors=vectorizer.fit_transform(hex_content).toarray() #form: list
	
	df=pd.DataFrame(vectors,index=indexs)
	criteria=df.loc['m0']
	df=df.dot(criteria)
	df=df.to_frame().reset_index()
	df=df.sort_values([0])

	print df

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
		file_index[i]="m"+str(file_index[i])
	
	for i in range(n):
		key=file_index[i]
		value=file_sim[i]
		file_sim_dict[key]=value

	for i in range(n):
		key=file_index[i]
		value=coverage_dict[key]
		file_coverage.append(value)
	
	print file_index
	return file_index,file_sim,file_coverage,file_sim_dict

if __name__=="__main__":
	
	n=100
	#sort_indexs,sort_sim,file_sim_dict=get_similarity(n)
	get_similarity(n)
