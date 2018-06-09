import io
import operator
import re
import matplotlib.pyplot as plt
import numpy as np

reLink = re.compile(r"http[^\s]*")
reMark = re.compile(r"[^a-zA-Z0-9\s]")
rePrefix = re.compile(r"'[a-z]+")
reRetweets = re.compile(r"@[^\s]+")
reSpace = re.compile(r"\s+")
reHashtags = re.compile(r"#[^\s]+")

sources = ['justRetweets','justLinks','justtext','noLinks','noRetweets']
#sourcesLens = sourcesLens()

def sourcesLens():
    sources = ['justRetweets','justLinks','justtext','noLinks','noRetweets']
    dict = {}
    for i in sources:
        data = io.open("justtext.txt", mode="r", encoding="utf-8")
        dict[i] = len(data.read())
        data.close
    return dict

stopWords = []
with open("stopWords.txt", "r") as stopFile:
    for i in stopFile:
        stopWords.append(i[:-1])

def prepare(myString):
    myString = myString.lower()
    myString = myString.replace(" &amp; ",' ')
    myString = reLink.sub('',myString)
    myString = rePrefix.sub('',myString)
    myString = reRetweets.sub('',myString)
    myString = reSpace.sub(' ',myString)
    myString = reMark.sub('',myString)
    return myString

def noLinks():
    data = io.open("justtext.txt", mode="r", encoding="utf-8")
    results = io.open("noLinks.txt", mode="w", encoding="utf-8")
    for i in data:
        if("http" not in i):
            results.write(i)
    data.close()
    results.close()

def justLinks():
    data = io.open("justtext.txt", mode="r", encoding="utf-8")
    results = io.open("justLinks.txt", mode="w", encoding="utf-8")
    for i in data:
        if("http" in i):
            results.write(i)
    data.close()
    results.close()
    
def noRetweets():
    data = io.open("justtext.txt", mode="r", encoding="utf-8")
    results = io.open("noRetweets.txt", mode="w", encoding="utf-8")
    for i in data:
        if(len(i)>1):
            if(i[0]!='@' and i[1]!='@' and i[:2]!='RT'):
                results.write(i)
    data.close()
    results.close()

def justRetweets():
    data = io.open("justtext.txt", mode="r", encoding="utf-8")
    results = io.open("justRetweets.txt", mode="w", encoding="utf-8")
    for i in data:
        if(len(i)>1):
            if(i[0]=='@' or i[1]=='@' or i[:2]=='RT'):
                results.write(i)
    data.close()
    results.close()

def prepareSources():
    noLinks()
    justLinks()
    noRetweets()
    justRetweets()

