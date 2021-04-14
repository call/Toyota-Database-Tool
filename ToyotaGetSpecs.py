from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
import re
import json


class Car():
    def __init__(self, vin):
        self.Vin = vin

with open("C:/Users/schro/Downloads/CS3435/Project v2/VINs") as f:
    lines = f.read().splitlines()


driver = webdriver.Chrome("C:/Users/schro/Downloads/chromedriver_win32/chromedriver.exe")
driver.get("https://www.toyota.com/owners/my-vehicle/vehicle-specification")

v = "JTEBU5JR5L5738967"     #Test vin to reach search page

time.sleep(5)
inputElement = driver.find_element_by_id("vin")
inputElement.send_keys(v)     #first VIN
inputElement.send_keys(Keys.ENTER)
time.sleep(5)


for x in range(0, len(lines)):
    file = open("VINToyotaSpecs", "a")
    try:
        car = lines[x].split(", ")[0]
        if car == "none":
            continue
        newCar = Car(car)

        inputElement = driver.find_element_by_id("vin")
        for a in range(20): #clear textbox
            inputElement.send_keys("\b")
        inputElement.send_keys(car)
        inputElement.send_keys(Keys.ENTER)
        time.sleep(4)
        
        basics = driver.find_element_by_class_name("basic-details-section.larger-form-factor").text.split("\n")
        for index, b in enumerate(basics):
            if b == "Model":
                setattr(newCar, "Model", basics[index+1].split()[1])
                setattr(newCar, "Year", int(basics[index+1].split()[0]))
            if b == "Exterior":
                setattr(newCar, "Exterior", basics[index+1])
            if b == "Interior":
                setattr(newCar, "Interior", basics[index+1])
            if b == "Drive Type":
                setattr(newCar, "Drive Type", basics[index+1])
            if b == "Transmission":
                setattr(newCar, "Transmission", basics[index+1])
            if b == "Engine":
                setattr(newCar, "NumCylinders", int(re.sub("[A-Z]|[!@#$-]",'',basics[index+1])))
            if b == "Date of First Use":
                if basics[index+1] == "January 01, 0001":
                    setattr(newCar, "First Bought", "New")
                else:
                    setattr(newCar, "First Bought", basics[index+1])

        equipment = driver.find_element_by_class_name("sie-section").text
        setattr(newCar, "Equipment", equipment)

        setattr(newCar, "Website", lines[x].split(", ")[1])
        setattr(newCar, "Webpage", lines[x].split(", ")[2])

        print(vars(newCar))
        file.write(str(vars(newCar)) + "\n")

    except StaleElementReferenceException:
        pass
    
    except:
        pass

    file.close()