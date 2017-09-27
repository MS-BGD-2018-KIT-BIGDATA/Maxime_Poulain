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

def getValues(url):
    soup = getSoupFromURL(url)
    dictionnaire = {}
    for i in soup.find_all('tr',class_='bleu'):
        element = i.find('td',class_='libellepetit G')
        if element != None and re.search(r'= [A-D]$',element.string):
            dictionnaire[element.text.split(' ')[-1]] = [(int(x.string.split('\xa0')[0].replace(' ',''))) for x in i.find_all('td','montantpetit G')[1:3]]
    return dictionnaire

final_dict = {}
for annee in range(2010,2016):
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(annee)
    final_dict[annee] = getValues(url)
    print('Année '+str(annee))
    print(final_dict[annee])
    print('---------')