#tylko wypisuje, nie zapisuje
def countLinks(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    counterAll = 0
    links = 0
    for i in data:
        counterAll += 1
        links += i.count("http")
    print("Spośród "+source+" "+str(round(100*links/counterAll,2))+"% zawiera odnośniki,")
    data.close()

#tylko wypisuje, nie zapisuje
def meanTweet(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    counter = 0 
    chars = 0
    words = 0
    for i in data:
        tmp = prepare(i)
        counter += 1
        chars += len(tmp)
        words += len(tmp.split())
    print('Średnia długość "treści" tweeta spośród '+source+' wynosi '+str(round(chars/counter,2))+" znaków lub średnio "+str(round(words/counter,2))+" słów")
    #print('"'+''.join([' ' for i in range(int(chars/counter))])+'"')
    #print("^czyli mniej więcej tyle")
    data.close()

#tylko wypisuje, nie zapisuje
def sourcesShare():
    data = io.open("justtext.txt", mode="r", encoding="utf-8")
    tmp = len(data.read())
    sources = ['justRetweets','justLinks','noLinks','noRetweets']
    for i in sources:
        results = io.open(i+".txt", mode="r", encoding="utf-8")
        print(i+" stanowi "+str(round(100*len(results.read())/tmp,2))+"% wszystkich tweetów")
        results.close()
    data.close()

def countMultiple(words, source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("countMultiple.txt", mode="w", encoding="utf-8")
    dict = {}
    for i in words:
        dict[i]=0
    for i in data:
        tmp = prepare(i)
        for word in words:
            if(word in tmp):
                dict[word] += 1        
    for i in words:
        results.write(i+": "+str(dict[i])+"\n")
    results.close()
    data.close()

#tylko wypisuje, nie zapisuje
def countSingle(word, source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    counter = 0    
    for i in data:
        tmp = prepare(i)
        if(word in tmp):
            counter += 1
    print(word+": "+str(counter))
    data.close()

def prevWord(word, source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("prev_"+word+".txt", mode="w", encoding="utf-8")
    dict = {}
    for i in data:
        tmp = prepare(i).split()
        if(word in tmp):
            try:
                x = tmp[tmp.index(word)-1]
                if(x in dict):
                    dict[x] += 1
                else:
                    dict[x] = 1
            except:
                pass

    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))[::-1]
    print(word)
    for i in sorted_dict:
        if(i[1]<2):
            break
        if(i[0] not in stopWords):
            print(i)
            results.write(str(i)+"\n")
    results.close()
    data.close()

def prev2Words(word, source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("prev2_"+word+".txt", mode="w", encoding="utf-8")
    dict = {}
    for i in data:
        tmp = prepare(i).split()
        if(word in tmp):
            try:
                x = ' '.join(tmp[tmp.index(word)-2:tmp.index(word)])
                if(x in dict):
                    dict[x] += 1
                else:
                    dict[x] = 1
            except:
                pass

    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))[::-1]
    print(word)
    for i in sorted_dict:
        if(i[1]<2):
            break
        x = i[0].split()
        try:
            if(x[0] not in stopWords and x[1] not in stopWords):
                print(i)
                results.write(str(i)+"\n")
        except:
            pass
    results.close()
    data.close()

def nextWord(word, source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("next_"+word+".txt", mode="w", encoding="utf-8")
    dict = {}
    for i in data:
        tmp = prepare(i).split()
        if(word in tmp):
            try:
                x = tmp[tmp.index(word)+1]
                if(x in dict):
                    dict[x] += 1
                else:
                    dict[x] = 1
            except:
                pass

    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))[::-1]
    print(word)
    for i in sorted_dict:
        if(i[1]<2):
            break
        if(i[0] not in stopWords):
            print(i)
            results.write(str(i)+"\n")
    results.close()
    data.close()

def next2Words(word, source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("next2_"+word+".txt", mode="w", encoding="utf-8")
    dict = {}
    for i in data:
        tmp = prepare(i).split()
        if(word in tmp):
            try:
                x = ' '.join(tmp[tmp.index(word)+1:tmp.index(word)+3])
                if(x in dict):
                    dict[x] += 1
                else:
                    dict[x] = 1
            except:
                pass
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))[::-1]
    print(word)
    for i in sorted_dict:
        if(i[1]<2):
            break
        x = i[0].split()
        try:
            if(x[0] not in stopWords and x[1] not in stopWords):
                print(i)
                results.write(str(i)+"\n")
        except:
            pass
    results.close()
    data.close()
    
