from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
from multiprocessing import Pool
import time
import itertools


def getSoupFromURL(url):
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        print("Request Error")
        return None

def getLinkFromPage(url):
    soup = getSoupFromURL(url)
    links = []
    for i in soup.body.find_all("a",href=re.compile('\S*/[0-9]+\.')):
        if i['href']:
            links.append('https:'+i['href'])
    return links

def contructUrls():
    url_debut = "https://www.leboncoin.fr/voitures/offres/"
    url_fin = "&q=renault%20zo%E9&brd=Renault&mdl=Zoe"
    region = ['ile_de_france','provence_alpes_cote_d_azur','aquitaine']
    url_regions = list(map(lambda x:url_debut+x+"/?o=",region))
    url = []
    for i in url_regions:
        if 'ile_de_france' in i:
            url.extend(list(map(lambda x:i+str(x)+url_fin,range(1,5))))
        else:
            url.extend(list(map(lambda x:i+str(x)+url_fin,range(1,3))))
    return url


def getAllInformations(link):
    soup = getSoupFromURL(link)
    infos = [re.sub(r'\W','',i.text) for i in soup.find_all("span",class_="value")]
    numero = [ str(re.search(r'0[0-9]([ .-]?[0-9]{2}){4}',i.text).group(0).replace(' ','').replace('.','')) for i in soup.body.find_all("p",itemprop="description")]
    if len(numero) > 0:
        infos.extend(numero)
    else:
        infos.extend(["None"])
    if len(soup.find_all("span",class_="ispro")) > 0:
        infos.extend(str(1))
    else:
        infos.extend(str(0))
    version = [re.search(r'zen|intens|life',i.text.lower()) for i in soup.body.find_all("p",itemprop="description")]
    if len(version) > 0 and version[0] != None:
        infos.extend([str(version[0].group(0))])
    else:
        infos.extend(["None"])
    return infos

def getUrlsArgus():
    annee = ['2013','2014','2015','2016','2017']
    types = ['zen','intens','life']
    combi = list(itertools.product(annee,types))
    return combi

def getArgusPrice(arg):
    annee,typ = arg
    dico = {}
    url = 'http://www.lacentrale.fr/cote-auto-renault-zoe-'+typ+'+charge+rapide+type+2-'+annee+'.html'
    return [annee,typ,getSoupFromURL(url).find("span",class_="jsRefinedQuot").text.replace(' ','')]



init_time = time.time()
with Pool() as p:
    urls = contructUrls()
    links = []
    [links.extend(i) for i in p.map(getLinkFromPage,urls)]
    result = list(p.map(getAllInformations,links))
    arg = list(p.map(getArgusPrice,getUrlsArgus()))


df = pd.DataFrame(result,columns=['prix','ville','marque','model','annee','km','carburant','boite','ref','telephone','pro','version'], )
df.drop(['ville','model','marque','carburant','boite','ref'],axis=1, inplace=True)
# print(df['année'].value_counts())

argus = pd.DataFrame(arg,columns=['annee','version','argus'])
# print(argus)

data = pd.merge(df, argus, how='inner', on=['annee','version'])
data['km'] = data['km'].map(lambda x:x.lower().split('km')[0]).astype(int)
data['prix'] = data['prix'].astype(int)
data['argus'] = data['argus'].astype(int)
data['indice'] = data['argus'] - data['prix']
print(data)
#print(data[data['indice']> 0].count())

end_time = time.time()
print("\nDone in {} s".format(end_time - init_time))
