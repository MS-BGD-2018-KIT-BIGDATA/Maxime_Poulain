from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import math
from multiprocessing import Pool
import time
import requests
import numpy as np
import re



url = "http://www.journaldunet.com/management/ville/classement/villes/population"
def getSoupFromURL(url):
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        return None

soup = getSoupFromURL(url)
villes = [i.text.split(' (')[0] for i in soup.tbody.find_all('a',href=re.compile('^/management/ville/'))][:10]
print(villes)

def sendRequest(depart, arrive):

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    querystring = {"origins":depart,"destinations":arrive,"key":"AIzaSyAKBEATKH1S_-lX8EiNEjzp8QG1bznrXm8"}

    headers = {
        'cache-control': "no-cache",
        'postman-token': "ade0b2b2-2bfa-94a1-af59-a5eaa856bb87"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)
    if response.status_code == 200:
        return response.text
    else:
        print("REQUEST ERROR")


def getdistance(depart, arrive):
    response = sendRequest(depart, arrive)
    if response != None:
        js = json.loads(response)
        value = js['rows'][0]['elements'][0]['distance']['text'].split()[0]
        if ',' in value:
            return float(js['rows'][0]['elements'][0]['distance']['text'].split()[0].replace(',','.'))
        else:
            return float(js['rows'][0]['elements'][0]['distance']['text'].split()[0])

    else:
        print("ERROR")
        return None


distance = []

for i in villes:
    tmp = []
    for j in villes:
        print(i)
        print(j)
        dist = getdistance(i,j)
        print(dist)
        tmp.append(dist)
    distance.append(tmp)



result =  pd.DataFrame(np.matrix(distance), columns=villes, index=villes)
print(result)
