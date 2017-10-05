from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import math

def getSoupFromURL(url):
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        return None

def getUserName(url):
    soup = getSoupFromURL(url)
    count = 0
    users = []
    for i in soup.find_all('tbody')[0].find_all('a'):
        if i.string != None and 'http' not in i.string:
            users.append(i.string)
    return users

def getNumberOfRepos(user):
    users_github = "https://api.github.com/users/"
    headers = {
        'authorization': "Basic bWF4cG91bGFpbjo1NGMzOWMwMDU2OGU2ZTQzNTc1MjMwNTdjOGM3ODljNjA2MTZlZmFj",
        'cache-control': "no-cache",
        'postman-token': "ad5f7c1e-e392-95ed-ebaf-9ab902dce4ba"
        }
    response = requests.request("GET",users_github+user, headers=headers)
    if response.status_code == 200:
        return int(json.loads(response.text)['public_repos'])

def getStarsNumber(user):
    users_github = "https://api.github.com/users/"
    headers = {
        'authorization': "Basic bWF4cG91bGFpbjo1NGMzOWMwMDU2OGU2ZTQzNTc1MjMwNTdjOGM3ODljNjA2MTZlZmFj",
        'cache-control': "no-cache",
        'postman-token': "ad5f7c1e-e392-95ed-ebaf-9ab902dce4ba"
        }

    nbrepos = getNumberOfRepos(user)
    nbpage = math.ceil(nbrepos/100)
    total = 0
    for j in range(1,nbpage+1):
        response = requests.request("GET",users_github+user+"/repos?page="+str(j)+"&per_page=100", headers=headers)
        if response.status_code == 200:
            somme = 0
            for i in json.loads(response.text):
                somme += i['stargazers_count']
            total +=somme
        else:
            print("REQUEST ERROR WITH USER "+user)

    if nbrepos != 0:
        # print('Number of repos '+str(nbrepos))
        # print('Number of stars '+str(total))
        return float('%.2f' % (float(total)/float(nbrepos)))
    else:
        return 0



url = 'https://gist.github.com/paulmillr/2657075'
users = getUserName(url)
stars = []
for i in users:
    # print(i)
    stars.append(getStarsNumber(i))


result = pd.DataFrame({'users': users,'mean_stars': stars})
print(result.dtypes)
print("---------")
print(result.sort_values(["mean_stars"],ascending=False))
