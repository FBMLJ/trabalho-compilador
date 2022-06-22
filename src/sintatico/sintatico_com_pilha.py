

# falta implementar 
class Arvore:
    def __init__(self, nome, eh_folha, filhos):
        self.nome = nome
        self.folha = eh_folha
        self.filhos = filhos

# classe que determinam as produções do gramatica
class Producao:
    def __init__(self, nome , eh_terminal = False, derivacao = [], reconhecedor_terminal = None):
        self.eh_terminal = eh_terminal
        self.derivacao = derivacao
        self.reconhecedor_terminal = reconhecedor_terminal
        self.nome = nome

    
    


# classe responsavel pela analise sintatica
class AnalisadorSintatico:
    def __init__(self, tokens,  producao_inicial) :
        self.tokens = tokens
        # criando estado original
        self.producoes = [producao_inicial]
        # falta implementar a arvore
        self.arvores = None
        # usamos pilha para reconhece o token
        self.pilha = [{"tokens": tokens,"producoes": self.producoes}]

    def reconhece(self):
        # caso a pilha fique vazia quer dizer que não fomos capazes de reconhecer o programa
        if len(self.pilha) == 0:
            return False
        atual = self.pilha.pop()

        # pegando o primeiro token e a primeira producao
        proxima_producao = atual["producoes"][0]
        proximo_token = atual["tokens"][0]

        # verificando se a produção é terminal ou não
        if not proxima_producao.eh_terminal:
            # caso seja vamos adicionar na lista todas as produções derivadas trocando pela produção original
            for i in proxima_producao.derivacao:
                self.pilha.append({"tokens": atual["tokens"] , "producoes": i+atual["producoes"][1:]})
            return self.reconhece()
        else:
            # caso seja terminal vamos fazer uma verificação se reconhece o primeiro token
            if proxima_producao.reconhecedor_terminal(proximo_token):
                #  no caso de ser o ultimo token a ser reconhecido podemos fazer as seguintes ações
                if len(atual["tokens"]) == 1:
                        #  validar caso tambem seja a ultima produção
                        if len(atual["producoes"] ) == 1:
                            return True
                        else:
                            # descarta o atual porque não é possivel mais valida-lo
                            return self.reconhece()
                # caso tenha apenas uma produção terminal e não somente um token não é mais possivel valida entao o descartamos
                elif len(atual["producoes"]) == 1:
                    return self.reconhece()
                # caso nenhum situação acima ocorreu removemos o primeiro token a primera produção e adicionamos denovo na pilha
                self.pilha.append({"tokens": atual["tokens"][1:],  "producoes": atual["producoes"][1:] })
                return self.reconhece()
            else:
                # caso o token terminal não recoheça o descartamos
                return self.reconhece()




producao_numero = Producao("NUMERO", eh_terminal= True, reconhecedor_terminal= lambda x: x.token_nome == "NUMBER")
producao_operador_aditivo = Producao("OPEADOR ADITIVO", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_lido == "+" or x.token_lido == "-")
#  criando as producoes
producao_expressa_aditiva = Producao("EXPRESSAO ADITIVA")
producao_var = Producao("VAR"), 
producao_sinal_igual = Producao("=", eh_terminal= True )
producao_expressao_simples = Producao("EXPRESSA SIMPLES")
producao_expressa = Producao("EXPRESSAO")
# remover daqui para baixo

producao_expressa_aditiva.derivacao = [
    [producao_numero, producao_operador_aditivo, producao_expressa_aditiva],
    [producao_numero]
]


def getAnalisadorSintatico(tokens):
    analisador=AnalisadorSintatico(tokens ,  producao_inicial=producao_expressa_aditiva)
    print(analisador.reconhece())