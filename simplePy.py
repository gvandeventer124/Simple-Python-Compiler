import pyFunc
from pyFunc import IMPORT, HASH, INT, IDENT, LT, GT,PERIOD, MAIN, \
     LPAREN,RPAREN,LCURL,RCURL, IF, SWITCH, WHILE, DO, FOR, INT, EQ, RETURN, FLOAT, \
     TRUE, FALSE, STAR,PERCENT,NEQ, EQUAL, LT,LTE,SHIFTL,GT,GTE,SHIFTR, DBLBAR, DBLAMP, PLUS, MINUS,\
     SEMICOLON, FLOAT, DOUBLE, BOOL,SLASH,NUM,CHAR,AND,OR,ELSE,CASE,BREAK,DEFAULT,COLON, \
     DEF, INDENT, IN, RANGE, COMMA,ELIF
import symtab
def simplePy(src):
    global indent, loop, bools, scopestack, commset, cond
    commset = 1
    cond = 1
    loop = 1
    scopestack = []
    bools = 1
    indent = 0
    pyFunc.init(src)
    while pyFunc.s == INDENT:
        pyFunc.getSym()
    symtab.init()
    program()
def program():
    i = pyFunc.index
    importstmt()
    function()
    while i != pyFunc.index:
        i = pyFunc.index
        stmt(0)
def importstmt():
    if pyFunc.s == IMPORT:
        pyFunc.getSym()
        if pyFunc.s == IDENT:
            print("fetch: " + pyFunc.val)
            pyFunc.getSym()
def function():
    global indent, scopestack
    if pyFunc.s == DEF:
        pyFunc.getSym()
        if pyFunc.s == MAIN:
            pyFunc.getSym()
            if pyFunc.s == COLON:
                pyFunc.getSym()
                scopestack = scopestack + ['main']
                indent = indent + 1
def stmt(lvl):
    global indent, scopestack,boolean
    while pyFunc.s == INDENT:
        lvl = lvl + 1
        pyFunc.getSym()
    if lvl == indent:
        i = pyFunc.index
        compStmt()
        if i == pyFunc.index:
            simpleStmt()
        if i == pyFunc.index:
            returnStmt()
    elif lvl < indent:
        print('end ' + scopestack[len(scopestack)-1])
        indent = indent - 1
        scopestack.pop()
        stmt(lvl)
def compStmt():
    global loop, indent, scopestack, cond, bools
    if pyFunc.s == FOR:
        loopid = loop
        code = 'iter ' + str(loopid) + ':'
        print(code)
        loop = loop + 1
        pyFunc.getSym()
        if pyFunc.s == IDENT:
            var = pyFunc.val
            pyFunc.getSym()
            if pyFunc.s == IN:
                pyFunc.getSym()
                if pyFunc.s == RANGE:
                    pyFunc.getSym()
                    if pyFunc.s == LPAREN:
                        pyFunc.getSym()
                        if pyFunc.s == NUM or pyFunc.s == IDENT:
                            print("start: ")
                            print('set ' + var + ' ' + str(pyFunc.val))
                            pyFunc.getSym()
                            if pyFunc.s == COMMA:
                                pyFunc.getSym()
                                if pyFunc.s == NUM or pyFunc.s == IDENT:
                                    print('while: ')
                                    print('LT ' + var + ' ' +str(pyFunc.val))
                                    pyFunc.getSym()
                                    if pyFunc.s == COMMA:
                                        pyFunc.getSym()
                                        if pyFunc.s == NUM or pyFunc.s == IDENT:
                                            print('update:')
                                            print('sum '+ var + ' ' +  var + ' ' + str(pyFunc.val))
                                            pyFunc.getSym()
                                        else:
                                            raise Exception
                                else:
                                    raise Exception
                            if pyFunc.s == RPAREN:
                                pyFunc.getSym()
                                if pyFunc.s == COLON:
                                    pyFunc.getSym()
                                    indent = indent + 1
                                    scopestack = scopestack + ['iter'+str(loopid)]
                                        
    elif pyFunc.s == WHILE:
        loopid = loop
        loop = loop + 1
        condid = cond
        cond = cond + 1
        pyFunc.getSym()
        print('iter' + str(loopid) + ':')
        if pyFunc.s == LPAREN:
           pyFunc.getSym()
           i = pyFunc.index
           print('while:')
           booleanStmt(bools)
           if i != pyFunc.index:
               if pyFunc.s == RPAREN:
                   pyFunc.getSym()
                   if pyFunc.s == COLON:
                       pyFunc.getSym()
                       indent = indent + 1
                       scopestack = scopestack + ['iter'+str(loopid)]
    elif pyFunc.s == IF:#
       pyFunc.getSym()
       condid = cond
       cond = cond + 1
       print('cond'+str(condid)+':')
       booleanStmt(bools)
       bools = bools + 1
       if pyFunc.s == COLON:
           pyFunc.getSym()
           indent = indent + 1
           scopestack = scopestack + ['cond'+str(condid)]
    elif pyFunc.s == ELIF:
       pyFunc.getSym()
       condid = cond
       cond = cond + 1
       print('cond'+str(condid)+':')
       booleanStmt(bools)
       bools = bools + 1
       if pyFunc.s == COLON:
           pyFunc.getSym()
           indent = indent + 1
           scopestack = scopestack + ['cond'+str(condid)]
    elif pyFunc.s == ELSE:
       pyFunc.getSym()
       condid = cond
       cond = cond + 1
       print('cond'+str(condid)+':')
       booleanStmt(bools)
       bools = bools + 1
       if pyFunc.s == COLON:
           pyFunc.getSym()
           indent = indent + 1
           scopestack = scopestack + ['cond'+str(condid)]
