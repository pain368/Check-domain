import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures
import sys
import json


def make_request(domainName):

    url = domainName.strip("\n")
    requestResult = requests.head(url)

    print("[*]{} -> response code: {}\n".format(url, requestResult.status_code))
    return url, requestResult.status_code


def getWhoIsResponse(data):

    # Regex
    pattern = r"https?://(www\.)?"
    urlFromFile = re.compile(str(pattern))
    rightUrl = urlFromFile.sub("", str(data))

    # Request
    ss = requests.get("https://who.is/whois/{}".format(rightUrl.strip("\n")))
    soup = BeautifulSoup(ss.text, "html.parser")
    xx = soup.pre.text
    resul = xx.split("\n")

    return resul

    # tag = soup.find_all("pre")


def start(function, data):
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8)as execute:
        future_url = {execute.submit(function, urlfromTable): urlfromTable for urlfromTable in data}

        for future in concurrent.futures.as_completed(future_url):
            url = future_url[future]
            try:
                result.append(future.result())
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
    return result


def __main__():

    fileInputLink = open(sys.argv[1], "r").readlines()

    data = start(make_request, fileInputLink)
    generalTab = []

    for i in range(len(data)):

        if data[i][1] == 200 or 301:
            generalTab.append(getWhoIsResponse(data[i][0]))

    pos = 0
    finalData = {}

    for i in range(len(generalTab)):

        for j in range(len(generalTab[i])):
            if generalTab[i][j].find("REGISTRAR:") == 0:

                pos = j
                value = generalTab[i][pos + 1].replace(" ", "")
                key = generalTab[i][0].replace(" ", "")

                finalData[key.strip("\r")] = value.strip("\r")

    for key, val in finalData.items():
        print(key, val)

    with open("whois.json", "w") as outfile:
        json.dump(finalData, outfile)

    outfile.close()


__main__()
