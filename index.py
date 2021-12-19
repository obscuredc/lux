import sys, random, colored
# open file
def Main():
    try:
        with open(sys.argv[1]) as file:
            Text = file.read()
            tokens = Lex(Text)
            parsed = Parse(tokens)
            #repr(parsed)
            program_exit_status = Execute(parsed)
            LuxExit(f"program terminated with status{str(program_exit_status)}")
            # finally, close
            file.close()
    except:
        LuxError("unknown error (did you provide a file?)")
def Unstable():
        with open(sys.argv[1]) as file:
            Text = file.read()
            tokens = Lex(Text)
            parsed = Parse(tokens)
            #repr(parsed)
            program_exit_status = Execute(parsed)
            LuxExit(f"program terminated with status{str(program_exit_status)}")
            # finally, close
            file.close()
class TTCommand:
    def __init__(self, idx, parameters, name):
        self.idx = idx
        self.params = parameters
        self.name = name
class TTInt:
    def __init__(self, idx, value):
        self.idx = idx
        self.value = value
#colors sometime
def LuxLog(message):
    print(f"[lux/{colored.fg('light_blue')}log{colored.attr('reset')}]: {message}")
def LuxWarn(message):
    print(f"[lux/{colored.fg('orange_4b')}warn{colored.attr('reset')}]: {message}")
def LuxError(message):
    print(f"[lux/{colored.fg('red')}fatal{colored.attr('reset')}]: {message}")
def LuxExit(message):
    print(f"[lux/{colored.fg('light_blue')}end{colored.attr('reset')}]: {message}")
class Lexer:
    def __init__(self, Raw):
        self.Raw = Raw      # raw text
        self.idx = 0          # current index num
        self.cc = self.Raw[0]       # current char
        self.endl = False
        self.tokens = []

        #STR
        self.AllowedCommandChar = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
        self.AllowedNumberChar = "0123456789"
        self.Whitespace = "\n\t "
        self.InComment = False
    def Main(self):
        while self.idx < len(self.Raw) and self.endl is False:
            if(self.cc in self.AllowedCommandChar and self.InComment is False):
                self.BuildCommand()
            elif(self.cc in self.AllowedNumberChar and self.InComment is False):
                self.BuildNumber()
            elif(self.cc in self.Whitespace and self.InComment is False):
                self.Continue()
            elif(self.cc == "#"):
                self.InComment = not(self.InComment)
                self.Continue()
            else:
                self.Continue()
        #finally add EOF
        self.tokens.append("EOF")
        #printoutLEX
        # for Token in self.tokens:
        #     if(isinstance(Token, TTInt)):
        #         print(str(Token.value) + " -NUM")
        #     elif(isinstance(Token, TTCommand)):
        #         print(Token.name + " -CMD")
        #     else:
        #         print("unknown token type")

        #return tokens
        return self.tokens

    def Continue(self):
        if self.idx+1 < len(self.Raw):
            self.idx += 1
            self.cc = self.Raw[self.idx]
        else:
            self.endl = True
    def BuildCommand(self):
        temp = ""
        while self.cc in self.AllowedCommandChar and self.endl is False:
            temp += self.cc
            self.Continue()
        self.tokens.append(TTCommand(self.idx, [], temp))
    def BuildNumber(self):
        temp = ""
        while self.cc in self.AllowedNumberChar and self.endl is False:
            temp += self.cc
            self.Continue()
        try:
            self.tokens.append(TTInt(self.idx, int(temp)))
        except:
            LuxError("instead of integer value, got unknown")
def Lex(raw):
    lexer = Lexer(raw)
    return lexer.Main()

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.endl = False
        self.temp = None
        self.idx = -1
        self.cc = None
        self.parsed = []
    def Main(self):
        self.Continue()
        while self.endl is False and self.idx < len(self.tokens):
            if(isinstance(self.cc, TTCommand)):
                if(self.temp is not None):
                    self.parsed.append(self.temp)
                self.temp = self.cc
                self.Continue()
            elif(isinstance(self.cc, TTInt)):
                try:
                    self.temp.params.append(self.cc)
                except:
                    pass
                self.Continue()
            elif(self.cc == "EOF"):
                self.parsed.append(self.temp)
                self.endl = True
                self.parsed.append("EOF")
        return self.parsed
    def Continue(self):
        self.idx+=1
        self.cc=self.tokens[self.idx]
