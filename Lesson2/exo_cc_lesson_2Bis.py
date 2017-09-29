from bs4 import BeautifulSoup
import requests
import re

def getSoupFromURL(url):
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        return None

def getInfos(url):
    soup = getSoupFromURL(url)
    element = soup.find_all("div",class_="prdtBloc")
    dico = {}
    for i in element:
        tmp = {}
        name = i.find("div",class_="prdtBTit")
        rp = i.find("span",class_="price")
        np = i.find("div",class_="prdtPrSt")
        if np != None and len(np) > 0:
            tmp['normalprice'] = float(np.text.replace(",","."))
        else:
            tmp['normalprice'] = float(rp.text.replace("€","."))
        if len(rp) > 0:
            tmp['pricewithreduction'] = float(rp.text.replace("€","."))
        dico[name.string.replace("\"","")] = tmp
    return dico

def getMeanPercentageReduction(dico,marque):
    stats = {}
    red = 0
    count = 0
    for j in dico[marque]:
        red += (dico[i][j]['normalprice'] - dico[i][j]['pricewithreduction'])
        count+=1
    stats[i] = (red / count)
    return stats

url='https://www.cdiscount.com/search/10/'
dico = {}
print('Moyenne des réductions par marque: ')
for i in ['acer','dell']:
    dico[i] = getInfos(url+i+'.html')
    print(str(i)+' '+str(getMeanPercentageReduction(dico,i)[i])+' €')
