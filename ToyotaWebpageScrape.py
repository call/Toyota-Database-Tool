from bs4 import BeautifulSoup
import requests
import re
import ToyotaGetSpecs

def printVars(vars):
        output = []
        for k in vars:
            output.append(k + ": " + str(vars[k]))
        print(output)
        return output

def getCar(link):
    response = requests.get(link)
    data = response.text

    soup = BeautifulSoup(data,'html.parser')
    text = soup.find_all(text=True)


    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style'
    ]

    Attributes = []
    for t in text:
        if t.parent.name not in blacklist:
            if not (t.isspace()):
                Attributes.append(t)



    #find vin
    def getVin():
        for a in Attributes:
            if re.search('[a-z]', a) or re.search('[!@#$\/\]]', a):
                continue
            if (len(a.replace(' ', '')) == 17):
                print(a)
                return a
            
    #find price
    def getPrice():
        for a in Attributes:
            if "Call For Price" in a:                       #If you have to call to get price, not valid
                return 0
            if len(a) > 7:                                  #If the number found is more than 7 digits, probably invalid
                continue
            if re.search("[$]", a):           
                return int(re.sub("[$,]",'',a))

    #find MPG
    def getMPG():
        mpgArr = []
        for a in Attributes:
            try:
                if re.search('[0-9]', a):           #is numeric, might contain the MPG
                    if "MPG" in a:                  #Best place to look
                        if "/" in a:                #probably a city/hwy combo
                            bs = a.split("/")
                            for b in bs:
                                mpgArr.append(int(re.sub("[a-z]|[A-Z]|[!@#$-/:]",'',b)))
                        else:
                            mpgArr.append(int(re.sub("[a-z]|[A-Z]|[!@#$-/:]",'',a)))
            except ValueError:
                continue
        return min(mpgArr), max(mpgArr) #city is most likely lower val, hwy is highest val

    v = getVin()
    c, h = getMPG()

    newCar = ToyotaGetSpecs.getSpecs(v)
    setattr(newCar, "Price", getPrice())
    setattr(newCar, "MPGCity", c)
    setattr(newCar, "MPGHWY", h)

    printVars(vars(newCar))
    return newCar