def booleanStmt(bid):
    global bools
    print('b' + str(bid) + ':')
    boolTerm(bid)
    if pyFunc.s == OR:
        print('end b' + str(bid))
        pyFunc.getSym()
        bools = bools + 1
        booleanStmt(bid+1)
    else:
        print('end b'+str(bid))
def boolTerm(bid):
    boolFact(bid)
    if pyFunc.s == AND:
        pyFunc.getSym()
        boolTerm(bid)
def boolFact(bid):
    global bools
    comparison(bid)
    if pyFunc.s == MINUS:
        pyFunc.getSym()
        boolFact(bid)
    elif pyFunc.s == LPAREN:
        pyFunc.getSym()
        bools = bools + 1
        booleanStmt(bid+1)
        if pyFunc.s == RPAREN:
            pyFunc.getSym()
def comparison(bid):
    if pyFunc.s == IDENT:
        v1 = pyFunc.val
        pyFunc.getSym()
        if pyFunc.s == EQUAL:
            pyFunc.getSym()
            if pyFunc.s == IDENT:
                print('EQ: ' + str(v1) + ' '+ str(pyFunc.val))
                pyFunc.getSym()
            elif pyFunc.s == NUM:
                print('EQ: ' + str(v1) + ' '+  str(pyFunc.val))
                pyFunc.getSym()
        elif pyFunc.s == GT:
            pyFunc.getSym()
            if pyFunc.s == IDENT:
                print('GT: ' + str(v1) + ' '+ str(pyFunc.val))
                pyFunc.getSym()
            elif pyFunc.s == NUM:
                print('GT: ' + str(v1) + ' '+  str(pyFunc.val))
                pyFunc.getSym()
        elif pyFunc.s == LT:
            pyFunc.getSym()
            if pyFunc.s == IDENT:
                print('LT: ' + str(v1) + ' '+  str(pyFunc.val))
                pyFunc.getSym()
            elif pyFunc.s == NUM:
                print('LT: ' + str(v1) + ' '+  str(pyFunc.val))
                pyFunc.getSym()
        elif pyFunc.s == GTE:
            pyFunc.getSym()
            if pyFunc.s == IDENT:
                print('GTE: ' + str(v1) + ' '+  str(pyFunc.val))
                pyFunc.getSym()
            elif pyFunc.s == NUM:
                print('GTE: ' + str(v1) + ' '+  str(pyFunc.val))
                pyFunc.getSym()
        elif pyFunc.s == LTE:
            pyFunc.getSym()
            if pyFunc.s == IDENT:
                print('LTE: ' + str(v1) + ' '+  str(pyFunc.val))
                pyFunc.getSym()
            elif pyFunc.s == NUM:
                print('LTE: ' + str(v1) + ' '+  str(pyFunc.val))
                pyFunc.getSym()
    if pyFunc.s == NUM:
            v1 = pyFunc.val
            pyFunc.getSym()
            if pyFunc.s == EQ:
                pyFunc.getSym()
                if pyFunc.s == EQ:
                    pyFunc.getSym()
                    if pyFunc.s == IDENT:
                        print('EQ: ' + str(v1) + ' '+ str(pyFunc.val))
                        pyFunc.getSym()
                    elif pyFunc.s == NUM:
                        print('EQ: ' + str(v1) + ' '+  str(pyFunc.val))
                        pyFunc.getSym()
            elif pyFunc.s == GT:
                pyFunc.getSym()
                if pyFunc.s == IDENT:
                    print('GT: ' + str(v1) + ' '+ str(pyFunc.val))
                    pyFunc.getSym()
                elif pyFunc.s == NUM:
                    print('GT: ' + str(v1) + ' '+  str(pyFunc.val))
                    pyFunc.getSym()
            elif pyFunc.s == LT:
                pyFunc.getSym()
                if pyFunc.s == IDENT:
                    print('LT: ' + str(v1) + ' '+  str(pyFunc.val))
                    pyFunc.getSym()
                elif pyFunc.s == NUM:
                    print('LT: ' + str(v1) + ' '+  str(pyFunc.val))
                    pyFunc.getSym()
            elif pyFunc.s == GTE:
                pyFunc.getSym()
                if pyFunc.s == IDENT:
                    print('GTE: ' + str(v1) + ' '+  str(pyFunc.val))
                    pyFunc.getSym()
                elif pyFunc.s == NUM:
                    print('GTE: ' + str(v1) + ' '+  str(pyFunc.val))
                    pyFunc.getSym()
            elif pyFunc.s == LTE:
                pyFunc.getSym()
                if pyFunc.s == IDENT:
                    print('LTE: ' + str(v1) + ' '+  str(pyFunc.val))
                    pyFunc.getSym()
                elif pyFunc.s == NUM:
                    print('LTE: ' + str(v1) + ' '+  str(pyFunc.val))
                    pyFunc.getSym()       
