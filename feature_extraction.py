#encoding=utf-8
import math
import json
import os
import sys
import csv
import pickle
import numpy
def SigmaPDF(num,nummean,numstd):
	num=float(num)
	nummean=float(nummean)
	numstd=float(numstd)
	return math.exp((-1*(num-nummean)**2)/(2*numstd**2))/(numstd*2.5)
def Sigma(list1,std1):
	U=float(len(list1)/2)
	f=[]
	for iter in range(len(list1)):
		item=float(list1[iter])
		f.append(SigmaPDF(iter,U,std1))
	return f
def GYHsigma(list1):
	sum=0.0
	for item in list1:
		sum+=item**2
	out=[]
	for item in list1:
		out.append(float(item/sum))
	return out
def GYHpitch(list1):
	sum=0.0
	for item in list1:
		sum+=item**2
	out=[]
	for item in list1:
		out.append(float(item/sum))
	return out
def Product(list1,list2):
	result=0.0
	for iter in range(len(list1)):
		result+=float(list1[iter]*list2[iter])
	return result
def list2Cmaxmin(list1):
	val=0
	valmax=0
	for iter in range(len(list1)-1):
		if list1[iter+1]>list1[iter]:
			val+=list1[iter+1]-list1[iter]
			if val>valmax:
				valmax=val
		else :
			val=0
	return 	valmax

def list2mean(list1):
	N=len(list1)
	#listn=float(list1)
	listn=list1
	narray=numpy.array(listn)
	sum1=narray.sum()
	mean=float(sum1)/float(N)
	return mean
def list2var(list1):
	N=len(list1)
	#listn=float(list1)
	listn=list1
	narray=numpy.array(listn)
        sum1=narray.sum()
	mean=float(sum1/N)
	narray2=narray*narray
	sum2=narray2.sum()
	var=float(sum2/N-mean**2)
	return var
def list2max(list1):
	#listn=float(list1)
	listn=list1
	return max(listn)
def list2min(list1):
	listn=list1
	#listn=float(list1)
	return min(listn)
def getvalfeature(position,vals,start,end,low,high):
	startp=low
	endp=high
	for iter in range(len(position)):
		if position[iter]==start:
			startp=iter
			break
	for iter in range(len(position)):
		if position[iter]==end:
			endp=iter
			break
	return vals[startp:endp]
def intonation_feature(feature_dict):
	f_outdict=dict()
	station=[]
	position=range(feature_dict["intonation_curve"]["start"],feature_dict["intonation_curve"]["end"]+1)
	vals=feature_dict["intonation_curve"]["vals"]
#	print vals
#	print position
	for item in feature_dict["words"]:
#		print item["word"]["stats"]["start"]
#		print type(item["word"]["stats"]["start"])
		station.append(item["stats"]["start"])
		station.append(item["stats"]["end"])
	high=max(station)
	low=min(station)
	for item in feature_dict["words"]:
		if item["stats"]["start"]<low or item["stats"]["end"]>high:
			#lsit=list2mean(vals)
			list100=[list2mean(vals),list2var(vals),list2mean(vals),list2mean(vals),len(item["syllables"]),0,Product(GYHsigma(Sigma(vals,0.2)),GYHpitch(vals)),Product(GYHsigma(Sigma(vals,0.5)),GYHpitch(vals)),Product(GYHsigma(Sigma(vals,1)),GYHpitch(vals)),Product(GYHsigma(Sigma(vals,5)),GYHpitch(vals)),Product(GYHsigma(Sigma(vals,10)),GYHpitch(vals))]
			f_outdict[item["word"]]=list100
			#f_outdict[item["word"]]=[]
			#f_outdict[item["word"]].append(list2mean(vals))
			#f_outdice[item["word"]].append(list2var(vals))
			#f_outdice[item["word"]].append(list2min(vals))
			#f_outdice[item["word"]].append(list2max(vals))
		else:
			start=item["stats"]["start"]
			end=item["stats"]["end"]
			nvals=getvalfeature(position,vals,start,end,low,high)
			#list=list2mean(nvals)
	#		try :
	#			list2max(nvals)-list2min(nvals)
			#list=[list2mean(nvals),list2var(nvals),list2min(nvals),list2max(nvals),len(item["syllables"]),list2max(nvals)-list2min(nvals)]
			list100=[list2mean(nvals),list2var(nvals),list2min(nvals),list2max(nvals),len(item["syllables"]),list2Cmaxmin(nvals),Product(GYHsigma(Sigma(nvals,0.2)),GYHpitch(nvals)),Product(GYHsigma(Sigma(nvals,0.5)),GYHpitch(nvals)),Product(GYHsigma(Sigma(nvals,1)),GYHpitch(nvals)),Product(GYHsigma(Sigma(nvals,5)),GYHpitch(nvals)),Product(GYHsigma(Sigma(nvals,10)),GYHpitch(nvals))]
	#		except:
	#			1+1
