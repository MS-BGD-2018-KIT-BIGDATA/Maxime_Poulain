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

def getMeanReduction(url):
    soup = getSoupFromURL(url)
    mean_reduction = 0
    reduction = soup.find_all("div",class_="ecoBlk")
    for i in reduction:
        try:
        #print(i.find('span').string.split('€')[0])
            mean_reduction += int(i.find('span').string.split('€')[0])
        except ValueError:
            pass
        #     print(i.find('span').string.split('%')[0])
        #     mean_reduction += int(i.find('span').string.split('%')[0])

    result = mean_reduction/len(reduction)
    return result

def getMeanPrice(url):
    soup = getSoupFromURL(url)
    mean_price = 0
    price = soup.find_all("span",class_="price")
    for i in price:
        mean_price += float(i.text.replace('€','.'))
    result = mean_price/len(price)
    return result

url='https://www.cdiscount.com/search/10/'#acer.html'
# print(getMeanPrice(url))
# print(getMeanReduction(url))
dico = {}
for i in ['acer','dell']:
    tmp = {}
    tmp['MeanPrice'] = getMeanPrice(url+i+'.html')
    tmp['MeanReduction'] = getMeanReduction(url+i+'.html')
    #print(tmp)
    dico[i] = tmp
print(dico)
