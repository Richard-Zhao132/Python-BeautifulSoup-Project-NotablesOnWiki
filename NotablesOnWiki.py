# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 17:04:50 2022

@author: Richard Zhao FLora Fung
Title: Data Science Homework 2 Wiki Search
Summary: Get data, YOB and YOD of person from wiki and seed twice
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import certifi
import csv



seedPages = ["Flora_Robson"]

allPeople = {}
allLinks = []
with urlopen("https://en.wikipedia.org/wiki/Flora_Robson", cafile=certifi.where()) as url:
    soup = BeautifulSoup (url , "lxml")
    #print(soup.prettify())
    
    name = soup.find("h1")      #Find the name
    name = name.string
    print(name)
    
    DOB = soup.find(class_="bday")      #Find the Year of Birth
    YOB = DOB.string[0:4]
    print(YOB)
    
    
    
    YODDescriptor = soup.find_all(text= "Died")   #Find the year of death
    YODParent = YODDescriptor[0].parent
    ParentParent = YODParent.parent     
    span = ParentParent.find("span", style="display:none")
    YOD = span.string[1:5]
    print(YOD)
    
    personInfo = (name, YOB, YOD)       #Put person data in tuple
    allPeople["Flora_Robson"] = personInfo      #Put tuple in dictionary
    print(allPeople["Flora_Robson"])            #Print test
    
    
    AllLinksInPg = []
    AllLinksInCurrPg = []
    currentTotalLink = ["Flora_Robson"]
    #links = soup.find_all("a")      
    
    all_PLinks = soup.select('p a')
    
    for link in all_PLinks:              #Create List of all links
        if link.has_attr("class"):  #If the link is not in english, ignore it
            continue
        else:
            ref = link.get("href")  #Gets the full link
            refStr = str(ref).partition("/wiki/")[2]    #Get part of link after "/wiki/"
            if not refStr:
                continue
            if refStr not in AllLinksInPg:
                AllLinksInPg.append(refStr)

print("All page links are " + str(len(AllLinksInPg)))


defaultLink = "https://en.wikipedia.org/wiki/"
n = 0

for link in AllLinksInPg:   #test this tmr
    if link in currentTotalLink:            #If we already have to link make note of it and move on to next item
        thisLink = ("Flora_Robson", link)
        allLinks.append(thisLink)
        print(link + " was already in list, moving on.")
        continue
                          
    with urlopen(defaultLink + link, cafile=certifi.where()) as url:
        soup = BeautifulSoup (url , "lxml")
        if soup.find("h1") == None:
            #print("no name was found in " + link + "moving on")
            continue
        elif soup.find("h1") != None:
            name = soup.find("h1")      #Find the name
            name = name.string
            #print("found name, " + name)
        
        if soup.find(class_="bday") == None:
            #print("no bdat was found in " + link + "moving on")
            continue
        else:
            DOB = soup.find(class_="bday")      #Find the Year of Birth
            YOB = DOB.string[0:4]
            #print("Found bday" + YOB)
        
        if not soup.find_all(text= "Died"):
            #print("no YOD was found in " + link + "moving on")
            continue
        else:
            YODDescriptor = soup.find_all(text= "Died")   #Find the year of death
            YODParent = YODDescriptor[0].parent
            #print("parent: " + YODParent.string)
            ParentParent = YODParent.parent     
            span = ParentParent.find("span", style="display:none")
            spanS = str(span)
            if len(spanS) == 0:
                continue
            if len(spanS) < 12:
                continue
            if span.string is None:
                continue
            YOD = span.string[1:5]
            #print("Found YOD " + YOD)
        


        personInfo = (name, YOB, YOD)       #Put person data in tuple
        allPeople[link] = personInfo      #Put tuple in dictionary
        thisLink = ("Flora_Robson",link)
        allLinks.append(thisLink)
        currentTotalLink.append(link)
        
        #links = soup.find_all("a") 
        all_PLinks = soup.select('p a')
        
        for linkRd2 in all_PLinks:              #Create List of all links
            if linkRd2.has_attr("class"):  #If the link is not in english, ignore it
                continue
            else:
                ref = linkRd2.get("href")  #Gets the full link
                refStr = str(ref).partition("/wiki/")[2]    #Get part of link after "/wiki/"
                if not refStr:
                    continue
                if refStr not in AllLinksInPg:
                    AllLinksInCurrPg.append(refStr)
        
        #print("total number of links in this page " + str(len(AllLinksInCurrPg)))
        #print("person is " + name)
        
        for linkInRd2 in AllLinksInCurrPg:
            if linkInRd2 in currentTotalLink:            #If we already have to link make note of it and move on to next item
                thisLink = (link, linkInRd2)
                allLinks.append(thisLink)
                #print(linkInRd2 + " was already in listRd2, moving on.")
                continue
            
            #try:                                    #Try to do everything to the current link
            with urlopen(defaultLink + linkInRd2, cafile=certifi.where()) as urlRd2:
                soupRd2 = BeautifulSoup (urlRd2 , "lxml")
                if soupRd2.find("h1") == None:
                    #print("no name was found in " + link + "moving on")
                    continue
                elif soupRd2.find("h1") != None:
                    name = soupRd2.find("h1")      #Find the name
                    name = name.string
                    #print("found name, " + name)
                
                if soupRd2.find(class_="bday") == None:
                    #print("no bdat was found in " + link + "moving on")
                    continue
                else:
                    DOB = soupRd2.find(class_="bday")      #Find the Year of Birth
                    YOB = DOB.string[0:4]
                    #print("Found bday" + YOB)
                
                if not soupRd2.find_all(text= "Died"):
                    #print("no YOD was found in " + link + "moving on")
                    continue
                else:
                    YODDescriptor = soupRd2.find_all(text= "Died")   #Find the year of death
                    YODParent = YODDescriptor[0].parent
                    ParentParent = YODParent.parent     
                    span = ParentParent.find("span", style="display:none")
                    spanS = str(span)
                    if len(spanS) == 0:
                        continue
                    if len(spanS) < 12:
                        continue
                    if span.string is None:
                        continue
                    try:
                        YOD = span.string[1:5]
                    except:
                        print("rd2 fail YOD " + linkInRd2)
                        continue
                
        

                personInfo = (name, YOB, YOD)       #Put person data in tuple
                allPeople[linkInRd2] = personInfo      #Put tuple in dictionary
                thisLink = (link, linkInRd2)
                allLinks.append(thisLink)
                currentTotalLink.append(linkInRd2)
        
                    
        #n+=1
        AllLinksInCurrPg.clear()
        #print("done with " + str(n) + " loop of rd2")
    
        
    #time.sleep(1)


print(len(allPeople))
print(len(allLinks))
print(len(currentTotalLink))
with open("notables.csv", "w", newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(["url", "name", "born", "died"])
    for i in allPeople:
        try:
            thewriter.writerow([i, allPeople[i][0], allPeople[i][1], allPeople[i][2]])
        except:
            continue


with open("links.csv", "w", newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(["from_url", "to_url"])
    for i in range(len(allLinks)):
        try:
            thewriter.writerow([allLinks[i][0], allLinks[i][1]])
        except:
            continue
        
        
    
    
    

    
    
        
    
    
 