import uuid
import urllib.request
import json
from tkinter.filedialog import askopenfilename

# buscar atendentes de todos os bots
# buscar na planilha proximo atendente 
# verificar bot a bot se ele esta como atendente
# se estiver remover 
# ir para proximo

class Attendants:
    def __init__(self, identity, fullname,email,teams,status,agentSlots):
        self.identity = identity
        self.fullname = fullname
        self.email = email
        self.teams = teams
        self.status = status
        self.agentSlots = agentSlots

class BotAgents:
    def __init__ (self,auth,attendants):
        self.attendants = attendants
        self.auth = auth
    
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
    with urllib.request.urlopen(req) as response:
        source_settings = response.read().decode('utf-8')
        response = json.loads(source_settings)
        for element in response["resource"]["items"]:
            attendant = Attendants(element["identity"], element["fullname"],element["email"],element["teams"],
                element["status"],element["agentSlots"])
            list_agents.append(attendant)
    return list_agents


list_bots = []
filename = askopenfilename()
arq = open(filename,"r",encoding="utf-8")
print("Buscando lista de atendentes...\n")
linhas = arq.readlines()
a=1
for linha in linhas:
    if linha != ";;\n":
        try:
            if(a!=1):
                auth = linha.split(';')[1]
                name = linha.split(';')[0]
                agents = getAgentsBot(auth)
                list_bots.append(BotAgents(auth,agents))
        except:
            print("error")
        a=2


listmundiale = askopenfilename()
arq2 = open(listmundiale,"r",encoding="utf-8")
print("Buscando lista de atendentes...\n")
linhas = arq2.readlines()
for linha in linhas:
    cpf = linha.split(';')[5]
    identify = generateIdentify(cpf)
    for bot in list_bots:
        hasAttendantInBot = checkInBot(identify,bot.attendants)
        if(hasAttendantInBot):
            print(removeAttendant(identify,bot.auth))
