x : dict<int, int> = {}
y : dict<int, int> = {}
z : dict<int, int> = {}

x.set(1, 2)
y.set(3, 4)
z.set(5, 6)

listOfDict : [dict<int,int>] = [x,y,z]

q : dict<int,int> = listOfDict[0]
r : dict<int,int> = listOfDict[1]

three : int = q.get(1) + r.get(3)

loopDict : dict<str, int> = {}

loopDict.set("infinite", 1)

while(True) : {
    loopDict.set("infinite", loopDict.get("infinite") + 1)
    if (loopDict.get("infinite") == 10) : {
        break
    }
}

beeDictionary : dict<str, [str]> = {}

beeDictionary.set("bumble bee", ["BUM-BULL-BE", "An insect that is a bee that bumbles"])
beeDictionary.set("honey bee", ["HUN-E-BE", "An insect that is a bee that makes honey"])

def lookUpBee(beeDictionary : dict<str, [str]>, bee : str) -> [str]: {
    desiredBee : [str] = beeDictionary.get(bee)
    pronounciation : str = desiredBee[0]
    definition : str = desiredBee[1]

    return [pronounciation, definition]
}

hunnybee : [str] = lookUpBee(beeDictionary, "honey bee")
bumbybee : [str] = lookUpBee(beeDictionary, "bumble bee")
