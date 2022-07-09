

class Arvore:
    interador = 0
    
    erro_instancia = []
    def __init__(self, producao, linha=None, pai=None, aceita_vazio = False, token_aceito = None):
        self.nome = producao.nome
        self.folha = producao.eh_terminal
        self.filhos = []
        self.validada = False
        self.pai = pai
        self.aceita_vazio = aceita_vazio
        self.token_linha = linha
        self.token_lido = token_aceito
    def _antecessor_validado(self):
        temp = self
        while temp.pai != None:
            if temp.pai.validada:
                return True
            temp = temp.pai
        return False

    def get_linha(self):

        if self.token_linha == None:
            
            return self.pai.get_linha()
            
        else:
            return self.token_linha
    def raiz(self, token, token_lido):
        if len(token_lido) == len(token):
            return True
        else:
            
            for i in token:
                if not i in token_lido:
                    print("Erro a reconhecer o token {}, na linha {}".format(i.token_lido, i.linha))
            return False

    def limpar_arvore(self):
        Arvore.interador+=1
        if self.folha:
            if self.validada:
                return True, [self.token_lido]
            else:
                Arvore.erro_instancia.append(self)
                return False,  []
        

        matriz = []
        matriz_token_lido = []
        for i in range(len(self.filhos)-1,-1,-1):
            filho = self.filhos[i]
            validador = True
            vetor = []
            vetor_token_lido = []
            for  f in filho:
                valor, token_lido  = f.limpar_arvore()
                vetor.append(valor)
                
                
                vetor_token_lido +=  token_lido
                validador = validador and valor
                if not validador:
                    break
            # matriz_token_lido.append(vetor_token_lido)
            if not validador:
                
                self.filhos.pop(i)
            else:
                matriz_token_lido = [vetor_token_lido] +  matriz_token_lido
        if len(self.filhos) > 0:
            
            
           
            
            self.filhos = self.filhos[0]
            self.validada = True
            return True, matriz_token_lido[0]
        else:
            # Arvore.erro_instancia.append(self)        
            return False, []
    
    def getErro(cls):
        vetorErroMessagem = []
        for instancia in cls.erro_instancia:
            # if not instancia._antecessor_validado():
                vetorErroMessagem.append("Ocorreu um erro na {} ao tentar reconhecer {}".format(instancia.token_linha, instancia.nome))
        return vetorErroMessagem
