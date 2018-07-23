import io
import operator
import re
import matplotlib.pyplot as plt
import numpy as np
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

reLink = re.compile(r"http[^\s]*")
reMark = re.compile(r"[^a-zA-Z0-9\s]")
rePrefix = re.compile(r"'[a-z]+")
reRetweets = re.compile(r"@[^\s]+")
reSpace = re.compile(r"\s+")
reHashtags = re.compile(r"#[^\s]+")
reQuotes = re.compile(r"[–|-] [A-Z][a-z]+ [A-Z][a-z]+$")

sources = ['justQuotes','justRetweets','justLinks','justtext','noLinks','noRetweets']
#sourcesLens = sourcesLens()

def sourcesLens():
    sources = ['justQuotes','justRetweets','justLinks','justtext','noLinks','noRetweets']
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
    global porter_stemmer
    global wordnet_lemmatizer
    #myString = myString.lower()
    myString = myString.replace(" &amp; ",' ')
    myString = myString.replace("RT ",'')
    myString = reLink.sub('',myString)
    myString = rePrefix.sub('',myString)
    myString = reRetweets.sub('',myString)
    myString = reHashtags.sub('',myString)
    myString = reSpace.sub(' ',myString)
    myString = reMark.sub('',myString)
    #myString = ' '.join([wordnet_lemmatizer.lemmatize(i) for i in myString.split()])
    myString = ' '.join([porter_stemmer.stem(i) for i in myString.split()])
    return myString

def justtext():
    data = io.open("raw.txt", mode="r", encoding="utf-8")
    results = io.open("justtext.txt", mode="w", encoding="utf-8")
    for i in data:
        tmp = i.split(',')
        results.write(','.join(tmp[1:-5])+'\n')
    results.close()        
    data.close()

