from Atomato import Atomato



class Scan:
    def __init__(self, nome_arquivo):
        self.nome_arquivo  = nome_arquivo
        self.interador = 0
        


    def nextCharSemAcrescimo(self):
        with open(self.nome_arquivo,'r',encoding = 'utf-8') as f:
            try:
                valor =  f.read()[self.interador]
            except(IndexError):
                return ""
            return valor

    def nextChar(self):
        
        with open(self.nome_arquivo,'r',encoding = 'utf-8') as f:
            valor =  f.read()[self.interador]
            
            
            self.interador +=1
            return valor

    def getTokens(self):
        current_token = ""
        tokens = []
        parada = False
        while self.nextCharSemAcrescimo() != "" and not parada:
            _char = self.nextChar()
            if _char in []:
                tokens.append(current_token)
                current_token = ''
            
            current_token= current_token + _char
            
        print(tokens)
l = Scan("input.txt")
l.getTokens()

