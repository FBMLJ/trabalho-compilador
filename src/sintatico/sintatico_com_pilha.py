from .arvore import Arvore

# classe responsavel pela analise sintatica
class AnalisadorSintatico:
    def __init__(self, tokens,  producao_inicial) :
        self.tokens = tokens
        # criando estado original
        self.producoes = [producao_inicial]
        self.arvore = Arvore(producao_inicial, linha=0)
        # falta implementar a arvore
        self.arvores = None
        self.ultima_linha_lido = -1
        # usamos pilha para reconhece o token
        self.pilha = [{"tokens": tokens,"producoes": self.producoes, "arvore": [self.arvore]}]

    def reconhece(self):
        # caso a pilha fique vazia quer dizer que não fomos capazes de reconhecer o programa
        if len(self.pilha) == 0:
            return False
        atual = self.pilha.pop()

        if (not atual["tokens"]) and (not atual["producoes"]): # ε
            return True
        elif not atual["tokens"] or not atual["producoes"]:
            if atual["producoes"]:
                proxima_producao = atual["producoes"][0]
                proxima_arvore = atual["arvore"][0]
                

                for i in proxima_producao.derivacao:
                    vetor_arvore = []
                    for j in i:
                        vetor_arvore.append(Arvore(j,pai=proxima_arvore,aceita_vazio=True))
                    proxima_arvore.filhos.append(vetor_arvore)
                    
                    self.pilha.append({"tokens": atual["tokens"] , "producoes": i+atual["producoes"][1:], "arvore": vetor_arvore+atual["arvore"][1:]})
            
            return self.reconhece()
        
        # pegando o primeiro token e a primeira producao
        proxima_producao = atual["producoes"][0]
        proximo_token = atual["tokens"][0]
        proxima_arvore = atual["arvore"][0]

        # verificando se a produção é terminal ou não
        if not proxima_producao.eh_terminal:
            # caso seja vamos adicionar na lista todas as produções derivadas trocando pela produção original
            for i in proxima_producao.derivacao:
                vetor_arvore = []
                for j in i:
                    vetor_arvore.append(Arvore(j, linha=proximo_token.linha,pai=proxima_arvore))
                proxima_arvore.filhos.append(vetor_arvore)
                self.pilha.append({"tokens": atual["tokens"] , "producoes": i+atual["producoes"][1:], "arvore": vetor_arvore+atual["arvore"][1:]})
            return self.reconhece()
        else:
            # caso seja terminal vamos fazer uma verificação se reconhece o primeiro token
            if proxima_producao.reconhecedor_terminal(proximo_token):
                proxima_arvore.validada = True
                proxima_arvore.token_lido =   proximo_token
                #  no caso de ser o ultimo token a ser reconhecido podemos fazer as seguintes ações
                if len(atual["tokens"]) == 1:
                        #  validar caso tambem seja a ultima produção
                        if len(atual["producoes"] ) == 1:
                            
                            return True
                        else:
                            # descarta o atual porque não é possivel mais valida-lo
                            self.pilha.append({"tokens": [],  "producoes": atual["producoes"][1:] , "arvore": atual["arvore"][1:] })
                
                            return self.reconhece()
                # caso tenha apenas uma produção terminal e não somente um token não é mais possivel valida entao o descartamos
                elif len(atual["producoes"]) == 1:
                    return self.reconhece()
                # caso nenhum situação acima ocorreu removemos o primeiro token a primera produção e adicionamos denovo na pilha
                self.pilha.append({"tokens": atual["tokens"][1:],  "producoes": atual["producoes"][1:], "arvore": atual["arvore"][1:] })
                return self.reconhece()
            else:
                # caso o token terminal não recoheça o descartamos
                        
                self.ultima_linha_lido = max([proximo_token.linha, self.ultima_linha_lido])
                
                return self.reconhece()



from .producao import get_producao_raiz
def getAnalisadorSintatico(tokens):
    analisador=AnalisadorSintatico(tokens ,  producao_inicial=get_producao_raiz())
    eh_validado = analisador.reconhece()
    
    arvore = analisador.arvore
    valor, token_lido = arvore.limpar_arvore()
    if eh_validado:
        print("Programa valido")
    else:
        print("Programa invalido \nErros:")
    arvore.raiz(tokens,token_lido)
    