def Parse(tokens):
    parser = Parser(tokens)
    return parser.Main()

def repr(parsed):
    for Token in parsed:
        if(Token != "EOF"):
            print(f"TOKEN {Token.name}")
            if len(Token.params) > 0:
                for P in Token.params:
                    print(f"TOKEN.params {P.value}")
            else:
                print("TOKEN.params *none")
        else:
            print("TOKEN EOF")
class Stack:
    def __init__(self, id):
        self.id = id
        self.R = []
class Enviorment:
    def __init__(self):
        self.stack = [] # must be the selected stacks.R
        self.textbuffer = ""
        self.stacks = []

        self.stacks.append(Stack(0))
        self.SetStackById(0)
    def GetStackById(self, id):
        for Stack in self.stacks:
            if(Stack.id == id):
                return Stack
        return False
    def SetStackById(self, id):
        if(self.GetStackById(id) is not False):
            stack=self.GetStackById(id)
            self.stack = stack.R 
        else:
            LuxLog(f"stack{id} is not a valid stack")
    def CreateStack(self, id):
        if self.GetStackById(id) is False:
            self.stacks.append(Stack(id))
        else:
            LuxError(f"there is already a stack of id{id}")
    def Repr(self):
        for Stack in self.stacks:
            LuxLog(f"STACK {str(Stack.id)}:")
            for value in Stack.R:
                LuxLog(f"    value: {str(value)}")
