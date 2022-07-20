from .arvore import Arvore

# classe responsavel pela analise sintatica
class AnalisadorSintatico:
    def __init__(self, tokens,  producao_inicial) :
        self.tokens = tokens # tokens lidos pelo Léxico
        # criando estado original
        self.producoes = [producao_inicial] # padrão = programa -> lista-de-declaracao
        self.arvore = Arvore(producao_inicial)
        self.eh_reconhecido = False
        self.contador = 0
        self.lista_token = []
        # usamos pilha para reconhecer os tokens, as produções e a árvore 
        self.pilha = [{"tokens": tokens, "producoes": self.producoes, "arvore": [self.arvore]}]
        # pilha mantem registro de que regra de produção foi adotada em que ponto da análise
        # sintática, para facilitar tentativa-e-erro

    def reconhece(self, identificadores):
        while True:
            # caso a pilha fique vazia quer dizer que não fomos capazes de reconhecer o programa
            if len(self.pilha) == 0:
                self.eh_reconhecido = False
                break
            atual = self.pilha.pop()

            if (not atual["tokens"]) and (not atual["producoes"]): # ε
                self.eh_reconhecido = True
                break

            elif not atual["tokens"] and atual["producoes"]: # caso produções aceitem ε, precisamos abri-las
                proxima_producao = atual["producoes"][0]
                proxima_arvore = atual["arvore"][0]
                self.desenvolve_producao(atual, proxima_producao.derivacao, proxima_arvore)
                continue

            elif not atual["producoes"]: # possui token mas não tem produções 
                continue
            
            # CASO CONVENCIONAL - POSSUÍMOS TOKENS E PRODUÇÕES
            # pegando o primeiro token e a primeira producao
            proxima_producao = atual["producoes"][0]
            proximo_token = atual["tokens"][0]
            proxima_arvore = atual["arvore"][0]

            # verificando se a produção é terminal ou não

            if not proxima_producao.eh_terminal:
                # caso seja terminal, adicionaremos na lista todas as produções derivadas trocando pela produção original
                self.desenvolve_producao(atual, proxima_producao.derivacao, proxima_arvore)
                continue
            else:
                # caso seja terminal vamos fazer uma verificação de reconhecimento do primeiro token
                if proxima_producao.reconhecedor_terminal(proximo_token):
                    proxima_arvore.validada = True
                    proxima_arvore.token_lido = proximo_token

                    if proximo_token.token_nome == "ID": # verifica se identificador está na tabela
                        proxima_arvore.validada = (proximo_token.token_lido in identificadores) or (proximo_token.token_lido == "main")
                        if not proxima_arvore.validada:
                            self.eh_reconhecido = False
                            break
                        
                    #  caso seja o último token a ser reconhecido, podemos fazer as seguintes ações
                    if len(atual["tokens"]) == 1:
                        #  validar também caso seja a ultima produção
                        if len(atual["producoes"] ) == 1:
                            self.eh_reconhecido = True
                            break
                        else:
                            self.pilha.append({"tokens": [],  "producoes": atual["producoes"][1:] , "arvore": atual["arvore"][1:]}) # não temos mais tokens, mas ainda temos produções
                            continue
                    # caso tenha apenas uma produção terminal e não somente um token não é mais possivel validar entao o descartamos
                    elif len(atual["producoes"]) == 1:
                        continue
                    # caso nenhuma situação acima tenha acontecido, removemos o primeiro token e a primeira produção e adicionamos de novo na pilha
                    self.lista_token.append(proximo_token)
                    self.pilha.append({"tokens": atual["tokens"][1:],  "producoes": atual["producoes"][1:], "arvore": atual["arvore"][1:] })
                
                continue
                
        return self.eh_reconhecido

    def desenvolve_producao(self, atual, derivacao, proxima_arvore):
        for producoes in derivacao:
            vetor_arvore = []
            
            for producao in producoes:
                arvore = Arvore(producao,pai=proxima_arvore)
                vetor_arvore.append(arvore)

            proxima_arvore.filhos.append(vetor_arvore)
            self.pilha.append({"tokens": atual["tokens"] , "producoes": producoes+atual["producoes"][1:], "arvore": vetor_arvore+atual["arvore"][1:]})
            # cortamos a produção que já foi aberta ([1:]) 



from .producao import get_producao_raiz
def get_analisador_sintatico(tokens, identificadores):
    print("Lista de Identificadores: ", identificadores)
    analisador=AnalisadorSintatico(tokens, producao_inicial=get_producao_raiz())
    eh_valido = analisador.reconhece(identificadores)
    
    arvore = analisador.arvore
    arvore.podar()
    if eh_valido:
        print("Programa valido")
    else:
        print("Programa invalido \nErros:")
        # arvore.raiz(tokens,token_lido)
    
    
        for j in range(len(tokens)):
            i = tokens[j]
            if i not in analisador.lista_token:
                print("Ocorreu um erro ao redor do token {}, na linha {}, ultimo token reconhecido {} linha {}".format(i.token_lido, i.linha, tokens[j-1].token_lido, tokens[j-1].linha))
                break