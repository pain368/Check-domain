
import requests
import sys
from bs4 import BeautifulSoup
import re
import json
import subprocess

fileInputLink = []
jsonArray = []
respStatus = ["OK", "ERROR"]

if __name__ == "__main__":

    try:

        fileInputLink = open(sys.argv[1], "r").readlines()

        for linkCounter in range(0, len(fileInputLink)):

            #Request Header
            req = requests.head(fileInputLink[linkCounter].strip("\n"))

            if req.status_code == 200:

                # Parse URL through RegEx
                rec = re.compile(r"https?://(www\.)?")
                o = rec.sub('', fileInputLink[linkCounter])

                # Make request to who.is - Get /https://who.is/whois/onet.pl
                reqWhoIs = requests.get("https://who.is/whois/{}".format(o.strip("\n")))

                # Parse document HTML from reqWhoIs
                soup = BeautifulSoup(reqWhoIs.text, "html.parser")
                tag = str(soup.find_all("pre"))
                whoIsData = tag.split("\r\n")

                # Display info
                print("[OK] {}".format(fileInputLink[linkCounter]), end="")

                stringPosition = 0

                for countLine in range(0, len(whoIsData)):
                    stringPosition = stringPosition + 1

                    # If find REGISTRAR in string
                    if (whoIsData[countLine].find("REGISTRAR")) == 0:
                        print(whoIsData[stringPosition])
                        jsonArray.append(json.dumps({fileInputLink[linkCounter].strip("\n"):
                                                         [respStatus[0], whoIsData[stringPosition]]}))

                    elif whoIsData[countLine].find("Registrar") == 0:
                        print(whoIsData[stringPosition])
                        jsonArray.append(json.dumps({fileInputLink[linkCounter].strip("\n"):
                                                         [respStatus[0], whoIsData[stringPosition]]}))

            elif req.status_code >= 400:
                print("[Error] {}".format(fileInputLink[linkCounter]))

            else:
                print("[CHECK MANUALLY] {}".format(fileInputLink[linkCounter]))


    except BaseException as error:
        print("[!]{}".format(error))