class Executor:
    def __init__(self, ptokens, env):
        self.ptokens = ptokens
        self.idx = -1
        self.cc = None
        self.env = env
        self.endl = False
        self.code = 0 #0->Success 1->warnings 2->Errors 3-> program ended itself
    def Continue(self):
        self.idx+=1
        self.cc=self.ptokens[self.idx]
    def Main(self):
        self.Continue()
        while self.endl is False and self.idx < len(self.ptokens):
            #wow if statments for commands here
            
            if(self.cc == "EOF"):
                self.endl = True
                break
            #print(f"[lux/log]: running {self.cc.name} on index{self.idx}")
            try:
            #IF STATMENTS FOR COMMANDS VV
                if(self.cc.name == "dummy"):
                    print("[lux/log]: dummy")
                elif(self.cc.name == "psh"):
                    self.env.stack.append(self.cc.params[0].value)
                elif(self.cc.name == "pop"):
                    self.env.stack.pop()
                elif(self.cc.name == "vstack"):
                    t=""
                    for N in self.env.stack:
                        t+=str(N) + " "
                    print(f"[lux/log]: {t}")
                    t=""
                elif(self.cc.name == "tbuf_psh"):
                    t=self.env.stack.pop()
                    self.env.textbuffer += chr(t)
                    t=""
                elif(self.cc.name == "tbuf_out"):
                    print(f"[lux/log]: {self.env.textbuffer}")
                elif(self.cc.name == "rem"):
                    pass
                elif(self.cc.name == "tbuf_ap"):
                    for Value in self.env.stack:
                        self.env.textbuffer += chr(Value)
                    self.env.stack = []
                elif(self.cc.name == "tbuf_rpsh"):
                    t=self.env.stack.pop()
                    self.env.textbuffer += str(t)
                elif(self.cc.name == "tbuf_cls"):
                    self.env.textbuffer = ""
                elif(self.cc.name == "add"):
                    t1=self.env.stack.pop()
                    t2=self.env.stack.pop()
                    self.env.stack.append(t1+t2)
                elif(self.cc.name == "sub"):
                    t1=self.env.stack.pop()
                    t2=self.env.stack.pop()
                    self.env.stack.append(t1-t2)
                elif(self.cc.name == "mul"):
                    t1=self.env.stack.pop()
                    t2=self.env.stack.pop()
                    self.env.stack.append(t1*t2)
                elif(self.cc.name == "div"):
                    t1=self.env.stack.pop()
                    t2=self.env.stack.pop()
                    self.env.stack.append(t1/t2)
                elif(self.cc.name == "jmp"):
                    self.idx = self.cc.params[0].value -2
                    self.Continue()
                elif(self.cc.name == "end"):
                    self.endl = True
                    self.code = 3
                elif(self.cc.name == "jmp_eq"):
                    t1=self.env.stack.pop()
                    t2=self.env.stack.pop()
                    self.env.stack.append(t2)
                    self.env.stack.append(t1)
                    if(t1==t2):
                        self.idx=self.cc.params[0].value -2
                        self.Continue()
                elif(self.cc.name == "jmp_ls"):
                    t1=self.env.stack.pop()
                    t2=self.env.stack.pop()
                    self.env.stack.append(t2)
                    self.env.stack.append(t1)
                    if(t1<t2):
                        self.idx=self.cc.params[0].value -2
                        self.Continue()
                elif(self.cc.name == "jmp_leq"):
                    t1=self.env.stack.pop()
                    t2=self.env.stack.pop()
                    self.env.stack.append(t2)
                    self.env.stack.append(t1)
                    if(t1<=t2):
                        self.idx=self.cc.params[0].value -2
                        self.Continue()
                elif(self.cc.name == "out"):
                    t=""
                    for N in self.env.stack:
                        if(N == 0):
                            break;
                        else:
                            t += chr(N)
                    LuxLog(t)
                elif(self.cc.name == "rev"):
                    self.env.stack.reverse()
                elif(self.cc.name == "cpy"):
                    t=self.env.stack.pop()
                    self.env.stack.append(t)
                    self.env.stack.append(t)
                elif(self.cc.name == "stk_s"):
                    if(self.env.GetStackById(self.cc.params[0].value) is False):
                        LuxError(f"no stack exists of id{self.cc.params[0].value}")
                    else:
                        self.env.SetStackById(self.cc.params[0].value)
                elif(self.cc.name == "stk_cls"):
                    self.env.stack = []
                elif(self.cc.name == "stk_c"):
                    self.env.CreateStack(self.cc.params[0].value)
                elif(self.cc.name == "stk_len"):
                    # self.env.stack.append(len(self.env.stack))
                    print(len(self.env.stack))
                elif(self.cc.name == "stk_rpr"):
                    self.env.Repr()
                elif(self.cc.name == "stk_del"):
                    self.env.stacks.pop(self.env.stacks.index(self.env.GetStackById(self.cc.params[0].value)))
                elif(self.cc.name == "io_word"):
                    v=input("[lux/cin]: ")
                    for Char in v:
                        self.env.stack.append(ord(Char))
                elif(self.cc.name == "io_num"):
                    v=input("[lux/cin]: ")
                    try:
                        v=int(v)
                    except:
                        v=0
                    self.env.stack.append(v)
                elif(self.cc.name == "outr"):
                    t=""
                    for Num in self.env.stack:
                        t+=str(Num)
                    LuxLog(t)
                elif(self.cc.name == "mpsh"):
                    for Value in self.cc.params:
                        self.env.stack.append(Value.value)
                elif(self.cc.name == "popto"):
                    t=self.env.stack.pop()
                    target=self.env.GetStackById(self.cc.params[0].value)
                    target.R.append(t)
                elif(self.cc.name == "rand"):
                    self.env.stack.append(random.randint(0, 100))
                #IF STATEMENTS FOR COMMANDS ^^
                elif (self.cc != "EOF"):
                    LuxError(f"command #{str(self.idx)} is unknown (name={str(self.cc.name)})")
                    self.code = 2
                if(self.cc != "EOF"):
                    self.Continue()
            except:
                LuxError(f"wrong amount of args applied or internal error at index{self.idx}")
                self.Continue()
        return self.code

def Execute(parsed_tokens):
    enviorment = Enviorment()
    executor = Executor(parsed_tokens, enviorment)
    return executor.Main()
#Main()     # normal run mode (error catch)
Unstable() #unstable run mode
