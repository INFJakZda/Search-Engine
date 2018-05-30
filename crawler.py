#import requests
from bs4 import BeautifulSoup
import urllib.request
import io
import re

checked = set()
with urllib.request.urlopen('https://www.nbcnews.com/politics/donald-trump') as response:
    soup = BeautifulSoup(response,"html5lib")
    links = soup.find_all('a')    
    #tweet = soup.find("p", class_="TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text")
    #import re
    #links = soup.find_all("a",href=re.compile("\.html"))
    #print(len(links))
    #for i in links[::2]:
    #    print(i['href'])
    for i in links:
        try:
            tmp = i['href']
            #print(tmp)
            if(re.search("n\d{6}$", tmp)):
            #if(tmp.startswith('/2018/')):
                checked.add(tmp)
        except:
            pass
    for i in checked:
        print(i)
        with urllib.request.urlopen('https://www.nbcnews.com/'+i) as one:
            wtf = BeautifulSoup(one.read().decode('utf-8'),"html5lib")
            articles = wtf.find_all('p')
            lel = ''
            for j in articles:
                lel+=j.get_text()
            f = io.open(i.split('/')[-1]+".txt", mode="w", encoding="utf-8")
            #f = open(i.split('/')[-1]+".txt", "w")
            f.write(lel)
            f.close()
