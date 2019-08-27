import os

dic={}
dic['HwpSummaryInformation']=1
dic['BIN0001.png']=1
dic['BIN0002.png']=1
dic['BIN0003.OLE']=1
dic['BIN0004.bmp']=1
dic['BIN0005.bmp']=1
dic['Section0']=1
dic['DocInfo']=1
dic['_LinkDoc']=1
dic['FileHeader']=1
dic['PrvImage']=1
dic['PrvText']=1
dic['DefaultJScript']=1
dic['JScriptVersion']=1

i=5
#root_dir='C:\\Users\\Administrator.AHN-01806070854\\Desktop\\thesis\\real_results'
root_dir='C:\\Users\\SANS_PC0\\Desktop\\temp'

dir_list=os.listdir(root_dir)
for j in range(len(dir_list)):
	file=root_dir+"\\test3_"+str(i)+'\\test3_'+str(i)+'_field_info.txt'
	f=open(file)
	data=f.read()
	tmp=data.split('\n')
	
	i+=1
	list=tmp

	for field in  list:

		if 'HwpSummaryInformation' in field:
			dic['HwpSummaryInformation']+=1

		if 'BIN0001' in field:
			dic['BIN0001.png']+=1

		if 'BIN0002' in field:
			dic['BIN0002.png']+=1

		if 'BIN0003' in field:
			dic['BIN0003.OLE']+=1

		if  'BIN0004' in field:
			dic['BIN0004.bmp']+=1

		if  'BIN0005' in field:
			dic['BIN0005.bmp']+=1

		if  'Section0' in field:
			dic['Section0']+=1

		if  'DocInfo' in field:
			dic['DocInfo']+=1

		if  '_LinkDoc' in field:
			dic['_LinkDoc']+=1

		if  'FileHeader' in field:
			dic['FileHeader']+=1

		if  'PrvImage' in field:
			dic['PrvImage']+=1

		if  'PrvText' in field:
			dic['PrvText']+=1

		if  'DefaultJScript' in field:
			dic['DefaultJScript']+=1

		if  'JScriptVersion' in field:
			dic['JScriptVersion']+=1

	f.close()
	f=open(file,'w')
	string_tmp=''
	for key in dic:
		string=key+' '+str(dic[key])+'\n'
		string_tmp+=string
	f.write(string_tmp)
	f.close()
