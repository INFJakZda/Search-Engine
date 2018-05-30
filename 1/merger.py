import glob
import io
import re
import operator
import string
import os
import glob

res = io.open("all.txt", mode="w", encoding="utf-8")
for file in glob.glob("*.txt"):
    f = io.open(file, mode="r", encoding="utf-8")    
    for line in f:
        filter(lambda x: x in string.printable, line)
        res.write(line)
    f.close()
res.close()
"""
        res.write(line)
f.close()
res.close()
    for i in replaceList:
        words = words.replace(i,"")
    for i in words.lower().split():
        if(i in dict):
            dict[i]+=1
        else:
            dict[i]=1
    #tab.append(','.join(tmp[1:-5]))
    #if(','.join(tmp[1:-5])==''):
    #    print(line)

dict1 = {}
dict2 = {}
for i in range(2009,2019):
    dict2[str(i)]=0
for line in f:
    tmp = line.split(',')
    if(tmp[0] in dict1):
        dict1[tmp[0]]+=1
    else:
        dict1[tmp[0]]=1
    dict2[re.search( r'(\d{4})', tmp[-5]).group()]+=1
    #res.write(','.join(tmp[1:-5])+'\n')
for i in dict1:
    print(i,dict1[i])
for i in dict2:
    print(i,dict2[i])

#print(sorted(tab,key=foo)[0:21])
sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))[::-1]
print(sorted_dict[:101])
"""

