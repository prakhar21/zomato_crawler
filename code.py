# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 01:00:49 2015

@author: prakhar
"""

from bs4 import BeautifulSoup
from urllib2 import urlopen
import sqlite3

## Connect to the database zomato.db
## Create a cursor to mark the current position for writing the data
createDB = sqlite3.connect('/home/prakhar/Desktop/scraping/zomato.db')
qc = createDB.cursor()

## Drop the table incase, it already exists
try:
    qc.execute("drop table jaipur_zomato")
except Exception as e:
    print e


## Create table with name jaipur_zomato by invoking this sql query
qc.execute("create table if not exists jaipur_zomato(id integer primary key autoincrement, name varchar(200), rating float, cusine varchar(200), costfor2 varchar(200),address varchar(200))")

count = 0
i = 0
j = 0

#Difining Locations
mainURL = "https://www.zomato.com/jaipur/restaurants/"
mainURL1 = "https://www.zomato.com/jaipur/"
popularPlacesInJaipur = []

#Fetching Popular Locations in Jaipur
html_open = urlopen(mainURL)
html_text = html_open.read()
html_close = html_open.close()
        
soup = BeautifulSoup(html_text)

## Fetching the names of popular locations in jaipur
## and store it in array by appending the new ones
for loc in soup.find_all('div',{"id":"filter-locations-html"}):
    h = loc.find('ul',{"id":"filter-locations-html-list"}).find_all('a')
    length_popularLocation = len(h)
    
    while i < length_popularLocation:
        popularPlacesInJaipur.append(h[i].contents[0])
        i+=1

i = 0

#-------------------------------------------------------
#-------------------------------------------------------
#-------------------------------------------------------

'''
---------------- Generating URL
'''


## Generating URL for the popular locations by concatinating the names to the mainURL1 after 
## cleaning it up
locations = []
while i < len(popularPlacesInJaipur):
    locations.append(mainURL1+popularPlacesInJaipur[i].lower().strip().replace(" ","-")+'-restaurants'+'?page=')
    #print locations[i]
    i+=1
    


targetPlace = ""            
            
indexes = [1,2,3,4,5]



while j < len(locations):
    
    print locations[j]
    targetPlace = locations[j]

    for i in indexes[:]:
        #url = urlopen("https://www.zomato.com/jaipur/raja-park-restaurants?page="+str(i))
        '''
        -----------------------------------------
        Links update as per index
        -----------------------------------------
        '''
        print "OPENING CONNECTION TO PAGE  " + str(i)
        #url = "https://www.zomato.com/jaipur/raja-park-restaurants?page="+str(i)
        url = targetPlace + str(i)
        print url
        print "\n------NAME------RATING-----CUSINE-------COSTFOR2--------ADDRESS----------\n"
        ''' 
        ----------------------------------------------------------
        Setting up the pipeline by opening and closing connections    
        ----------------------------------------------------------
        '''
        html_open = urlopen(url)
        html_text = html_open.read()
        html_close = html_open.close()
        
        soup = BeautifulSoup(html_text)
        
        #Starting to scrap
        for rest in soup.find_all('article','search-result'):
            Name = rest.find('a','result-title').contents[0].replace("'","")
            # print Name + "| "
            Rating = rest.find('div','search_result_rating col-s-4 clearfix').next.next.contents[0].strip()
            if Rating == '-' or len(Rating) > 3:
                Rating = 0
            # print Rating + "| "
            Address = rest.find('div','search-result-address zdark').contents[0].replace("'","")
            try:
                CostFor2 = rest.find('div','res-cost').next.next.next.strip()
            except Exception as e:
                CostFor2 = "NA"
            # print Address + "."
            Cusine = rest.find('div','res-snippet-small-cuisine truncate search-page-text').contents[1].replace("'","")
            count += 1
            
            try:
                #qc.execute("INSERT INTO jaipur_zomato(name,rating,cusine,costfor2,address) values ('%s','%f','%s','%s','%s')" % (Name,Rating,Cusine,CostFor2,Address))
                qc.execute("INSERT INTO jaipur_zomato(name,rating,cusine,costfor2,address) values (?,?,?,?,?)", (Name,Rating,Cusine,CostFor2,Address))
            except Exception as e:
                print Name, Rating, Cusine, CostFor2, Address
            #qc.execute("INSERT INTO jaipur_zomato(name,rating,cusine,costfortwo,address) values (\"prakhar\",3.3,\"mishra\",\"3232\",\"dsds\")")
            #print Name+"|"+Rating+"|"+Cusine+"|"+CostFor2+"|"+Address
            
        
        print "---------------------------------------------------\n------------------------------------------"
    
    print "Total Results : " + str(count)
    
    j += 1
    print j
    
    print "\n\n----------Starting to fetch for another Locations--------\n" 
            #print Name
            #count += 1
            #print count
            
createDB.commit()
createDB.close()
        
    
    
