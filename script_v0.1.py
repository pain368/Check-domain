import time
import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures
import sys

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
    tag = str(soup.find_all("pre"))

    whoIsData = tag.split("\r\n")

    return whoIsData


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
        whoisdata = []
        if data[i][1] == 200 or 301:
            whoisdata.append(getWhoIsResponse(data[i][0]))
        generalTab.append(whoisdata)

    finalData = []

    for i in range(len(generalTab)):
        finalData.append([(generalTab[i][0][0].split(":")[2].strip(" ")), generalTab[i][0][2:4]])

    for i in range(len(finalData)):
        print("".join(str(finalData[i])))


__main__()
