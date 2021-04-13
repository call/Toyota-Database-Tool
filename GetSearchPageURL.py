from bs4 import BeautifulSoup
import requests
import re

with open("C:/Users/schro/Downloads/CS3435/Project v2/ToyotaDealerURLs") as f:
    lines = f.read().splitlines()

hdr = {'User-Agent': 'Mozilla/5.0'}
for dealer in lines:
    url = dealer
    urls_A = []
    urls_B = []
    urls_C = []
    urls_D = []
    urls_All = [] #backup
    
    try:
        soup = BeautifulSoup(requests.get(url, headers = hdr, timeout=2).text,'html.parser')
    except:
        print(url + " timed out")
        continue
    for link in soup.find_all('a', href=True):
        if "20" in link['href']:                                    #likely a link to a 20__ year car
            continue
        
        makes = ["avalon", "camry", "corolla", "highlander", "rav4", "sequoia", "sienna", "tacoma", "tundra", "yaris"]
        if any(substring in link['href'].lower() for substring in makes):    #likely a link to a particular car
            continue
        
        urls_All.append(link)
        
        if url not in link['href']:                                 #likely a link to a different website
            continue
        
        #likely keywords for search page url
        if "search" in link['href'].lower() or "inventory" in link['href']:
            urls_A.append(link['href'])
        if "new" in link['href'].lower():
            urls_B.append(link['href'])
        if "vehicle" in link['href']:
            urls_C.append(link['href'])
        if link['href'].lower().count('toyota') > 1:
            urls_D.append(link['href'])
    
    if(len(urls_A) > 0):
        print(min(urls_A))
        continue
    if(len(urls_B) > 0):
        print(min(urls_B))
        continue
    if(len(urls_C) > 0):
        print(min(urls_C))
        continue
    if(len(urls_D) > 0):
        print(min(urls_D))
        continue
        
    #try links without the website as the header
    for link in urls_All:
        #likely keywords for search page url
        if "search" in link['href'].lower() or "inventory" in link['href']:
            urls_A.append(link['href'])
        if "new" in link['href'].lower():
            urls_B.append(link['href'])
        if "vehicle" in link['href']:
            urls_C.append(link['href'])
        if link['href'].lower().count('toyota') > 1:
            urls_D.append(link['href'])


    if(len(urls_A) > 0):
        print(dealer + min(urls_A))
        continue
    if(len(urls_B) > 0):
        print(dealer + min(urls_B))
        continue
    if(len(urls_C) > 0):
        print(dealer + min(urls_C))
        continue
    if(len(urls_D) > 0):
        print(dealer + min(urls_D))
        continue
    print("none")