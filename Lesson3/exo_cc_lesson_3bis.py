import googlemaps
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np
import re

gmaps = googlemaps.Client(key='GOOGLE_API_KEY')

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

matrix = gmaps.distance_matrix(villes, villes)
distances = []
for i in matrix['rows']:
    tmp = []
    for j in i['elements']:
        tmp.append(float(j['distance']['text'].split()[0].replace(',','.')))
    distances.append(tmp)

result =  pd.DataFrame(np.matrix(distances), columns=villes, index=villes)
print(result)
