def init():
    global symTab
    symTab = [[]]

def printST():
    for l in symTab:
        print(l)
        
def newObj(entry):
    name = entry[0]
    value = entry[1]
    i = 0
    while i < len(symTab):     
        for e in symTab[i]:
            if e == name:
                return
        i = i + 1
    symTab[0].append([entry])

def find(name):
    i = -1
    n = ''
    while i < len(symTab):     
        for e in symTab[i]:
            if e == name:
                return
        i = i + 1
        
def update(ud):
    name = ud[0]
    val = ud[1]
    symTab[i] = (name,val)
