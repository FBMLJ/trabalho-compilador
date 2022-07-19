

class Arvore:
    
    erro_instancia = []
    def __init__(self, producao, pai=None, token_aceito = None):
        self.nome = producao.nome
        self.folha = producao.eh_terminal
        self.filhos = []
        self.validada = False
        self.pai = pai
        self.token_lido = token_aceito

    def podar(self):

        if self.folha:
            if self.validada:
                return True, [self.token_lido]
            else:
                Arvore.erro_instancia.append(self)
                return False, []

        matriz_token_lido = []

        for i in range(len(self.filhos)-1,-1,-1):
            filho = self.filhos[i]
            # filho é composição de produções
            validador = True
            vetor = []
            vetor_token_lido = []

            for f in filho:
                # f -> produção (podendo ser terminal ou não)
                valor, token_lido = f.podar()
                vetor.append(valor)
                vetor_token_lido += token_lido
                validador = validador and valor
                if not validador:
                    break

            if not validador:
                self.filhos.pop(i) # filho não reconhecido
            else:
                matriz_token_lido = [vetor_token_lido] +  matriz_token_lido

        if len(self.filhos) > 0: # algum filho foi reconhecido na árvore
            self.filhos = self.filhos[0]
            self.validada = True
            # cada linha representa os tokens reconhecidos por um nó da árvore
            return True, matriz_token_lido[0]
        else:
            # Arvore.erro_instancia.append(self)        
            return False, []