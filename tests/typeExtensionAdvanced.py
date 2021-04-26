x = {}
y = {}
z = {}
x[1] = 2
y[3] = 4
z[5] = 6
listOfDict = [x,y,z]
q = listOfDict[0]
r = listOfDict[1]
three = q[1] + r[3]
loopDict = {}
loopDict["infinite"] = 1
while True:
    loopDict["infinite"] = loopDict["infinite"] + 1
    if loopDict["infinite"] == 10 :
        break
beeDictionary = {}
beeDictionary["bumble bee"] = ["BUM-BULL-BE","An insect that is a bee that bumbles"]
beeDictionary["honey bee"] = ["HUN-E-BE","An insect that is a bee that makes honey"]
def lookUpBee(beeDictionary,bee):
    desiredBee = beeDictionary[bee]
    pronounciation = desiredBee[0]
    definition = desiredBee[1]
    return [pronounciation,definition]
hunnybee = lookUpBee(beeDictionary,"honey bee")
bumbybee = lookUpBee(beeDictionary,"bumble bee")
