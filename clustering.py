#-*-coding:utf-8-*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from pwn import *
import re
import get_distribution
import numpy as np

#get features of mutated file
def get_features(n):
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
		
		vectorizer=TfidfVectorizer(min_df=1)
		vectors=vectorizer.fit_transform(hex_content) #form: list
		print vectors

		#NMF feature extraction
		vector_array=vectors.toarray()
		nmf=NMF(n_components=50)
		nmf.fit(vector_array)
		features=nmf.transform(vector_array)
		
		#feature normalizaion
		normalizer=Normalizer()
		norm_features=normalizer.fit_transform(features)
		df_features=pd.DataFrame(norm_features,index=file_list)
		
		#df_features.columns=['1','2']
		return df_features


def clustering(features,n,n_clusters):
		
		file_list=[]
		for i in range(n):
			file_list.append('m'+str(i))

		model=KMeans(n_clusters=n_clusters,algorithm='auto')
		model.fit(features)
			
		#clustreing and return label
		predict=pd.DataFrame(model.predict(features),index=file_list)
		predict.columns=['predict']
		r=pd.concat([features,predict],axis=1)

		group_df=predict['predict']
		group_list=group_df.values.tolist()

		#get coverage information
		coverage_dict=get_distribution.get_dict('results/coverage_softmax_100.csv')
		
		#file -> each group
		A=[]; B=[]; C=[]; D=[]
		for i in range(n):
			filename='m'+str(i)
			if group_list[i]==0:
				A.append(filename)
			if group_list[i]==1:
				B.append(filename)	
			if group_list[i]==2:
				C.append(filename)
			if group_list[i]==3:
				D.append(filename)
		
		sumA=0; sumB=0; sumC=0; sumD=0
		for i in range(len(A)):
			sumA+=float(coverage_dict[A[i]])
		for i in range(len(B)):
			sumB+=float(coverage_dict[B[i]])
		for i in range(len(C)):
			sumC+=float(coverage_dict[C[i]])
		for i in range(len(D)):
			sumD+=float(coverage_dict[D[i]])
		
		#sorting using coverage sum
		sumlist=[]
		sumlist.append(sumA); sumlist.append(sumB); sumlist.append(sumC); sumlist.append(sumD)
		sorted_sumlist=sorted(sumlist)
		sorted_sumlist.reverse()
		tmplist=[]
		
		#tmplist->group sorting 
		for i in range(n_clusters):
			if sorted_sumlist[i]==sumlist[0]:
				tmplist.append("A")	
			if sorted_sumlist[i]==sumlist[1]:
				tmplist.append("B")
			if sorted_sumlist[i]==sumlist[2]:
				tmplist.append("C")
			if sorted_sumlist[i]==sumlist[3]:
				tmplist.append("D")
		
		clustered_X=[]; clustered_Y=[]
		for i in range(n_clusters):
			if tmplist[i]=="A":
				clustered_X+=A
			if tmplist[i]=="B":
				clustered_X+=B
			if tmplist[i]=="C":
				clustered_X+=C
			if tmplist[i]=="D":
				clustered_X+=D
		
		for i in range(n):
			key=clustered_X[i]
			value=coverage_dict[key]
			clustered_Y.append(value)
		
		plt.figure(1)
		plt.title('total')
		ind=np.arange(len(clustered_X))
		plt.bar(ind,clustered_Y)
		#plt.show()

		return clustered_X,clustered_Y

if __name__=="__main__":
	
	n=100
	n_clusters=4
	features=get_features(n)
	clustering(features,n,n_clusters)
