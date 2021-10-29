import uuid
import urllib.request, json
import json
from tkinter.filedialog import askopenfilename
import gc
from objects import Attendants, BotAgents
# buscar atendentes de todos os bots
# buscar na planilha proximo atendente 
# verificar bot a bot se ele esta como atendente
# se estiver remover 
# ir para proximo

    
def checkInBot(identity,list_agents):
    for agent in list_agents:
        if agent.identity == identity:
            return True
    return False

def removeAttendant(identity,auth):
    identity = identity.replace("%40","%2540")
    identity = identity.replace("@","%40")
    body = {
        "id": str(uuid.uuid4()),
        "to": "postmaster@desk.msging.net",
        "method": "delete",
        "uri": f"/attendants/{identity}"
    } 
    req = urllib.request.Request(url="https://http.msging.net/commands",
                             data=bytes(json.dumps(body), encoding="utf-8"), method='POST')
    req.add_header("Authorization", auth)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as response:
        source_settings = response.read().decode('utf-8')
        response = json.loads(source_settings)
        if(response["status"] == "success"):
            return True
    return False

def generateIdentify(cpf):
    return f"10{cpf}%40mundiale.com.br@blip.ai"

def getAgentsBot(auth):
    gc.collect()
    list_agents = []
    body = {
        "id": str(uuid.uuid4()),
        "to": "postmaster@desk.msging.net",
        "method": "get",
        "uri": "/attendants/"
    }
    req = urllib.request.Request(url="https://http.msging.net/commands",
                             data=bytes(json.dumps(body), encoding="utf-8"), method='POST')
    req.add_header("Authorization", auth)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as response:
            source_settings = response.read().decode('utf-8')
            response_dic = json.loads(source_settings)
            for element in response_dic["resource"]["items"]:
                attendant = Attendants(element["identity"], element["fullname"],element["email"],element["teams"],
                    element["status"])
                list_agents.append(attendant)
    except:
        with urllib.request.urlopen(req) as response:
            source_settings = response.read().decode('utf-8')
            response_dic = json.loads(source_settings)
            for element in response_dic["resource"]["items"]:
                attendant = Attendants(element["identity"], element["fullname"],element["email"],element["teams"],
                    element["status"])
                list_agents.append(attendant)
    return list_agents


list_bots = []
filename = askopenfilename()
arq = open(filename,"r",encoding="utf-8")
print("Buscando lista de atendentes...\n")
linhas = arq.readlines()
a=1
list_bot_error = []
for linha in linhas:
    if linha != ";;\n":
        try:
            if(a!=1):
                auth = linha.split(';')[1]
                auth = auth.replace("\n","")
                name = linha.split(';')[0]
                agents = getAgentsBot(auth)
                list_bots.append(BotAgents(auth,agents))
        except:
            list_bot_error.append(linha)
        a=2

listmundiale = askopenfilename()
arq2 = open(listmundiale,"r",encoding="utf-8")
print("Buscando lista de atendentes...\n")
linhas = arq2.readlines()
list_removed = []
removeds = {}
for linha in linhas:
    qtd=0
    cpf = linha.split(';')[5]
    identify = generateIdentify(cpf)
    list_removed = []
    for bot in list_bots:
        hasAttendantInBot = checkInBot(identify,bot.attendants)
        if(hasAttendantInBot):
            print(removeAttendant(identify,bot.auth))
            qtd += 1
            list_removed.append(bot)
    removeds[cpf] = list_removed
    print(f"CPF:{cpf} Removidos:{qtd}")
    if qtd > 0:
        print(f"Removido de :{list_removed}")
final = open("deletados.txt",'w+')
for key in removeds:
    final.write(f"{key}:{removeds[key]}\n")