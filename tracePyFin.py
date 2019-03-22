import subprocess
import time
import concurrent.futures
import subprocess
from concurrent import futures

domainUrl = [
    "www.google.pl",
    "www.se.pl",
    "www.sekurak.pl",
    "www.fakt.pl",
    "www.ford.pl",
    "www.interia.pl",
    "www.bosch.pl",
    "www.kobi.pl",
    "www.kross.pl"]


def tracert(domainName, result):
    print("[*] {}".format(domainName))
    array = subprocess.check_output(("traceroute", "{}".format(domainName)))
    result.append(array.decode("utf-8"))


def trace():
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
    start = time.time()

    finallData = []

    traceRouteReturnData = trace()
    toRewriteData = list(map(lambda y: y.split("\n"), filter(lambda x: x != None, traceRouteReturnData)))

    for row in range(0, len(toRewriteData)):
        finallData.append(list(filter(lambda x: x.find("* * *") != 4, toRewriteData[row])))

    for row in range(0, len(finallData)):
        rowLen = len(finallData[row])
        print(finallData[row][0].split(" ")[2], finallData[row][rowLen - 3][3:])  # display data

    end = time.time()
    print(end - start)


__main__()