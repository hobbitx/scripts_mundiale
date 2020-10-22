import uuid
import urllib.request
import json


def getSource(idBlip):
    source_index = idBlip.split("@")[1]
    if source_index == "0mn.io":
        return "0mn.io"
    else:
        return "Whatsapp"


def getRequest(skip):
    auth = "Key Y2xhcm9jb21lcmNpYWxyb3V0ZXI6OWpUWWEzVGs5b0ZPZXRTMkp5THQ="
    body_settings = {
        "id": str(uuid.uuid4()),
        "method": "get",
        "uri": f"/contacts?$skip={skip}&$take=20&$filter=(source%20eq%20null)"
    }
    req = urllib.request.Request(url="https://http.msging.net/commands",
                             data=bytes(json.dumps(body_settings), encoding="utf-8"), method='POST')
    req.add_header("Authorization", auth)
    req.add_header("Content-Type", "application/json")
    return req

erros = []
auth = "Key Y2xhcm9jb21lcmNpYWxyb3V0ZXI6OWpUWWEzVGs5b0ZPZXRTMkp5THQ="
skip = 0
req = getRequest(skip)
with urllib.request.urlopen(req) as settings:
    source_settings = settings.read().decode('utf-8')
    json_obj = json.loads(source_settings)
    total = json_obj["resource"]["total"]
    while skip <= total:
        for element in json_obj["resource"]["items"]:
            identity = element["identity"]
            source = getSource(identity)
            body = {
                "id": str(uuid.uuid4()),
                "method": "merge",
                "uri": "/contacts",
                "type": "application/vnd.lime.contact+json",
                "resource": {
                    "identity": identity,
                    "source": source
                }
               
            }
            req = urllib.request.Request(url="https://http.msging.net/commands",
                                data=bytes(json.dumps(body), encoding="utf-8"), method='POST')
            req.add_header("Authorization", auth)
            req.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req) as response:
                if response.status != 200:
                    erros.append(identity)
        skip += 20
        req = getRequest(skip)
        with urllib.request.urlopen(req) as settings:
            source_settings = settings.read().decode('utf-8')
            json_obj = json.loads(source_settings)

final = open("erros.txt",'w+')
for err in erros:
    final.write(f"{err}\n")