def justQuotes(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("justQuotes.txt", mode="w", encoding="utf-8")
    for i in data:
        if reQuotes.findall(i):
            results.write(i)
        #if(len(i)>1):
        #    if(i[0]=='"' and i[1]!='@'):
        #        results.write(i)
    data.close()
    results.close()

def clean(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("clean.txt", mode="w", encoding="utf-8")
    for i in data:
        tmp = prepare(i)
        while(tmp.startswith('.') or tmp.startswith(' ')):
              tmp = tmp.strip('.').strip(' ')
        if(len(tmp)>0):
            results.write(tmp+'\n')
    data.close()
    results.close()

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
            if(i[:2]=='RT'):
                results.write(i)
    data.close()
    results.close()

def prepareSources():
    noLinks()
    justLinks()
    noRetweets()
    justRetweets()
    justQuotes()

#tylko wypisuje, nie zapisuje
def meanTweet(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("results.txt", mode="a", encoding="utf-8")
    counter = 0 
    chars = 0
    words = 0
    for i in data:
        tmp = prepare(i)
        counter += 1
        chars += len(tmp)
        words += len(tmp.split())
    print('Średnia długość "treści" tweeta spośród '+source+' wynosi '+str(round(chars/counter,2))+" znaków lub średnio "+str(round(words/counter,2))+" słów\n")
    results.write('Średnia długość "treści" tweeta spośród '+source+' wynosi '+str(round(chars/counter,2))+" znaków lub średnio "+str(round(words/counter,2))+" słów\n")
    #print('"'+''.join([' ' for i in range(int(chars/counter))])+'"')
    #print("^czyli mniej więcej tyle")
    results.close()
    data.close()

#tylko wypisuje, nie zapisuje
def sourcesShare():
    data = io.open("justtext.txt", mode="r", encoding="utf-8")
    tmp = len(data.read())
    sources = ['justQuotes','justRetweets','justLinks','noLinks','noRetweets']
    for i in sources:
        arg = io.open(i+".txt", mode="r", encoding="utf-8")
        results = io.open("results.txt", mode="a", encoding="utf-8")
        #print(i+" stanowi "+str(round(100*len(arg.read())/tmp,2))+"% wszystkich tweetów\n")
        results.write(i+" stanowi "+str(round(100*len(arg.read())/tmp,2))+"% wszystkich tweetów\n")
        results.close()
        arg.close()
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

def prevWord(word, source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open(word+".txt", mode="w", encoding="utf-8")
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
    results = io.open(word+".txt", mode="a", encoding="utf-8")
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
    results = io.open(word+".txt", mode="a", encoding="utf-8")
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
    results = io.open(word+".txt", mode="a", encoding="utf-8")
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

def countThanks(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("results.txt", mode="a", encoding="utf-8")
    counter = 0
    dict = {}
    dict2 = {}
    for i in data:
        if(i.startswith('thank')):
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
    print(counter,' tweets started with "Thank(s) you ..."\n')
    results.write("Spośród "+source+str(counter)+' niepowtarzalnych tweetów zaczyna się od "Thank(s) you ..."\n')
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))[::-1]
    for i in sorted_dict:
        if(i[1]<5):
            break
        if(i[0] not in stopWords):
            print(i)
            results.write(str(i)+"\n")
    sorted_dict2 = sorted(dict2.items(), key=operator.itemgetter(1))[::-1]
    for i in sorted_dict2:
        if(i[1]<3):
            break
        x = i[0].split()
        try:
            if(x[0] not in stopWords and x[1] not in stopWords):
                print(i)
                results.write(str(i)+"\n")
        except:
            pass
    data.close()
    results.close()

def countUsers(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("results.txt", mode="a", encoding="utf-8")
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
    print(source)
    print("W tweetach jest mowa o "+str(len(dict))+" róznych użytkownikach twittera\n")
    print(round(100*nUsers/nTweets,2),"% tweetów zawiera nawiązanie do innego użytkownika\n")
    results.write(source)
    results.write("W tweetach jest mowa o "+str(len(dict))+" róznych użytkownikach twittera\n")
    results.write(str(round(100*nUsers/nTweets,2))+"% tweetów zawiera nawiązanie do innego użytkownika\n")
    for i in sorted_dict:
        if(i[1]<100):
            break
        print(i)
        results.write(str(i)+"\n")
    data.close()
    results.close()

def countHashtags(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("results.txt", mode="a", encoding="utf-8")
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
    print(source)
    print("W tweetach jest mowa o"+str(len(dict))+"róznych hashtagach\n")
    print(round(100*nHashtags/nTweets,2),"% tweetów zawiera jakiś hashtag\n")
    results.write(source)
    results.write("W tweetach jest mowa o"+str(len(dict))+"róznych hashtagach\n")
    results.write(str(round(100*nHashtags/nTweets,2))+"% tweetów zawiera jakiś hashtag\n")
    for i in sorted_dict:
        if(i[1]<50):
            break
        print(i)
        results.write(str(i)+"\n")
    data.close()
    results.close()

def tmp(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("tmp.txt", mode="w", encoding="utf-8")
    mySet = set()
    for i in data:
        mySet.add(i.strip()+'\n')
    for i in sorted(mySet):
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

def countFirstWord(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    results = io.open("results.txt", mode="a", encoding="utf-8")
    dict = {}
    dict2 = {}
    counter = 0
    for i in data:
        if(len(i.split())>0):
            tmp = i.split()[0]
            if(tmp in dict):
                dict[tmp] += 1
            else:
                dict[tmp] = 1
        if(len(i.split())==1):
            if(tmp in dict2):
                dict2[tmp] += 1
            else:
                dict2[tmp] = 1
    results.write("Liczba wszystkich jednosłownych tweetów:"+str(len(dict2))+'\n')
    sorted_dict2 = sorted(dict2.items(), key=operator.itemgetter(1))[::-1]
    #print("Liczba wszystkich jednosłownych tweetów:",sum(dict.values()))
    results.write("Jedyne słowo tweeta: ilość takich tweetów:\n")
    for i in sorted_dict2:
        if(i[0] not in stopWords):
            #print("Jedyne słowo tweeta:",i[0]," ilość takich tweetów:",i[1])
            results.write(str(i)+'\n')    
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))[::-1]
    #print("Liczba wszystkich jednosłownych tweetów:",sum(dict.values()))
    results.write("Pierwsze słowo tweeta: ilość tak zaczynających się tweetów:\n")
    for i in sorted_dict:
        if(i[1]<100):
            break
        if(i[0] not in stopWords):
            #print("Pierwsze słowo tweeta:",i[0]," ilość tak zaczynających się tweetów:",i[1])
            results.write(str(i)+'\n')
    data.close()
    results.close()
    
def countFirstWord2(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    #results = io.open("results.txt", mode="a", encoding="utf-8")
    dict = {}
    dict2 = {}
    counter = 0
    for i in data:
        if(len(i.split())>1):
            first = i.split()[0:2]
            if(first[0] not in stopWords and first[1] not in stopWords):
                tmp = ' '.join(first)
                if(tmp in dict):
                    dict[tmp] += 1
                else:
                    dict[tmp] = 1
        if(len(i.split())==2):
            if(tmp in dict2):
                dict2[tmp] += 1
            else:
                dict2[tmp] = 1
    #results.write("Liczba wszystkich dwusłownych tweetów:"+str(len(dict2))+'\n')
    sorted_dict2 = sorted(dict2.items(), key=operator.itemgetter(1))[::-1]
    #results.write("Jedyne dwa słowa tweeta: ilość takich tweetów:\n")
    #print("Jedyne dwa słowa tweeta: ilość takich tweetów:")
    for i in sorted_dict2:
        if(i[1]<2):
            break
        if(i[0] not in stopWords):
            pass
            #print(i)
            #results.write(str(i)+'\n')
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))[::-1]
    #print("Pierwsze dwa słowa tweeta: ilość tak zaczynających się tweetów:")
    #results.write("Pierwsze dwa słowa tweeta: ilość tak zaczynających się tweetów:\n")
    for i in sorted_dict:
        if(i[1]<50):
            break
        if(i[0] not in stopWords):
            print(i)
            #results.write(str(i)+'\n')
    data.close()
    #results.close()

def countWords(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    #results = io.open(first+"VS"+second+".txt", mode="w", encoding="utf-8")
    dict = {}
    for i in data:
        j = prepare(i).split()
        for tmp in j:
            if(tmp in dict):
                dict[tmp] += 1
            else:
                dict[tmp] = 1
    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))[:-50:-1]
    for i in sorted_dict:
        if(i[0] not in stopWords):
            print(i)
    
batman = 123
def splitTweets(source='justtext'):
    data = io.open(source+".txt", mode="r", encoding="utf-8")
    counter = 0
    for i in data:
        results = io.open(str(counter)+".txt", mode="w", encoding="utf-8")
        results.write(i[:-1])
        results.close()
        break
    data.close()
print(prepare("The Fake Mainstream Media has from the time I announced I was running for President run the most highly sophisticated &amp; dishonest Disinformation Campaign in the history of politics. No matter how well WE do they find fault. But the forgotten men &amp; women WON I'm President!"))
"""
countFirstWord2('proccessed')
results = io.open("results.txt", mode="w", encoding="utf-8")
results.close()
prepareSources()
sourcesShare()
meanTweet()
countThanks('proccessed')
countUsers()
countHashtags()
countFirstWord('proccessed')
countFirstWord2('proccessed')

myList = ['donald',
          'trump',
          'hillary',
          'clinton',
          'barack',
          'obama',          
          'putin',
          'russia',
          'china',
          'chinese',
          'ivanka',
          'korea',
          'america',
          'war',
          'bomb',
          'syria',
          'iraq',
          'wall',
          'border',
          'mexico',
          'mexican',
          'poland']
countMultiple(myList,'proccessed')
"""
          
          
