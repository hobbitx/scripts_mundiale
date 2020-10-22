import urllib.request, json
import uuid

arq = open("levantamento bots net.csv","r",encoding="utf-8")
print("verificando...\n")

linhas = arq.readlines()

a=1
for linha in linhas:
    if(a!=1):
        body =  {
            "id": uuid.uuid4(),
            "method": "get",
            "uri": "/buckets/blip_portal:builder_working_flow"
        }
        auth = linha.split(';')[1]
        name = linha.split(';')[0]
        req = urllib.request.Request(url="https://http.msging.net/commands",data=bytes(json.dumps(body), encoding="utf-8"),method='POST')
        req.add_header("Authorization" ,auth)
        req.add_header("Content-Type","application/json")

        with urllib.request.urlopen(req) as response:
            source = response.read().decode('utf-8')
            json_obj = json.loads(source)
            with open(name+'.json', 'w',encoding='utf-8') as json_file:
                json.dump(json_obj, json_file,ensure_ascii=False, indent=4)
    a=2