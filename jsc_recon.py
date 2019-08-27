import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import binascii
from tensorflow.examples.tutorials.mnist import input_data
import olefile

'''
[test4]
\x05HwpSummaryInformation 517
BinData/BIN0001.png 295 (o)
BinData/BIN0002.OLE 3318 
BodyText/Section0 3131 (o)
DocInfo 1084
DocOptions/_LinkDoc 524
PrvImage 3599
PrvText 1146
Scripts/DefaultJScript 136
Scripts/JScriptVersion 13
'''

root_dir=os.getcwd()+'/'
dir_list=os.listdir(root_dir)
perc=100
field='Scripts/JScriptVersion'
field_size=13

class VAE:
	def __init__(self,n_in):
		self.n_in=n_in

	def build(self):
		self.x=tf.placeholder(tf.float32,[None,self.n_in])
		self.lr=tf.placeholder(tf.float32,[])

		#encoder layer
		#W_en=tf.Variable(tf.random_normal([self.n_in,1024],stddev=0.001))
		#b_en=tf.Variable(tf.zeros([1024]))
		
		#en_h=tf.nn.relu(tf.matmul(self.x,W_en)+b_en)
		
		##append
		W_en=tf.Variable(tf.random_normal([self.n_in,6],stddev=0.001))
		b_en=tf.Variable(tf.zeros([6]))
		
		en_h=tf.nn.relu(tf.matmul(self.x,W_en)+b_en)
		##
		
		#latent layer
		W_mu=tf.Variable(tf.random_normal([6,2],stddev=0.001))
		b_mu=tf.Variable(tf.zeros([2]))
		W_sig=tf.Variable(tf.random_normal([6,2],stddev=0.001))
		b_sig=tf.Variable(tf.zeros([2]))
		
		mu=tf.matmul(en_h,W_mu)+b_mu
		sig=tf.matmul(en_h,W_sig)+b_sig
		e=tf.random_normal(tf.shape(mu))
		z=mu+tf.multiply(e,tf.exp(0.5 * sig))

		#decoder layer
		W_de=tf.Variable(tf.random_normal([2,6],stddev=0.001))
		b_de=tf.Variable(tf.zeros([6]))

		h_de=tf.nn.relu(tf.matmul(z,W_de)+b_de)
		
		W_out=tf.Variable(tf.random_normal([6,self.n_in],stddev=0.001))
		b_out=tf.Variable(tf.random_normal([self.n_in]))

		self.x_=tf.matmul(h_de,W_out)+b_out
		
		#loss
		KLD=-0.5 * tf.reduce_sum(1+sig - tf.pow(mu,2) - tf.exp(sig),reduction_indices=1)
		BCE=tf.reduce_sum(tf.nn.sigmoid_cross_entropy_with_logits(logits=self.x_,labels=self.x),reduction_indices=1)
		self.loss=tf.reduce_mean(KLD+BCE)

		#optimize
		self.train=tf.train.GradientDescentOptimizer(self.lr).minimize(self.loss)

		#reconstruction
		self.z_in=tf.placeholder(tf.float32,[None,2])
		h_de_=tf.nn.dropout(tf.nn.relu(tf.matmul(self.z_in,W_de)+b_de),0.5)
		self.new_x_=tf.nn.sigmoid(tf.matmul(h_de_,W_out)+b_out)

