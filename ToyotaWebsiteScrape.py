from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import time
import re

import ToyotaGetVin as t


with open("./ToyotaDealerURLs") as f:
    websiteLines = f.read().splitlines()
with open("./ToyotaDealerSearchpageURLs") as f:
    searchPageLines = f.read().splitlines()

hdr = {'User-Agent': 'Mozilla/5.0'}


for x in range(872, len(websiteLines)):
    if searchPageLines[x] == "none":
        continue
    
    file = open("VINs", "a")
    try:
        website = websiteLines[x]
        url = searchPageLines[x]

        urls = [] #this sites inventory webpages (page 1,2,...)
        urls.append(url) #pushes onto stack
        UniqueVins = []
        UniqueURLs = []

        while(len(urls) > 0):
            u = urls.pop()
            
            try:
                request = requests.get(u,headers=hdr,timeout=10)
                if u in UniqueURLs:
                    continue
                soup = BeautifulSoup(request.text,'html.parser')
            except:
                print("bad url")
                break
            UniqueURLs.append(u)
            
            output = []
            for link in soup.find_all('a', href=True):
                if "http" in str(link) and "20" in str(link): #a link usually has http and a link to a car usually has 20(year) in it
                    if link['href'] in output: #duplicate
                        continue
                    if website not in link['href']: #probably an ad (like carfax)
                        continue
                    output.append(link['href'])

            for o in output:
                a = t.getVinFromLink(o)
                if a == "none":
                    continue
                if a not in UniqueVins:
                    UniqueVins.append(a)
                    print(a)
                    file.write(a + ", " + website + ", " + o + "\n")
            
            #find next page
            for link in soup.find_all('a', href=True):
                if "next" in str(link) or "Next" in str(link):
                    urls.append(website + link['href'])
        print(len(UniqueVins) + "from: " + website)
    except:
        continue
    file.close()
