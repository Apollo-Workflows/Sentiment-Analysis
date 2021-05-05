#####################################################################
## This script uses the deploy.sh to create the typeMappings.json, ##
## which can directly be used by the apollo platform.              ##             
#####################################################################

import json
import os

stream = os.popen('./deploy.sh --url')
urls = stream.read()

urls = urls.split("\n")
urls = urls[:-1]


data = []

for url in urls:
    url = url.replace("\u001b[0m\u001b[0m", "")
    splitted = url.split(' = ')
    functionType = splitted[0][4:]
    url = splitted[1][1:-1]

    entry = {}

    entry["functionType"] = functionType
    entry["resources"] = [{"type": "Serverless", "properties": {"Uri": url}}]

    data.append(entry)



with open('typeMappings.json','w') as outfile:
    json.dump(data, outfile, indent=4)