class HWP:
	
	def __init__(self):
		
		self.index_cov_dict={}
		self.index_file_dict={}
		self.file_list=[]
		self.sort_file_list=[] #**
		self.im_file=[] #top coverage file + coredump file
		self.cov_list=[]
		
	def select_file(self):
		
		'''
		#high coverage file
		length=0
		file=root_dir+'seed2_total_cov.txt'
		f=open(file)
		data=f.read()
		tmp1=data.split('\n')
		for t in tmp1:
			tmp2=t.split(' ')
			self.cov_list.append(int(tmp2[1]))
			self.file_list.append(tmp2[0])
		length=len(self.cov_list)
		length_10=int(length*0.1)
		
		index=[]
		#make index
		for i in range(length):
			index.append(i)
			
		for i in range(length):
			key=index[i]
			value=self.file_list[i]
			self.index_file_dict[key]=value

		sort_index=sorted(range(len(self.cov_list)),reverse=True,key=self.cov_list.__getitem__)
		self.cov_list.sort(reverse=True)

		for index in sort_index:
			key=self.index_file_dict[index]
			self.sort_file_list.append(key)
	
		self.im_file=self.sort_file_list[:perc]
		'''
		
		#segmentation fault file
		file=root_dir+'real_results\\seg_1\\seg_1_seg_list.txt'
		f=open(file)
		data=f.read()
		tmp=data.split('\n')
		
		for file in tmp:
			if file in self.im_file:
				pass
			else:
				self.im_file.append(file)
		print(self.im_file)
		
	def load_data(self):
		tmp_list=[]	
		hex_content=[]
		total=[]
		hex_arr=[]
		total_list=[]
		total_arr=[]

		#check if olefile
		for file in self.im_file:
			im_file=file
			
			if not olefile.isOleFile(im_file):
				self.im_file.remove(file)
		
		for file in self.im_file:
			im_file=file
			ole=olefile.OleFileIO(im_file,write_mode=True)
			stream=ole.openstream(field)
			data=stream.read()
			stream.seek(0)
			#print(file)
			#print('[*] real data: ',data)
			hex_content.append(data) 
		#print(len(hex_content)) #274
		
		for string_hex in hex_content:
			string_hex=binascii.hexlify(string_hex)

			hex_list=[int(string_hex[i:i+2],16) for i in range(0,len(string_hex),2)]
			hex_arr=np.asarray(hex_list)
			total_list.append(hex_arr)
		total_arr=np.asarray(total_list)
		return total_arr
		
def next_batch(num,data):

	batch=[]
	idx=np.arange(0,len(data))
	
	np.random.shuffle(idx)
	idx=idx[:num]
	data_shuffle=[data[i] for i in idx]
	data_shuffle=np.asarray(data_shuffle)
	for d in data_shuffle:
		inputs=(np.asfarray(d)/255.0*0.99)+0.01 #scale
		batch.append(inputs)
	batch_array=np.asarray(batch)
	return batch_array	
	
def main():

	global mi
	mi=0
	
	h=HWP()
	h.select_file()
	total_arr=h.load_data()
	total_x=total_arr
	
	n_in=13
	lr=1e-3
	vae=VAE(n_in)
	vae.build()
	
	saver=tf.train.Saver()
	with tf.Session() as sess:
		saver.restore(sess,"model/jsc.ckpt")
		
		for epoch_i in range(100):
			#z1=np.random.normal(loc=-2,scale=0.1,size=1)
			#z2=np.random.normal(loc=2,scale=0.1,size=1)
			#z=np.concatenate((z1,z2),axis=0)
			z=np.random.normal(size=2)
			z=np.array([z]).reshape(1,2)
			new_x_=sess.run(vae.new_x_,feed_dict={vae.z_in:z})
			
			x_=new_x_
			
			for i in range(len(x_[0])):
				tmp=x_[0][i]-0.01
				tmp=tmp/0.99
				tmp=int(tmp*255)
				if tmp<0:
					x_[0][i]=int(0)
				elif tmp>255:
					x_[0][i]=int(255)
				else:
					x_[0][i]=int(tmp)
			x_=x_.astype(int)
			hex_string=""
				
			for i in range(len(x_[0])):
				tmp=hex(x_[0][i])
				tmp=tmp[2:]
				if len(tmp)==1:
					tmp='0'+tmp
				hex_string+=tmp
			
			hex_string=binascii.unhexlify(hex_string)
		
			print(mi)
			recon_file='recon\\stand\\m'+str(mi)+'.hwp'
			ole=olefile.OleFileIO(recon_file,write_mode=True)
			stream=ole.openstream(field)
			ole.write_stream(field,hex_string)
			
			mi+=1
			
if __name__ == '__main__':
	main()
