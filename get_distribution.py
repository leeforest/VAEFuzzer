#-*-coding:utf-8-*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pwn import *
import re
import numpy as np
import sys

#get dictionary from csv
def get_dict(csv,n):
	

	file_list=[]
	cov_list=[]
	for i in range(100):
		file_list.append(str(i))

	f=open(csv,'r')
	coverage_dict={}
	
	count=0
	for i in range(n):
		tmp=f.readline().split(" ")
		key=tmp[0]
		value=tmp[1]
		coverage_dict[key]=value.replace("\n","")
		cov_list.append(value)
	f.close()
	i=1
	tmp=[]
	for key in coverage_dict:
		tmp.append(key)
	
	print len(tmp)
	tmp.sort()				
	print tmp

	return coverage_dict,cov_list


#get list X,Y from csv 
def get_data(csv):
	
	f=open(csv,'r')
	coverage_dict={}
	
	X=[]; Y=[]
	for i in range(100):
		tmp=f.readline().split(" ")
		X.append(tmp[0])
		Y.append(tmp[1].replace("\n",""))
	f.close()
	
	return X,Y

#plot distribution
def distribution(csv):
	
	X,Y=get_data(csv)
	sum=0
	ind=np.arange(len(X))
	plt.bar(ind,Y)
	plt.show()

if __name__=="__main__":
	
	CSV='results/try_5_hwp_coverage_softmax_100.csv'

	#csv=sys.argv[1]
	get_dict(CSV,100)
	
	#get_data(csv)
	#distribution(csv)
