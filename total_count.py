#-*- coding: utf-8 -*-
import os

root_dir='C:\\Users\\Administrator.AHN-01806070854\\Desktop\\thesis\\real_results'
dir_list=os.listdir(root_dir)
dic={}
dic['HwpSummaryInformation']=1
dic['BIN0001']=1
dic['BIN0002']=1
dic['BIN0003']=1
dic['BIN0004']=1
dic['BIN0005']=1
dic['Section0']=1
dic['DocInfo']=1
dic['_LinkDoc']=1
dic['FileHeader']=1
dic['PrvImage']=1
dic['PrvText']=1
dic['DefaultJScript']=1
dic['JScriptVersion']=1

i=1
for j in range(len(dir_list)):
	file=root_dir+"\\test3_"+str(i)+'\\test3_'+str(i)+'_field_info.txt'
	f=open(file)
	data=f.read()
	tmp=data.split('\n')
	
	i+=1

	for t in tmp:
		if 'HwpSummaryInformation' in t:
			temp=t.split(' ')
			
			dic['HwpSummaryInformation']+=int(temp[1])

		if 'BIN0001' in t:
			temp=t.split(' ')
			
			dic['BIN0001']+=int(temp[1])

		if 'BIN0002' in t:
			temp=t.split(' ')
			
			dic['BIN0002']+=int(temp[1])

		if 'BIN0003' in t:
			temp=t.split(' ')
			
			dic['BIN0003']+=int(temp[1])

		if 'BIN0004' in t:
			temp=t.split(' ')
			
			dic['BIN0004']+=int(temp[1])

		if 'BIN0004' in t:
			temp=t.split(' ')
			
			dic['BIN0004']+=int(temp[1])

		if 'BIN0005' in t:
			temp=t.split(' ')
			
			dic['BIN0005']+=int(temp[1])

		if 'Section0' in t:
			temp=t.split(' ')
			
			dic['Section0']+=int(temp[1])

		if 'DocInfo' in t:
			temp=t.split(' ')
			
			dic['DocInfo']+=int(temp[1])

		if '_LinkDoc' in t:
			temp=t.split(' ')
			
			dic['_LinkDoc']+=int(temp[1])

		if 'FileHeader' in t:
			temp=t.split(' ')
			
			dic['FileHeader']+=int(temp[1])
	
		if 'PrvImage' in t:
			temp=t.split(' ')
			
			dic['PrvImage']+=int(temp[1])
			
		if 'PrvText' in t:
			temp=t.split(' ')
			
			dic['PrvText']+=int(temp[1])

		if 'DefaultJScript' in t:
			temp=t.split(' ')
			
			dic['DefaultJScript']+=int(temp[1])
	
		if 'JScriptVersion' in t:
			temp=t.split(' ')
			
			dic['JScriptVersion']+=int(temp[1])

	f.close()
	file=root_dir+'total_count.txt'
	f=open(file,'w')
	string_tmp=''
	for key in dic:
		string=key+' '+str(dic[key])+'\n'
		string_tmp+=string
	f.write(string_tmp)
	f.close()