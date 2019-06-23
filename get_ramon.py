#!env/bin/python
import sys
import logging
import requests
import json
import csv

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(message)s')

def getHttpCall(base_url,payload,headers):
    r = requests.get(base_url, params=payload,headers=headers)
    raw = r.json()
    return raw

def doCSV(fits):
    csv_columns = ['name','size']
    csv_file = "ilan_ramon.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in fits["items"]:
                writer.writerow(data)
    except:
        logging.error("Couldn't write csv file")
         

def metaLinks(collection):
    logging.info("querying each image data for metadata link")
    links = []
    metas = []
    for item in collection:
        somelink = item["href"]
        links.append(somelink)
    for link in links:
        try:
            logging.info("quering {} ".format(link))
            allPics = getHttpCall(link,'','')
        except:
            logging.warning("{} could no be reached, continue next".format(link))
            continue
        for meta in allPics:
            if 'json' in meta:
                metas.append(meta)
    return metas
    
def extractAndFilter(metas):
    fits = {"items":[]}
    for meta in metas:
        logging.info("Inspecting {} metada".format(meta))
        try:
            data = getHttpCall(meta,'','')
        except Exception:
            logging.warning("meta {} couldn't be reached".format(meta))
            continue
        if "File:FileSize" in data and "AVAIL:NASAID" in data:
            size = data["File:FileSize"]
            name = data["AVAIL:NASAID"]
            if float(size.split(' ')[0]) > 1000:
                fits["items"].append({"name":name,"size":size}) 
    logging.debug(fits)


def queryAPI(q,api_key,base_url):
    payload = {"q": q}
    headers = {"api_key" : api_key}
    logging.info("Querying NASA library for {}".format(q))
    try:
        raw = getHttpCall(base_url,payload,headers)
    except:
        logging.error("NASA endpoint could not be reached")
        #print ("NASA endpoint could not be reached")
        sys.exit(1) 
    collection = raw["collection"]["items"]
    links = []
    print(raw["collection"]["links"][0])
    while "prompt" in raw["collection"]["links"][0] and raw["collection"]["links"][0]["prompt"] == "Next":
        logging.info("got additional page")
        link = raw["collection"]["links"][0]
        #for link in raw["collection"]["links"][0]:
        params = link["href"].split('?')[1].split('&')
        for param in params:
            if "page" in param:
                page = param.split('=')[1]
                pagePay = {"page": page}
                payload.update(pagePay)
                logging.info("Next page is page {} payload is {}".format(page,payload))
                if int(page) != 1:
                    try:
                        raw = getHttpCall(base_url,payload,headers)
                        for item in raw["collection"]["items"]:
                            collection.append(item)
                    except:
                        logging.warning("next page could not be reached - using partial data")
                        break
                else:
                    break
                
    #print (collection[0])
    logging.info("Got all data based on {} query".format(q))
    logging.info("Collection has {} items".format(len(collection)) )
    logging.debug(collection)
    return collection


def main():
    api_key = "3Iz7NOzY9bFmlSMTF36KL1A0ts4Z6X8DD60aCXID"
    base_url = "https://images-api.nasa.gov/search"
    q = "Ilan Ramon"

    doCSV(extractAndFilter(metaLinks(queryAPI(q,api_key,base_url))))

    

    
    


if __name__=="__main__":
    main()