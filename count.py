list=['BinData/BIN0002.png/Scripts/JScriptVersion', '\x05HwpSummaryInformation/PrvText', '\x05HwpSummaryInformation/BodyText/Section0', '\x05HwpSummaryInformation/BodyText/Section0', 'BinData/BIN0003.OLE/BodyText/Section0', 'BinData/BIN0003.OLE/BodyText/Section0', 'BodyText/Section0/BinData/BIN0003.OLE', 'BinData/BIN0003.OLE/BinData/BIN0002.png', 'BinData/BIN0001.png/BinData/BIN0004.bmp', 'BodyText/Section0/BinData/BIN0005.bmp', 'BodyText/Section0/BinData/BIN0005.bmp', 'BinData/BIN0001.png/BinData/BIN0001.png', 'BinData/BIN0002.png/PrvImage', '\x05HwpSummaryInformation/BinData/BIN0003.OLE', 'BinData/BIN0004.bmp/Scripts/JScriptVersion', 'BinData/BIN0003.OLE/Scripts/DefaultJScript', 'BinData/BIN0005.bmp/BodyText/Section0', 'DocOptions/_LinkDoc/PrvImage', 'BinData/BIN0001.png/BinData/BIN0001.png', 'BodyText/Section0/PrvImage', 'BinData/BIN0002.png/PrvText', 'BinData/BIN0003.OLE/BinData/BIN0001.png', 'BodyText/Section0/BinData/BIN0002.png', 'DocOptions/_LinkDoc/\x05HwpSummaryInformation', 'Scripts/JScriptVersion/\x05HwpSummaryInformation', 'BinData/BIN0001.png/BinData/BIN0001.png', 'PrvImage/\x05HwpSummaryInformation', 'BinData/BIN0003.OLE/BinData/BIN0004.bmp', 'BinData/BIN0005.bmp/Scripts/DefaultJScript', 'BinData/BIN0001.png/Scripts/JScriptVersion', 'Scripts/DefaultJScript/BodyText/Section0', 'BinData/BIN0004.bmp/BinData/BIN0004.bmp', '\x05HwpSummaryInformation/BinData/BIN0002.png', 'Scripts/DefaultJScript/BinData/BIN0001.png', 'BinData/BIN0005.bmp/PrvText', 'PrvImage/PrvImage', 'Scripts/JScriptVersion/BodyText/Section0', 'BinData/BIN0003.OLE/DocInfo', 'BinData/BIN0003.OLE/DocInfo', 'DocOptions/_LinkDoc/BinData/BIN0003.OLE', 'BodyText/Section0/BodyText/Section0', 'PrvImage/BinData/BIN0005.bmp', 'PrvImage/PrvText', 'BinData/BIN0002.png/PrvImage', 'Scripts/DefaultJScript/BinData/BIN0004.bmp', '\x05HwpSummaryInformation/\x05HwpSummaryInformation', 'Scripts/JScriptVersion/DocOptions/_LinkDoc', 'DocInfo/DocInfo', 'BinData/BIN0001.png/\x05HwpSummaryInformation', 'DocInfo/BodyText/Section0', 'DocOptions/_LinkDoc/PrvText', 'BinData/BIN0004.bmp/Scripts/JScriptVersion', 'BinData/BIN0002.png/DocInfo', 'Scripts/JScriptVersion/BinData/BIN0003.OLE', 'PrvText/DocInfo', 'DocOptions/_LinkDoc/Scripts/DefaultJScript', 'BodyText/Section0/PrvImage', 'BinData/BIN0003.OLE/BinData/BIN0001.png', 'DocInfo/PrvImage', 'BinData/BIN0002.png/PrvImage', 'Scripts/DefaultJScript/PrvText', 'DocOptions/_LinkDoc/BinData/BIN0004.bmp', 'DocInfo/BinData/BIN0004.bmp', 'BinData/BIN0005.bmp/DocOptions/_LinkDoc']
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

for key in dic:
	print key,dic[key]
