import concurrent.futures
import subprocess
import sys
from urllib.parse import urlparse
import json


def tracert(domainName, result):
    print("[*] {}".format(domainName))
    opt = urlparse(domainName.strip("\n"))
    array = subprocess.check_output(("traceroute", "{}".format(opt.netloc)))
    result.append(array.decode("utf-8"))


def trace(domainUrl):
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8)as execute:
        future_url = {execute.submit(tracert, url, result): url for url in domainUrl}

        for future in concurrent.futures.as_completed(future_url):
            url = future_url[future]
            try:
                result.append(future.result())
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
    return result


def __main__():

    finallData = []
    jsonarray = {}

    fileInputLink = open(sys.argv[1], "r").readlines()
    traceRouteReturnData = trace(fileInputLink)
    toRewriteData = list(map(lambda y: y.split("\n"), filter(lambda x: x != None, traceRouteReturnData)))

    for row in range(0, len(toRewriteData)):
        finallData.append(list(filter(lambda x: x.find("* * *") != 4, toRewriteData[row])))

    for row in range(0, len(finallData)):
        rowLen = len(finallData[row])
        print(finallData[row][0].split(" ")[2], "".join(str(finallData[row][rowLen - 3][3:])))
        jsonarray[finallData[row][0].split(" ")[2]] = "".join(str(finallData[row][rowLen - 3][3:]))

    # write data to file .json
    with open("data.json", "w") as writeJson:

        json.dump(jsonarray, writeJson)

    writeJson.close()


__main__()
