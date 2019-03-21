import subprocess

import concurrent.futures
import subprocess
from concurrent import futures

domainUrl = ["www.google.pl", "www.se.pl", "www.sekurak.pl", "www.fakt.pl", "www.ford.pl", "www.interia.pl", "www.bosch.pl",
       "www.kobi.pl", "www.kross.pl"]


traceRouteReturnData = []

def tracert(domainName):
    print("[*] {}".format(domainName))
    array = subprocess.check_output(("traceroute", "{}".format(domainName)))
    traceRouteReturnData.append(array.decode("utf-8"))

import time

start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as execute:
    future_url = {execute.submit(tracert, url): url for url in domainUrl}

    for future in concurrent.futures.as_completed(future_url):
        url=future_url[future]
        try:
            traceRouteReturnData.append(future.result())

        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))


toRewriteData = []

# Deleta all None element
for col in traceRouteReturnData:
    if col != None:
        toRewriteData.append(col.split("\n"))


finallData = []
for row in range(0, len(toRewriteData)):
    tempArray= []
    for col in range(0, len(toRewriteData[row])):
        if toRewriteData[row][col].find("* * *") != 4:
            tempArray.append(toRewriteData[row][col])

    finallData.append(tempArray)

for row in range(0, len(finallData)):
    rowLen= len(finallData[row])
    print(finallData[row][0].split(" ")[2], finallData[row][rowLen - 3][3:]) # display data

end = time.time()

print(end-start)


