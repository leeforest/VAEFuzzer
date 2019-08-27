import matplotlib
matplotlib.use('Agg')
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import functools
import os
import cv2
#import load_data
import binascii
import olefile

'''
[seed1]
\x05HwpSummaryInformation 501
BinData/BIN0001.png 182015
BinData/BIN0002.png 11555
BinData/BIN0003.OLE 13828
BinData/BIN0004.bmp 5990454
BinData/BIN0005.bmp 101430
BodyText/Section0 21868
DocInfo 4695
DocOptions/_LinkDoc 524
FileHeader 256
PrvImage 5154
PrvText 518
Scripts/DefaultJScript 272
Scripts/JScriptVersion 8

[seed2]
['\x05HwpSummaryInformation'] 501
['BinData', 'BIN0001.jpg'] 878177
['BinData', 'BIN0002.PNG'] 295
['BinData', 'BIN0003.bmp'] 587449
['BinData', 'BIN0004.OLE'] 3327
['BodyText', 'Section0'] 4306
['DocInfo'] 1160
['DocOptions', '_LinkDoc'] 524
['PrvImage'] 6469
['PrvText'] 1186
['Scripts', 'DefaultJScript'] 136
['Scripts', 'JScriptVersion'] 13
'''

root_dir='C:\\Users\\Administrator.AHN-01806070854\\Desktop\\thesis\\'
dir_list=os.listdir(root_dir)
#file_num=1000
perc=100
#field='Scripts/DefaultJScript'
#field_size=272 
#field='BodyText/Section0'
#field_size=21868
field='\x05HwpSummaryInformation'
field_size=501

class HWP:
	
	def __init__(self):
		
		self.index_cov_dict={}
		self.index_file_dict={}
		self.file_list=[]
		self.sort_file_list=[] #**
		self.im_file=[] #top coverage file + coredump file
		self.cov_list=[]
		self.i=7
		
	def select_file(self):
		
		length=0
		file=root_dir+'seed1_total_seg.txt'
		f=open(file)
		data=f.read()
		tmp1=data.split('\n')
		
		self.im_file=tmp1
		
	def load_data(self):
		tmp_list=[]	
		hex_content=[]
		total=[]
		hex_arr=[]
		total_list=[]
		total_arr=[]

		#check if olefile
		for file in self.im_file:
			im_file='hwp_seeds\\'+file
			
			if not olefile.isOleFile(im_file):
				self.im_file.remove(file)
		
		for file in self.im_file:
			print(file)
			im_file='hwp_seeds\\'+file
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
		#print(total_arr.shape) #(290,101430)
		#print(total_arr[0])
		return total_arr

def next_batch(num,data):

	batch=[]
	idx=np.arange(0,len(data))
	np.random.shuffle(idx)
	idx=idx[:num]
	data_shuffle=[data[ i] for i in idx]
	data_shuffle=np.asarray(data_shuffle)
	for data in data_shuffle:
		inputs=(np.asfarray(data)/255.0*0.99)+0.01 #scale
		batch.append(inputs)
	
	return np.asarray(batch)
	
def xavier_init(fan_in, fan_out, constant = 1):
	with tf.name_scope('xavier'):
		low = -constant * np.sqrt(6.0 / (fan_in + fan_out))
		high = constant * np.sqrt(6.0 / (fan_in + fan_out))
		return tf.random_uniform((fan_in, fan_out),minval = low, maxval = high,dtype = tf.float32)

def doublewrap(function):

	@functools.wraps(function)
	def decorator(*args, **kwargs):
		if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
			return function(args[0])
		else:
			return lambda wrapee: function(wrapee, *args, **kwargs)
	return decorator

@doublewrap
def define_scope(function, scope=None, *args, **kwargs):

	attribute = '_cache_' + function.__name__
	name = scope or function.__name__
	@property
	@functools.wraps(function)
	def decorator(self):
		if not hasattr(self, attribute):
			with tf.variable_scope(name, *args, **kwargs):
				setattr(self, attribute, function(self))
		return getattr(self, attribute)
	return decorator

