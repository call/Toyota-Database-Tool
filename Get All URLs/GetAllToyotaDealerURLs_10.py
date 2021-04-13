from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import numpy as np

#Field(s)
threadNumber = 10
threadTotal = 10
numZipcodes = 41729
y = np.array_split(np.arange(numZipcodes), threadTotal)
ThreadZipcodes = y[threadNumber-1]


#access zipcode search
driver = webdriver.Chrome("C:/Users/schro/Downloads/chromedriver_win32/chromedriver.exe")
driver.get("https://www.toyota.com/dealers/")
inputElement = driver.find_element_by_name("zipcode")


#get all US zipcodes from local file
with open("C:/Users/schro/Downloads/CS 3435/Zipcodes") as f:
    lines = f.read().splitlines()

#Enter 1st valid zipcode to remove banner
inputElement.send_keys('\b\b\b\b\b')
inputElement.send_keys('00501')
inputElement.send_keys(Keys.ENTER)


#give webpage time to react
time.sleep(1)


f2 = open("C:/Users/schro/Downloads/CS 3435/ToyotaDealerShipURLData" + str(threadNumber), "a")
pattern = "href=\"(.*?)\" target"

#FIRST
urlArr = driver.find_elements_by_class_name("cta-btns")


#Adds the URL for each zipcode when called to file
def appendURLs(num, dealership):
    x = urlArr[dealership].get_attribute('innerHTML')
    newURL = re.search(pattern, x).group(1)
    print(newURL)
    f2.write(str(num) + ", " + newURL + "\n")


#--------


for dealership in range(len(urlArr)):
    appendURLs(0, dealership)


#loop through every zipcode,
#search through the other searchbar 
#at the top for that zipcode


#temporarily start at 1000 because most 00XXX are nonexistent
for num in ThreadZipcodes:
    print(lines[num])
    inputElement = driver.find_element_by_class_name("react-autosuggest__input")
    inputElement.send_keys('\b\b\b\b\b')
    inputElement.send_keys(lines[num])
    inputElement.send_keys(Keys.ENTER)
    
    #get all urls, write to file
    urlArr = driver.find_elements_by_class_name("cta-btns")
    for dealership in range(len(urlArr)):
        try:
            appendURLs(num, dealership)
        except:
            print("no deals")
    
    time.sleep(1)
f2.close()
