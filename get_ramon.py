#!env/bin/python

import requests
import urllib.parse as urlparser
import json

api_key="3Iz7NOzY9bFmlSMTF36KL1A0ts4Z6X8DD60aCXID"
base_url = "https://images-api.nasa.gov/search"

def getHttpCall(base_url,payload,headers):
    r = requests.get(base_url, params=payload,headers=headers)
    raw = r.json()
    return raw

def metaLinks(collection):
    links = []
    for item in collection:
        metalink = item["href"]
        links.append(metalink)
    print (links)


def queryAPI(q,api_key,base_url):
    payload = {"q": q}
    headers = {"api_key" : api_key}
    raw = getHttpCall(base_url,payload,headers)
    collection = raw["collection"]["items"]
    links = []
    while "prompt" in raw["collection"]["links"]:
        for link in raw["collection"]["links"]:
            page = link["href"].split('?')[1].split('&')[0].split('=')[1]
            pagePay = {"page": page}
            payload.update(pagePay)
            raw = getHttpCall(base_url,payload,headers)
            collection.append(raw["collection"]["items"]) 

    return collection

def main():
    api_key = "3Iz7NOzY9bFmlSMTF36KL1A0ts4Z6X8DD60aCXID"
    base_url = "https://images-api.nasa.gov/search"
    q = "Ilan Ramon"

    metaLinks(queryAPI(q,api_key,base_url))
    
if __name__=="__main__":
    main()