class VariationalAutoencoder:

	def __init__(self, image, enc_dimensions = [field_size, 500, 200, 64], dec_dimensions = [64, 200, 500, field_size]):
		self.image = image
		self.enc_dimensions = enc_dimensions
		self.dec_dimensions = dec_dimensions
		self.latent = None
		self.prediction
		self.optimize
		self.error

	@define_scope
	def prediction(self):
		current_input = self.image

		# ENCODER
		encoder = []
		with tf.name_scope('Encoder'):
			for layer_i, n_output in enumerate(self.enc_dimensions[1:-1]):
				with tf.name_scope('enc_layer' + str(layer_i)):
					n_input = int(current_input.get_shape()[1])
					W = tf.Variable(xavier_init(n_input, n_output), name = 'weight'+str(layer_i))
					b = tf.Variable(tf.zeros(shape=(1, n_output)), name = 'bias'+str(layer_i))
					encoder.append(W)
					current_input = tf.nn.elu(tf.add(tf.matmul(current_input, W), b),name='enclayer' + str(layer_i))

		# Latent layer
		with tf.name_scope('LatentLayer'):
			n_input = int(current_input.get_shape()[1])

			with tf.name_scope('mu_layer'):
				mu_weight = tf.Variable(xavier_init(n_input, self.enc_dimensions[-1]), name = 'mu_weight')
				mu_bias = tf.Variable(tf.zeros(shape=(1, self.enc_dimensions[-1])), name = 'mu_bias')
				self.mu = tf.add(tf.matmul(current_input, mu_weight), mu_bias, name = 'mu')
				#tf.summary.image('mu', self.mu)

			with tf.name_scope('logvar_layer'):
				logvar_weight = tf.Variable(xavier_init(n_input, self.enc_dimensions[-1]), name = 'logvar_weight')
				logvar_bias = tf.Variable(tf.zeros(shape=(1, self.enc_dimensions[-1])), name = 'logvar_bias')
				self.logvar = tf.add(tf.matmul(current_input, logvar_weight), logvar_bias, name ='logvar')
				#tf.summary.image('logvar', self.logvar)

			eps = tf.random_normal(shape=(1, self.enc_dimensions[-1]), name = 'gaussian_noise')

			self.latent = tf.add(self.mu, tf.multiply(tf.sqrt(tf.exp(self.logvar)), eps), name ='hidden_layer')
			current_input = self.latent

		# DECODER
		with tf.name_scope('Decoder'):
			for layer_i, n_output in enumerate(self.dec_dimensions[1:]):
				with tf.name_scope('dec_layer' + str(layer_i)):
					n_input = int(current_input.get_shape()[1])
					W = tf.Variable(xavier_init(n_input, n_output), name = 'weight'+str(layer_i))
					b = tf.Variable(tf.zeros(shape=(1, n_output)), name = 'bias'+str(layer_i))
					encoder.append(W)
					current_input = tf.nn.elu(tf.add(tf.matmul(current_input, W), b),
                                              name='decclayer' + str(layer_i))

		return current_input

	@define_scope
	def optimize(self):
		optimizer = tf.train.AdamOptimizer(learning_rate=0.001)
		return optimizer.minimize(self.error)

	@define_scope
	def error(self):

		self.reconstr_error = tf.reduce_sum(tf.pow(tf.subtract(self.prediction, self.image), 2))
		print(self.reconstr_error)
		self.latent_loss = -1/2*tf.reduce_sum(1 + self.logvar - tf.square(self.mu) - tf.exp(self.logvar), name = 'latent_loss')
		self.loss = self.reconstr_error + self.latent_loss
		tf.summary.scalar('error', self.loss)
		return self.loss

def main():
	
	h=HWP()
	h.select_file()
	total_arr=h.load_data()
	x=total_arr
	#x=load_data()
	#print(x.shape) #(12,field_size)

	image = tf.placeholder(tf.float32, [None, field_size])
	model = VariationalAutoencoder(image)

	merged_summary = tf.summary.merge_all()
	sess = tf.Session()
	logpath = '/tmp/tensorflow_logs/vae/1'
	test_writer = tf.summary.FileWriter(logpath, graph=tf.get_default_graph())
	train_writer = tf.summary.FileWriter('/train')
	
	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())
	
		for epoch_i in range(100000):

			for batch_i in range(50):
				batch_xs=next_batch(50,x)
				_=sess.run(fetches=[model.optimize], feed_dict={image: batch_xs})
				error=model.error.eval(feed_dict={image: batch_xs})		
			
			if epoch_i%100==0:
				print(epoch_i, error)

				# Plot example reconstructions
				test_xs=next_batch(1,x)
				recon = sess.run(model.prediction, feed_dict={image: test_xs})
				#print(recon[0][0:100])
				for i in range(len(recon[0])):
					tmp=recon[0][i]-0.01
					tmp=tmp/0.99
					tmp=int(tmp*255)
					if tmp<0:
						recon[0][i]=int(0)
					elif tmp>255:
						recon[0][i]=int(255)
					else:
						recon[0][i]=int(tmp)
				recon=recon.astype(int)
				#recon=recon.tolist()
				hex_string=""

				for i in range(len(recon[0])):
					tmp=hex(recon[0][i])
					tmp=tmp[2:]
					if len(tmp)==1:
						tmp='0'+tmp
					hex_string+=tmp
			
				hex_string=binascii.unhexlify(hex_string)
		
				#before write, copy original 
				orig='results\\HwpSummaryInformation_seg\\m1.hwp'
				recon_file='results\\HwpSummaryInformation_seg\\m'+str(epoch_i)+'.hwp'
				command='copy '+orig+' '+recon_file
				os.system(command)
				ole=olefile.OleFileIO(recon_file,write_mode=True)
				stream=ole.openstream(field)
				ole.write_stream(field,hex_string)

	
if __name__ == '__main__':
  main()