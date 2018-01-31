import requests
import random

def getPort():
    upper = 499
    lower = 2
    r = (int) (random.random() * (upper - lower)) + lower
    port = ""
    if (r < 10): port = "3000"+str(r)
    elif (r >= 10 and r <= 99): port = "300" + str(r)
    elif (r >= 100 and r <= 249): port = "30" + str(r)
    elif (r >= 250 and r <= 499): 
        r = r + 8
        port = "32" + str(r)
      
    proxies = {
               'http': 'http://127.0.0.1:'+port
               }
    return proxies

def parse(url):
    proxies = getPort()
    #check if port is open
    try:
        #page = requests.get(url, proxies=proxies)
        page = requests.get(url)
    except:
        proxies = getPort()
        #page = requests.get(url, proxies=proxies)
        page = requests.get(url)
    return page.content
