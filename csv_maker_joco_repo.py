
from bs4 import BeautifulSoup
from selenium import webdriver
import string
import copy
import datetime


#set up chrome webdriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("C:/Users/jsmcf/OneDrive/Documents/Programming/chromedriver", options=options)

url = "https://jocoreport.com/jcr-mugstest/index7days.htm"

driver.get(url)
driver.implicitly_wait(100)
#home page is empty
driver.find_element_by_id("button_next").click()

class Person():
    def __init__(self, name, sex, age, height, weight, city, date, arrestedBy, charge):
        self.name = name.replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").strip()
        self.sex = sex
        self.age = age
        self.height = height[0]+"'"+height[1:3]+"\""
        self.weight = weight
        self.city = city.strip()
        self.date = date
        self.arrestedBy = arrestedBy
        self.charge = charge.replace(",","-")
    def update_info(self, person):
        self = copy.copy(person)
    def printVals (self):
        return str(self.name)+","+str(self.sex)+","+str(self.age)+","+str(self.height)+","+str(self.weight)+","+str(self.city)+","+str(self.date)+","+str(self.arrestedBy)+","+str(self.charge)+"\n"
    
nameDict = {}
persons = []
dupCount = 0
iNameDict = 0

#the database does not have a count of the webpages. There are multiple duplicates
#READ PAGES
while (dupCount < 3):
    html = driver.page_source
    #get basic html and beautify it
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    #index where in text the data of interest is
    nameIndx = text.find("Name: ") + len("Name: ")
    sexIndx = text.find("Sex: ") + len("Sex: ")
    ageIndx = text.find("Age: ") + len("Age: ")
    heightIndx = text.find("Height: ") + len("Height: ")
    weightIndx = text.find("Weight: ") + len("Weight: ")
    cityIndx = text.find("From: ") + len("From ")
    dateIndx = text.find("Arrest Date: ") + len("Arrest Date: ")
    arrestedbyIndx = text.find("Arrested By: ") + len("Arrested By: ")
    chargesIndx = text.find("Charges: ") + len("Charges: ")

    #add each page to a list of persons
    tempPerson = Person(text[nameIndx:text.find("\n",nameIndx)], text[sexIndx:text.find("\n",sexIndx)],
        text[ageIndx:text.find("\n",ageIndx)], text[heightIndx:text.find("\n",heightIndx)],
        text[weightIndx:text.find("\n",weightIndx)], text[cityIndx:text.find("\n",cityIndx)],
        text[dateIndx:text.find("\n",dateIndx)], text[arrestedbyIndx:text.find("\n",arrestedbyIndx)],
        text[chargesIndx:text.find("\n",chargesIndx)])
    #duplicate checking
    if (nameDict.get(tempPerson.name) == None):
        nameDict.update({tempPerson.name : iNameDict})
        iNameDict += 1
        persons.append(tempPerson)
        dupCount = 0
    
    else:
        persons[ nameDict.get(tempPerson.name) ].update_info(tempPerson)
        dupCount += 1
    
    #click on next button    
    driver.find_element_by_id("button_next").click()

csvData = "Name,Sex,Age,Height,Weight,From,Arrest Date,Arrested By,Charges\n"
for person in persons:
    csvData += person.printVals()

#CSV FILE CREATION
f = open("mugshots" + ".csv", 'w')
f.write(csvData)
driver.quit()
f.close()
