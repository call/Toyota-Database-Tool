from bs4 import BeautifulSoup
import requests
import re


#find vin on webpage
def getVinFromPage(link):
    soup = BeautifulSoup(requests.get(link).text,'html.parser')
    text = soup.find_all(text=True)

    blacklist = ['[document]','noscript','header','html','meta','head','input','script','style']
    Attributes = []
    for t in text:
        if t.parent.name not in blacklist:
            if not (t.isspace()):
                Attributes.append(t)
                
    
    vins = []
    for a in Attributes:
        if re.search('[a-z]', a) or re.search('[!@#$\/\-]]', a) or not re.search('[0-9]', a):
            continue
        if (len(a.replace(' ', '')) == 17):
            vins.append(a)
    return vins
    
#find vin in url
def getVinFromLink(link):
    a = link[-17:]
    if re.search('[!@#$\/\-]]', a) or not re.search('[0-9]', a) or re.search('[a-z]', a):
        return "none"
    else:
        return a