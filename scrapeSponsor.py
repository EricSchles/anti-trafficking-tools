import concurrent.futures
import requests
from multiprocessing import Pool
import random 
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from dateutil import parser
import time
import os
import sys
import subprocess
from timeit import default_timer as timer
from scrape_sponsor_parser import parse

start = timer()
        
#fill locs, get timestamp
ts = int(time.time())
ts_str = str(ts)

locs = ["la", "imperial", "washington", "upstateca", "sfbay", 
        "centralcoast", "sandiego", "oregon", "nevada", 
        "sanjoaquinvalley", "sacramento", "newyork", "southflorida", 
        "burlington", "newjersey", "maine", "northcarolina", "daytona", 
        "georgia", "newhampshire", "pennsylvania", "westvirginia", 
        "southwestflorida", "rhodeisland", "delaware", "michigan", 
        "ohio", "northwestflorida", "massachusetts", "northflorida", 
        "southcarolina", "maryland", "connecticut", "virginia", "dc", 
        "indiana", "upstateny", "southdakota", "illinois", "northeasttexas", 
        "northdakota", "southeasttexas", "nebraska", "wisconsin", 
        "iowa", "louisiana", "kansas", "tennessee", "arkansas", 
        "missouri", "kentucky", "southtexas", "alabama", "mississippi", 
        "minnesota", "centraltexas", "oklahoma", "arizona", "montana", 
        "newmexico", "westtexas", "colorado", "wyoming",  "idaho", "utah", "alaska", "hawaii"]

# turn this into a database instead of writing out to files and folder structure
urls = []
for loc in locs:
    #location subfolder in sponsor subfloder in scrape-ads
    directory = os.path.join(os.getcwd(), 'scrape-data/sponsor_ads/'+loc+'/')
    try:
        os.makedirs(directory)
    except OSError:
        pass
    subprocess.call(["sudo","chmod","777",directory])
    #the day/timestamp subfolder in location
    os.makedirs(directory+ts_str)
    #log file
    log = open(directory+ts_str+'/log.txt', 'w')
    print loc
    log.write('scraping loc : ')
    log.write(loc)
    log.write("...") 
    urls.append("http://"+loc+".backpage.com/FemaleEscorts/?layout=date")
    urls.append("http://"+loc+".backpage.com/BodyRubs/?layout=date")
    urls.append("http://"+loc+".backpage.com/Strippers/?layout=date")
    urls.append("http://"+loc+".backpage.com/Domination/?layout=date")
    urls.append("http://"+loc+".backpage.com/TranssexualEscorts/?layout=date")
    urls.append("http://"+loc+".backpage.com/MaleEscorts/?layout=date")
    urls.append("http://"+loc+".backpage.com/Datelines/?layout=date")
    urls.append("http://"+loc+".backpage.com/AdultJobs/?layout=date")
    
    #scrape the 8 pages   
    pool = Pool(8)
    results = pool.map(parse, urls)
    log.write('done!')
    log.write("\n")
    print('done')
    #all 8 files
    log.write('saving files...')
    service = ''
    for i in range(0,7):
        if (i==0) : service = 'escorts'
        elif (i==1) : service = 'bodyrubs'
        elif (i==2) : service = 'strippers'
        elif (i==3) : service = 'domination'
        elif (i==4) : service = 'transescorts'
        elif (i==5) : service = 'maleescorts'
        elif (i==6) : service = 'datelines'
        elif (i==7) : service = 'adultjobs'
        g = open(directory+ts_str+'/'+service+'.txt', 'w')
        g.write(results[i])
        g.close()
    log.write("\n")
    log.write('done!')
    log.write("\n")
    print('saved')
elapsed_time = timer() - start
log.write("time to run : ")
log.write(str(elapsed_time))
log.write(" seconds")
log.close()
