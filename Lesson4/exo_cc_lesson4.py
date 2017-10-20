from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
from multiprocessing import Pool
import time
import itertools
import json



def getJSON(url):
    res = requests.get(url)
    return json.loads(res.text)

def getMedic(id):
    url = "https://www.open-medicaments.fr/api/v1/medicaments/"+id
    res = requests.get(url)
    return json.loads(res.text)

def getElements(id):
    elems = []
    jso = getMedic(id)
    elems.append(jso['titulaires'][0])
    elems.append(jso['substancesActives'][0]['dosageSubstance'])
    nb = re.search(r"\d{1,}",jso['presentations'][0]['libelle'])
    if nb :
        elems.append(int(nb.group(0)))
    else:
        elems.append(None)
    elems.append(jso['presentations'][0]['dateDeclarationCommercialisation'].split('-')[0])
    elems.append(jso['presentations'][0]['dateDeclarationCommercialisation'].split('-')[1])
    elems.append(jso['presentations'][0]['prix'])
    age = re.search(r"\d{2} ans",jso['indicationsTherapeutiques'])
    if age :
        elems.append(age.group(0).split()[0])
    else:
        elems.append(None)
    print(elems)
    return elems


js = getJSON("https://www.open-medicaments.fr/api/v1/medicaments?limit=100&query=ibuprof%C3%A8ne")

res = []
for i in js:
    print(i["codeCIS"])
    res.append(getElements(i["codeCIS"]))

df = pd.DataFrame(res,columns=['laboratoire','Dosage','nb comprime','Année','Mois','Prix','Age restriction'])
print(df)

# init_time = time.time()
# with Pool() as p:
#     p.map(getElements,[i["codeCIS"] for i in js])
# end_time = time.time()
# print("\nDone in {} s".format(end_time - init_time))






#