def simpleStmt():
    if pyFunc.s == IDENT:
        var = pyFunc.val
        pyFunc.getSym()
        if pyFunc.s == EQ:
            pyFunc.getSym()
            e = expr()
            print('load: ' + var + ' ' + str(e))
def returnStmt():
    global commset
    code = ''
    if pyFunc.s == RETURN:
        pyFunc.getSym()
        code = code + 'ret: e' + str(commset)
        print(code)
        print('e'+str(commset)+':')
        expr()
        print('end e'+str(commset))
        commset = commset+1
def expr():
    t = term()
    if pyFunc.s == PLUS:
        pyFunc.getSym()
        t2 = term()
        print("sum: " + str(t) + ' ' + str(t2))
    if pyFunc.s == MINUS:
        pyFunc.getSym()
        t2 = term()
        print("min: " + str(t) + ' ' + str(t2))
    return t
def term():
    t = factor()
    if pyFunc.s == STAR:
        pyFunc.getSym()
        t2 = factor()
        print("mul: " + str(t) + ' ' + str(t2))
    if pyFunc.s == SLASH:
        pyFunc.getSym()
        t2 = factor()
        print("div: " + str(t) + ' ' + str(t2))
    return t
def factor():
    if pyFunc.s == NUM:
        val = pyFunc.val
        print('get: ' + str(val))
        pyFunc.getSym()
        return val
    if pyFunc.s == IDENT:
        val = pyFunc.val
        print('get: ' + str(val))
        pyFunc.getSym()
        return val
    elif pyFunc.s == LPAREN:
        pyFunc.getSym()
        e = expr()
        if pyFunc.s == RPAREN:
            pyFunc.getSym()
            return e
print("Test 1")
print()
simplePy('''
import OhiMark
def main:
  a = 4
  b = 6
  c = 0
  x = 0.1
  y = 1.4
  while(a < b or b < c):
    a = a + 1;
  x = x / 2
  while(x >= y):
    x = x / 2
  b = 9
  return 0
;
''')
print()
print("Test 2")
print()
simplePy('''
def main:
  d = 1
  for c in range(7,100,1):
    d = d + c
  h = 0
  for g in range(20,200,8):
    for a in range(1,2,1):
      h = h + a * g
  return h ;
''')
print()
print("Test 3")
print()
simplePy('''
def main:
  if(a < b):
    x = x + 1
  elif a == b:
    x = x + 11
  else:
    a = a + 2
  return g ;
''')
print()
print("Test 4")
print()
simplePy('''
def main:
  if(b == 1):
    a = b
  elif(b == 2):
    b = a
  else:
    a = 0
    b = 0
  return 0
  ;
  ''')