#				print("ereor")
#				print(nvals)
	#		nvals=[1,2]
	#		print navals
		#	print Product(GYHsigma(Sigma(nvals,10)),GYHpitch(nvals))
			f_outdict[item["word"]]=list100
			#f_outdict[item["word"]]=[]
			#f_outdict[item["word"]].append(list2mean(nvals))
			#f_outdice[item["word"]].append(list2var(nvals))
			#f_outdice[item["word"]].append(list2min(nvals))
			#f_outdice[item["word"]].append(list2max(nvals))
	return f_outdict
#chongfucishu=0	
def json2feature(filename):
	json_data=open(filename)
	data=json.load(json_data)
#	print type(data["intonation_curve"]["start"])
#	print data["intonation_curve"]["start"]
	feature=dict()
	f_outdict=intonation_feature(data)
#	print data["intonation_curve"]	
	
	for item in data["words"]:#下面那句决定提取的特征
		#print type(data["words"])#list
		#print item["word"]#
	#	feature[item["word"]]=[item["stats"]["start"],item["stats"]["end"],item["stats"]["energy"]]
		#基本特征＋句子长度特征
		#feature[item["word"]]=[item["stats"]["start"],item["stats"]["end"],item["stats"]["energy"],len(data["words"])]
        	#所有的特征
		if item["word"] in feature:
			print item["word"].upper()
			for item in data["words"]:
				print item["word"]
		else:
			feature[item["word"]]=[item["stats"]["start"],item["stats"]["end"],item["stats"]["energy"],len(data["words"]),f_outdict[item["word"]]]
	#print len(feature)
	#print len(data["words"])
	if len(feature)==len(data["words"]):
		return feature
	else:
		return "error"

rootdir='./jsonSmall'
FileList=[]# 将被处理文件的目录
for root,SubFloders,files in os.walk(rootdir):
	for f in files:
		if f.find('.json')!=-1:
		#	FileList.append(os.path.join(root,f))
			FileList.append(f)
			#print(os.path.join(root,f))
	errormessage=[]
count_IC=0
for item in FileList:#特征`提取
	#print(type(item))
	#print len(item)
	count_IC+=1
	filename='./jsonSmall/'+item
	#print item
	#feature=json2feature(filename)
	#print count_IC

	try:
		feature=json2feature(filename)
		if feature=="error":
			print feature
		else :
			pkl_file = file('./feature/'+item[:len(item)-5]+'.pkl','wb')     #文件保存在item.pkl中
			pickle.dump(feature, pkl_file)     #通过dump函数进行序列化处理
			pkl_file.close()
	except:
		
		#print item[:len(item)-5]
		errormessage.append(item[:len(item)-5])
	
	#print('./json/'+ item)
	#os.system(str)
print ("重复次数")
#print chongfucishu
print(len(FileList))
#print(os.getcwd())
print("出错文件数目")
print(len(errormessage))
print errormessage[0]
#print errormessage
pkl=file('error2.pkl','wb')
pickle.dump(errormessage,pkl)
pkl.close()
'''
filename='test.json'
json_data=open(filename)
data=json.load(json_data)
feature=dict()
for item in data["words"]:
	feature[item["word"]]=[item["stats"]["start"],item["stats"]["end"],item["stats"]["energy"]]
	print item["word"]
	#print item["stats"]["start"]
	#print item["stats"]["end"]
	#print type(item["stats"]["energy"])#float 类型  
print feature#经过实验验证engery是经过归一化的
#文件写入:
outname=filename[:len(filename)-5]+'.json'
print outname'''
'''output=open(outname,'w')
for key in feature:
	output.write(key)
output.write(feature)
output.close()
encodejson=json.dumps(feature)
print encodejson
#out=open(outname,'w')
	#out.write(encodejson)
#out.close()
pkl_file = file(filename[:len(filename)-5]+'.pkl','wb')     #文件保存在account.pkl中
pickle.dump(feature, pkl_file)     #通过dump函数进行序列化处理
pkl_file.close()'''
#解析pkl文件
'''
pkl_file = file(filename[:len(filename)-5]+'.pkl','rb')         #打开刚才存储的文件
account_dic = pickle.load(pkl_file)         #通过load转换回来
print account_dic
print type(account_dic)
pkl_file.close()'''
