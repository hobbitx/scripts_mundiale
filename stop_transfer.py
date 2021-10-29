import uuid
import urllib.request
import json
from tkinter.filedialog import askopenfilename


base_url = "https://http.msging.net/commands"
def getRequest(auth,resource):
    
    body_settings = {
        "id": str(uuid.uuid4()),
        "method": "set",
        "uri": "/resources/congested",
        "type": "text/plain",
        "resource": resource
    }
    req = urllib.request.Request(url=base_url,
                             data=bytes(json.dumps(body_settings), encoding="utf-8"), method='POST')
    req.add_header("Authorization", auth)
    req.add_header("Content-Type", "application/json")
    return req


resource = false

filename = askopenfilename()
arq = open(filename,"r",encoding="utf-8")

erros = []
print("verificando...\n")
linhas = arq.readlines()
a=1
for linha in linhas:
    if linha != ";;\n":
        try:
            if(a!=1):
                auth = linha.split(';')[1]
                name = linha.split(';')[0]
                req = getRequest(auth,resource)
                with urllib.request.urlopen(req) as response:
                    if response.status != 200:
                        erros.append((auth,name))
            else:
                a=2
        except:
            erros.append((auth,name))

             
final = open("erros.txt",'w+')
for err in erros:
    final.write(f"{err}\n")