#!/usr/bin/env python
#encoding=utf-8
import os
import json
import csv
import pickle

def csv2list(filename):
    listout=[]
    with open(filename) as f:
        reader=csv.reader(f)
        for row in reader:
            listout.append(row)
    return listout

def stress_form_json(filename,word):
    json_data=open(filename)
    data=json.load(json_data)
    for worditem in data["words"]:
        #print worditem
        if worditem["word"] == word:
           # print word,worditem
            return worditem["stats"]["stress_pattern"]
        

filedir='./jsonCheck/51a0da0efcfff22a5a0031a2.json'
filedir1='./jsonCheck/51a0da0efcfff22a5a0031a4.json'
json_data=open(filedir1)
data=json.load(json_data)
#print data
#print type(data)#dict
print "data[words]的格式:",type(data["words"])
# 下面json解析成功
for worditem in data["words"]:
    #print item
    #print type(worditem)#dict
    print worditem["word"],type(worditem["word"])
   # print worditem["stats"],type(worditem["stats"])
    print worditem["stats"]["stress_pattern"]

csvFile=csv2list('filename_trans.csv')
wenjianming=[]
juzi=[]
for item in csvFile:
    wenjianming.append(item[0])
    juzi.append(item[1])

#print wenjianming
#print len(juzi)

pkl_file=file('Label.pkl','r')
LabelRaw=pickle.load(pkl_file)
pkl_file.close()
#print LabelRaw
count = 0
countL3=0
countM3=0
countP3=0
countM0=0
errorcount=0
countA=0
error01=0
error10=0
countE=0
LabelRaw[13][200][1]='mp3/510d38d4fcfff2fc6d000543.mp3'
for item in LabelRaw:
    iter = 0
    for item1 in item:
        iter += 1
        if iter%2 !=0:
            if item1[1] in wenjianming:
                filename= './jsonCheck/'+item1[1][4:29]+'json'
                #print filename
                #print item1[2]
                #print item[iter-1]#单词
                #print item[iter]#标注
                for worditer in range(len(item[iter-1])):
                    #print len(item[iter-1][worditer])
                    if len(item[iter-1][worditer])>0:
                       # print item[iter-1][worditer]
                        try:
                           #print item[iter-1][worditer],stress_form_json(filename,item[iter-1][worditer]),item[iter][worditer]
                           if item[iter][worditer]=='3'or item[iter][worditer]=='' or item[iter][worditer]==' ' :
                               countL3+=1
                               #print item[iter-1][worditer]
                               #下面的代码验证了程序的正确性，现在被注释掉，因为想做一些其他工作
                              # if stress_form_json(filename,item[iter-1][worditer])==1:
                              #     countM3+=1
                              # elif stress_form_json(filename,item[iter-1][worditer])==0:
                              #     countM0+=1
                              # else:
                              #     countE+=1#print item[iter][worditer],stress_form_json(filename,item[iter-1][worditer])
                              # if stress_form_json(filename,item[iter-1][worditer])==1 and item[iter][worditer]=='3':
                              #     countP3+=1
                              # if stress_form_json(filename,item[iter-1][worditer])==0 and (item[iter][worditer]==' ' or item[iter][worditer]==''):
                              #     countA+=1
                              # if stress_form_json(filename,item[iter-1][worditer])==0 and item[iter][worditer]=='3':
                              #     error01+=1
                              # if stress_form_json(filename,item[iter-1][worditer])==1 and (item[iter][worditer]==' ' or item[iter][worditer]==''):
                              #     error10+=1

                        except :
                           errorcount+=1   

print count
print errorcount
#print countM3,countM0,countL3,countE
print countL3,countM3,countP3,countA,countE
#print error01,error10
#print "Percision:" ,float(countP3)/float(countM3)
print "accuracy:",float(countP3+countA)/float(countL3-countE)

#提取好的样本和不好的样本

pkl_file1=file('./bob/outsentenceB.pkl','r')
#print pkl_file1.read()
Bad=pickle.load(pkl_file1)
pkl_file1.close()

#pkl_file=file('Label.pkl','r')
#LabelRaw=pickle.load(pkl_file)

pkl_file2=file('./bob/outsentenceB.pkl','r')
Good=pickle.load(pkl_file2)
pkl_file2.close()


print Bad
print Good

def list2txt(list1,list2,f):
    for iter in range(len(list1)):
        if iter >1 and len(list1[iter])>0:
            f.write(list1[iter]+'\t')
            if list2[iter]=='' or list2[iter]==' ':
                f.write(str(0)+'\n')
            else :
                f.write(str(list2[iter])+'\n')
    f.close()

def sample2file(filedir,f):
    json_data=open(filedir)
    data=json.load(json_data)
    for worditem in data["words"]:
        f.write(str(worditem["word"])+'\t')
        f.write(str(worditem["stats"]["stress_pattern"])+'\n')
    f.close()
    #print item
    #print type(worditem)#dict
        #print worditem["word"],type(worditem["word"])
   # print worditem["stats"],type(worditem["stats"])
        #print worditem["stats"]["stress_pattern"]
        

for item in LabelRaw:
    iter = 0
    for item1 in item:
        iter += 1
        if iter%2 !=0:
            if item1[1] in wenjianming:
                #filename= './jsonCheck/'+item1[1][4:29]+'json'
                for itemGood in Good:
                    if item1[1][4:28]==itemGood:
                        filename= './jsonCheck/'+item1[1][4:29]+'json'
                        #print itemGood
                        name=item1[1][4:28]
                        cmd='mkdir ./Good/'+name
                        os.system(cmd)
                        #print name
                        print filename
                        cmd='cp ./mp3/'+name+'.mp3 ./Good/'+name+'/'
                        os.system(cmd)
                        f1=open('./Good/'+name+'/Model.txt','wb')
                        sample2file(filename,f1)
                        #写入模型
                        f2=open('./Good/'+name+'/Lable.txt','wb')
                        #print item[iter-1],item[iter]
                        #print type(item[iter-1]),type(item[iter])
                        list2txt(item[iter-1],item[iter],f2)
                        #f2.write(item[iter-1]+'\n')
                        #f2.write(item[iter])
                        #f2.close()
                for itemBad in Bad:
                    if item1[1][4:28]==itemBad:
                        filename= './jsonCheck/'+item1[1][4:29]+'json'
                        name=item1[1][4:28]
                        cmd='mkdir ./Bad/'+name
                        os.system(cmd)
                        #print name
                        print filename
                        cmd='cp ./mp3/'+name+'.mp3 ./Bad/'+name+'/'
                        os.system(cmd)
                        f1=open('./Bad/'+name+'/Model.txt','wb')
                        sample2file(filename,f1)
                        #写入模型
                        f2=open('./Bad/'+name+'/Lable.txt','wb')
                        #print item[iter-1],item[iter]
                        #print type(item[iter-1]),type(item[iter])
                        list2txt(item[iter-1],item[iter],f2)

