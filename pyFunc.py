IMPORT = 1;HASH = 2;INT = 3;IDENT = 4;LT = 5; GT = 6; PERIOD = 7;MAIN = 8;
LPAREN = 9; RPAREN = 10;LCURL=11;RCURL=12; IF = 13; SWITCH = 14;WHILE = 15;
DO = 16;FOR = 17;EQ = 19;RETURN = 20; FLOAT = 21;TRUE = 22; FALSE = 23;
STAR = 24; PERCENT = 25; NEQ = 26; EQUAL = 27; LT = 28; LTE = 29; SHIFTL = 30; GT = 31;
GTE = 32; SHIFTR = 33; DBLBAR = 34; DBLAMP = 35; PLUS = 36; MINUS = 37; SEMICOLON = 38; FLOAT = 39; DOUBLE = 40;
BOOL = 41;SLASH=42;NUM = 43;CHAR = 44;AND = 45;OR = 46;ELSE = 47;CASE = 48;BREAK = 49; DEFAULT = 50;
COLON = 51; DEF = 52; INDENT = 53;IN = 54; RANGE = 55; COMMA = 56; ELIF = 57;
keywords = ((IMPORT,'import'),(INT,'int'),(FLOAT,'float'),(DOUBLE,'double'),(BOOL,'bool'),(MAIN,'main'),(IF,'if'),(SWITCH,'switch'),\
            (WHILE,'while'),(DO,'do'),(FOR,'for'),(RETURN,'return'),(TRUE,'true'),(FALSE,'false'),
            (CHAR,'char'),(ELSE,'else'),(CASE,'case'),(BREAK,'break'),(DEFAULT,'default'),(DEF,'def'),
            (IN,'in'),(RANGE,'range'),(ELIF,'elif'),(OR,'or'),(AND,'and'))
def init(src):
    global f,ch,index,s,val
    f = src
    ch = src[0]
    index = 0
    s = None
    val = None
    getSym()
def getChar():
    global f,ch,index
    if index < len(f):
        ch = f[index]
        index = index+1
def getSym():
    global f,ch,index,s,val
    space = 0
    if ch == '':
        pass
    while ch in ' \n':
        if ch == ' ':
            space = space + 1
            if (space == 2):
                s = INDENT
                space = 0
                getChar()
                return
        else:
            space = 0
        getChar();
    if ch == chr(0):
        if index < len(f):
            getChar()
        else:
            s = EOF
    elif 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
        ident()
    elif '0' <= ch <= '9':
        num()
    elif ch == '#':
        s = HASH
        getChar()
    elif ch == ';':
        s = SEMICOLON
        getChar()
    elif ch == ':':
        s = COLON
        getChar()
    elif ch == '*':
        s = STAR
        getChar()
    elif ch == '/':
        getChar()
        if ch == '=':
            s = SLSHEQ
            getChar()
        else:
            s = SLASH
    elif ch == '%':
        getChar()
        if ch == '=':
            s = PCNTEQ
            getChar()
        else:
            s = PERCENT
    elif ch == '^':
        getChar()
        if ch == '=':
            s = HATEQ
            getChar()
        else:
            s = HAT
            getChar()
    elif ch == '=':
        getChar()
        if ch == '=':
            getChar()
            s = EQUAL
        else:
            s = EQ
    elif ch == '!':
        getChar()
        if ch == '=':
            s = NEQ
            getChar()
        else:
            s = EXC
    elif ch == '~':
        s = TILDE
        getChar()
    elif ch == '<':
        getChar()
        if ch == '=':
            s = LTE
            getChar()
        elif ch == '<':
            getChar()
            if ch == '=':
                s = SHIFTLEQ
                getChar()
            else:
                s = SHIFTL
                getChar()
        else:
            s = LT
    elif ch == '>':
        getChar()
        if ch == '=':
            s = GTE
            getChar()
        elif ch == '>':
            getChar()
            if ch == '=':
                s = SHIFTREQ
                getChar()
            else:
                s = SHIFTR
                getChar()
        else:
            s = GT
    elif ch == '|':
        getChar()
        if ch == '|':
            s = OR
            getChar()
        elif ch == '=':
            s = BAREQ
            getChar()
        else:
            s = BAR
    elif ch == '&':
        getChar()
        if ch == '&':
            s = AND
            getChar()
        elif ch == '=':
            s = AMPEQ
            getChar()
        else:
            s = AMP
    elif ch == ',':
        s = COMMA
        getChar()
    elif ch == '.':
        getChar()
        if ch == '.':
            getChar()
            if ch == '.':
                s = TRIPDOT
                getChar()
        else:
            s = PERIOD
    elif ch == ':':
        s = COLON
        getChar()
    elif ch == '(':
        s = LPAREN
        getChar()
    elif ch == ')':
        s = RPAREN
        getChar()
    elif ch == '[':
        s = LBRACK
        getChar()
    elif ch == ']':
        s = RBRACK
        getChar()
    elif ch == '{':
        s = LCURL
        getChar()
    elif ch == '}':
        s = RCURL
        getChar()
    elif ch == '+':
        getChar()
        if ch == '+':
            s = DBLPLUS
            getChar()
        elif ch == '=':
            s = PLUSEQ
            getChar()
        else:
            s = PLUS
    elif ch == '-':
        getChar()
        if ch == '-':
            s = DBLMINUS
            getChar()
        elif ch == '=':
            s = MINUSEQ
            getChar()
        elif ch == '>':
            s = ARROW
            getChar()
        else:
            s = MINUS
def ident():
    global s, val
    start = index
    while ('A' <= ch <= 'Z') or ('a' <= ch <= 'z') or ('0' <= ch <= '9'):
        getChar()
    for kw, match in keywords:
        if f[start-1:index-1] == match:
            s = kw
            return
    s, val = IDENT, f[start-1:index-1]
def num():
    global s, val
    start = index
    val = 0
    while ('0' <= ch <= '9'):
        val = val * 10
        val = val + int(ch)
        getChar()
    if ch == '.':
        s = NUM
        getChar()
        x = 0
        while('0' <= ch <= '9'):
            getChar()
            x = x + val
        x = int(x)/(len(str(x))*10)
        val = val + x
    else:
        s = NUM