def wordsSimilarity(first,second, source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open(first+"VS"+second+".txt", mode="w", encoding="utf-8")
    count_first = 0
    count_second = 0
    count_both = 0
    for i in data:
        tmp = prepare(i)
        """
        if("hillary" in tmp or "clinton" in tmp or "hilary" in tmp):
            count_first += 1
        if("email" in tmp):
            count_second += 1
        if(("hillary" in tmp or "clinton" in tmp or "hilary" in tmp) and "email" in tmp):
            count_both += 1
        """
        if(first in tmp):
            count_first += 1
        if(second in tmp):
            count_second += 1
        if(first in tmp and second in tmp):
            count_both += 1
        
    #print(first+": "+str(count_first)+"\n"+second+": "+str(count_second)+"\nboth:"+str(count_both)) 
    results.write(first+": "+str(count_first)+"\n"+second+": "+str(count_second)+"\nboth:"+str(count_both))                
    #print('Postać Hillary Clinton pojawia się w '+str(round(100*count_both/count_second,2))+"% tweetów dotyczących e-maili")
    #results.write('Postać Hilary Clinton pojawia się w '+str(100*count_both/count_second)+"% tweetów dotyczących emaili")
    results.close()
    data.close()

def wordsSimilarity2(firsts,seconds, source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open(firsts[0]+"V2S"+seconds[0]+".txt", mode="w", encoding="utf-8")
    count_first = 0
    count_second = 0
    count_both = 0
    for i in data:
        tmp = prepare(i)
        
        flagFirst = False
        for first in firsts:
            if(first in tmp):
                flagFirst = True
        if(flagFirst):
            count_first += 1
            
        flagSecond = False
        for second in seconds:
            if(second in tmp):
                flagSecond = True
        if(flagSecond):
            count_second += 1
            
        if(flagSecond and flagFirst):
            count_both += 1
        
    #print(','.join(firsts)+": "+str(count_first)+"\n"+','.join(seconds)+": "+str(count_second)+"\nboth:"+str(count_both)) 
    results.write(','.join(firsts)+": "+str(count_first)+"\n"+','.join(seconds)+": "+str(count_second)+"\nboth:"+str(count_both)) 
    #print('Postać Hillary Clinton pojawia się w '+str(round(100*count_both/count_second,2))+"% tweetów dotyczących e-maili")
    #results.write('Postać Hilary Clinton pojawia się w '+str(100*count_both/count_second)+"% tweetów dotyczących emaili")
    results.close()
    data.close()
"""
def wtf():
    data = io.open("justtext.txt", mode="r", encoding="utf-8")
    results = io.open("tmp.txt", mode="w", encoding="utf-8")
    mySet = set()
    for i in data:
        mySet.add(i)
    for i in sorted(mySet):
        myString = i
        myString = myString.replace(" &amp; ",' ')
        myString = reLink.sub('',myString)
        myString = reSpace.sub(' ',myString)
        results.write(myString.strip('.').strip(' ')+'\n')
    data.close()
    results.close()
"""
def process():
    data = io.open("justtext.txt", mode="r", encoding="utf-8")
    results = io.open("processed.txt", mode="w", encoding="utf-8")
    mySet = set()
    for i in data:
        mySet.add(i)
    for i in sorted(mySet):
        myString = prepare(i).strip().replace("rt ",'')+'\n'
        if(len(myString)>10):
            results.write(myString)
    data.close()
    results.close()
process()

def countThanks(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    counter = 0
    dict = {}
    dict2 = {}
    for i in data:
        if(i.startswith('Thank')):
           counter += 1
           try:
               tmp = reMark.sub('',i).split()[2]
               if(tmp in dict):
                   dict[tmp] += 1
               else:
                   dict[tmp] = 1
           except:
               pass
           try:
               tmp = ' '.join(reMark.sub('',i).split()[2:4])
               if(tmp in dict2):
                   dict2[tmp] += 1
               else:
                   dict2[tmp] = 1
           except:
               pass
    print(counter,' tweets started with "Thank(s) you ..."')
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))[::-1]
    for i in sorted_dict:
        if(i[1]<2):
            break
        if(i[0] not in stopWords):
            print(i)
            #results.write(str(i)+"\n")
    sorted_dict2 = sorted(dict2.items(), key=operator.itemgetter(1))[::-1]
    for i in sorted_dict2:
        if(i[1]<2):
            break
        x = i[0].split()
        try:
            if(x[0] not in stopWords and x[1] not in stopWords):
                print(i)
                #results.write(str(i)+"\n")
        except:
            pass
    data.close()

def countUsers(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    dict = {}
    nTweets = 0
    nUsers = 0
    for line in data:
        nTweets += 1
        users = reRetweets.findall(line)
        if users:
            nUsers += 1
        for user in users:
            if(user in dict):
                dict[user] += 1
            else:
                dict[user] = 1
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))[::-1]
    print("W tweetach jest mowa o ",len(dict)," róznych użytkownikach twittera")
    print(round(100*nUsers/nTweets,2),"% tweetów zawiera nawiązanie do innego użytkownika")
    for i in sorted_dict:
        if(i[1]<100):
            break
        #print(i)
        #results.write(str(i)+"\n")
    data.close()

def countHashtags(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    dict = {}
    nTweets = 0
    nHashtags = 0
    for line in data:
        nTweets += 1
        hashtags = reHashtags.findall(line)
        if hashtags:
            nHashtags += 1
        for hashtag in hashtags:
            if(hashtag in dict):
                dict[hashtag] += 1
            else:
                dict[hashtag] = 1
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))[::-1]
    print("W tweetach jest mowa o",len(dict),"róznych hashtagach")
    print(round(100*nHashtags/nTweets,2),"% tweetów zawiera jakiś hashtag")
    for i in sorted_dict:
        if(i[1]<50):
            break
        #print(i)
        #results.write(str(i)+"\n")
    data.close()

def justQuotes(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("justQuotes.txt", mode="w", encoding="utf-8")
    for i in data:
        if(len(i)>1):
            if(i[0]=='"' and i[1]!='@'):
                results.write(i)
    data.close()
    results.close()

def tweetHistogram(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    dict = {}
    for i in data:
        tmp = len(prepare(i))
        #tmp = len(i)
        if(tmp in dict):
            dict[tmp] += 1
        else:
            dict[tmp] = 1
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(0))
    for i in sorted_dict:
        print("Długość tweeta:",i[0]," ilość tweetów o takiej długości:",i[1])
    data.close()

def countOneWord(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    dict = {}
    for i in data:
        if(len(i.split())==1):
            tmp = i[:-1]
            if(tmp in dict):
                dict[tmp] += 1
            else:
                dict[tmp] = 1
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))[::-1]
    print("Liczba wszystkich jednosłownych tweetów:",sum(dict.values()))
    for i in sorted_dict:
        if(i[1]<2):
            break
        print("Treść tweeta:",i[0]," ilość takich tweetów:",i[1])
    data.close()

batman = 123
