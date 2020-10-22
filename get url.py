import urllib.request, json
import uuid
from tkinter.filedialog import askopenfilename

def get_settings(auth):
    body_settings =  {
        "id": str(uuid.uuid4()),
        "method": "get",
        "uri": "/buckets/blip_portal:builder_working_configuration"
    }
    req = urllib.request.Request(url="https://http.msging.net/commands",data=bytes(json.dumps(body_settings), encoding="utf-8"),method='POST')
    req.add_header("Authorization" ,auth)
    req.add_header("Content-Type","application/json")
    with urllib.request.urlopen(req) as settings:
        source_settings = settings.read().decode('utf-8')
        json_settings = json.loads(source_settings)
    return json_settings

filename = askopenfilename()
arq = open(filename,"r",encoding="utf-8")

print("verificando...\n")

linhas = arq.readlines()
print("lido")
urls = [()]
a=1
for linha in linhas:
    if linha != ";;\n":
        try:
            if(a!=1):
        
                body =  {
                    "id": str(uuid.uuid4()),
                    "method": "get",
                    "uri": "/buckets/blip_portal:builder_working_flow"
                }
                auth = linha.split(';')[1]
                name = linha.split(';')[0]


                req = urllib.request.Request(url="https://http.msging.net/commands",data=bytes(json.dumps(body), encoding="utf-8"),method='POST')
                req.add_header("Authorization" ,auth)
                req.add_header("Content-Type","application/json")
                settings = get_settings(auth)
                with urllib.request.urlopen(req) as response:       
                    source = response.read().decode('utf-8')
                    json_obj = json.loads(source)
                    for element in json_obj["resource"]:
                        for action in json_obj["resource"][element]["$enteringCustomActions"]:
                            if action["type"] == "ProcessHttp":
                                if  action["settings"]["uri"].startswith("{{config"):
                                    try:
                                        url = action["settings"]["uri"].split("}}")[0]
                                        url = url.split(".")[1]
                                        base = settings["resource"][url] 
                                        final = action["settings"]["uri"].split("}}")[1]
                                        bot_url = (name,base+final)
                                        if(bot_url not in urls):
                                            urls.append(bot_url)   
                                    except:
                                        urls.append((name,action["settings"]["uri"])) 
                        for action in json_obj["resource"][element]["$leavingCustomActions"]:
                            if action["type"] == "ProcessHttp":
                                if action["settings"]["uri"] not in urls and action["settings"]["uri"].startswith("{{config"):
                                    try:
                                        url = action["settings"]["uri"].split("}}")[0]
                                        url = url.split(".")[1]
                                        base = settings["resource"][url] 
                                        final = action["settings"]["uri"].split("}}")[1]
                                        bot_url = (name,base+final)
                                        if(bot_url not in urls):
                                            urls.append(bot_url)  
                                    except:
                                        urls.append((name,action["settings"]["uri"])) 
        except:
            print("error")
        a=2
final = open("lista_urls.txt",'w+')
for url in urls:
    final.write(f"{url}\n")
