

# falta implementar 
import token
from torch import le


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
            print(len(token_lido))
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
            # print(matriz_token_lido[0])
            # print(len(self.filhos) == len(matriz_token_lido))
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



#  criando as producoes

# TERMINAIS
producao_numero = Producao("NUMERO", eh_terminal= True, reconhecedor_terminal= lambda x: x.token_nome == "NUMBER")
# 28.
producao_operador_aditivo = Producao("OPERADOR ADITIVO", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_lido in "+-")
# 31.
producao_operador_multiplicativo = Producao("OPERADOR MULTIPLICATIVO", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_lido in "*/")
producao_abre_colchetes = Producao("ABRE COLCHETES", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_lido == "[")
producao_fecha_colchetes = Producao("FECHA COLCHETES", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_lido == "]")
producao_abre_parenteses = Producao("ABRE PARÊNTESES", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_lido == "(")
producao_fecha_parenteses = Producao("FECHA PARÊNTESES", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_lido == ")")
producao_identificador = Producao("ID", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_nome == "ID")
# 25.
producao_operador_logico = Producao("OPERADOR LOGICO",eh_terminal= True,reconhecedor_terminal=lambda x: x.token_nome == "OPERADOR_LOGICO")

# --------------------------------

# NÃO-TERMINAIS

# 1. programa→ lista-de-declaracao
producao_programa = Producao("PROGRAMA")

# 2. lista-de-declaracao → declaracao lista-de-declaração’
producao_ld = Producao("LISTA DECLARAÇÃO")

# 3. lista-de-declaração’ → declaracao lista-de-declaração’ | ε
producao_ld1 = Producao("LISTA DECLARAÇÃO'")

# 4. declaracao → var-declaracao | fun-declaracao
producao_decl = Producao("DECLARAÇÃO")

# 5. var-declaracao → especificador-de-tipo ID ; | especificador-de-tipo ID [ NUM ] ;
producao_var_decl = Producao("VAR-DECLARAÇÃO")

# 6. especificador-de-tipo → int | void
producao_tipo = Producao("TIPO", eh_terminal=True, reconhecedor_terminal= lambda x:x.token_lido in ["int", "void"])

# 7. fun-declaracao → especificador-de-tipo ID ( parametros ) compound-stmt
producao_fun_decl = Producao("FUN-DECLARAÇÃO")

# 8. parametros → parametro-list | void
producao_params = Producao("PARAMETROS")

# 9. parametro-list → parametro parametro-list’
producao_params_list = Producao("PARAMETRO-LIST")

# 10. parametro-list’ → , parametro parametro-list’ | ε

producao_params_list1 = Producao("PARAMETRO-LIST'")

# 11. parametro → especificador-de-tipo ID | especificador-de-tipo ID [ ]
producao_param = Producao(
    "PARAMETRO", derivacao=[
    [producao_tipo, producao_identificador],
    [producao_tipo, producao_identificador, producao_abre_colchetes, producao_fecha_colchetes]
])

# 12. compound-stmt → { declaracao-locais statement-list }
producao_compound_stmt = Producao("COMPOUND-STMT")

# 13. declaracao-locais → var-declaracao declaracao-locais’ | declaracao-locais’
producao_decl_loc = Producao("DECLARACAO-LOCAIS")

# 14. declaracao-locais’ → var-declaracao declaracao-locais’ | ε
producao_decl_loc1 = Producao("DECLARACAO-LOCAIS'")

# 15.
producao_stmt_list = Producao("STATEMENT-LIST")
# 16.
producao_stmt_list1 = Producao("STATEMENT-LIST'")
# 18.
producao_exp_stmt = Producao("EXPRESSAO-STMT")
# 19.
producao_sel_stmt = Producao("SELECAO-STMT")
# 20.
producao_iter_stmt = Producao("ITERACAO-STMT")
# 21.
producao_ret_stmt = Producao("RETURN-STMT")

# 22. expressao → var = expressao | expressao-simples
producao_expressao = Producao("EXPRESSAO")

# 23. var → ID | ID [ expressao ]
producao_var = Producao("VAR")

# 24. expressao-simples → expressao-aditiva operador-logico expressao-aditiva | expressao-aditiva
producao_expressao_simples = Producao("EXPRESSAO SIMPLES")

# 26. expressao-aditiva → termo expressao-aditiva’
producao_expressao_aditiva = Producao("EXPRESSAO ADITIVA")


producao_token_atribuicao = Producao("=", eh_terminal= True, reconhecedor_terminal= lambda x: x.token_nome == "ATRIBUICAO")

# 29. termo => fator termo'
producao_termo = Producao("TERMO")

# 32. fator → ( expressao ) | var | chamada | NUM
producao_fator = Producao("FATOR")


# 30. termo’ → operador-multiplicativo fator termo’ | ε
producao_termo1 = Producao("TERMO'")


# 27. expressao-aditiva’ → operador-aditivo termo expressao-aditiva’ | e
producao_expressao_aditiva1 = Producao("EXPRESSAO ADITIVA'")


# Faltam instanciar as produções 33,34,35,36, 17
# DERIVAÇÕES
producao_var.derivacao = [
    [producao_identificador], 
    [producao_identificador, producao_abre_colchetes, producao_expressao, producao_fecha_colchetes]
]

producao_expressao.derivacao = [
    [producao_var, producao_token_atribuicao, producao_expressao],
    [producao_expressao_simples]
]

producao_expressao_simples.derivacao = [
    [producao_expressao_aditiva, producao_operador_logico, producao_expressao_aditiva],
    [producao_expressao_aditiva]
]

producao_expressao_aditiva.derivacao  = [
    [producao_termo, producao_expressao_aditiva1]
]
producao_expressao_aditiva1.derivacao = [
    [producao_operador_aditivo, producao_termo, producao_expressao_aditiva1],
    []
]
producao_termo.derivacao = [
    [producao_fator, producao_termo1]
]
producao_termo1.derivacao = [
    [producao_operador_multiplicativo, producao_fator, producao_termo1],
    []
]

# SEM CHAMADA (ADICONAR ESTA COISA PLS)
producao_fator.derivacao = [
    [producao_abre_parenteses, producao_expressao, producao_fecha_parenteses],
    [producao_var],
    [producao_numero],
    #[producao_chamada]
]

def getAnalisadorSintatico(tokens):
    analisador=AnalisadorSintatico(tokens ,  producao_inicial=producao_expressao)
    print(analisador.reconhece())
    # print(analisador.ultima_linha_lido)
    arvore = analisador.arvore
    valor, token_lido = arvore.limpar_arvore()
    # print(arvore.validada)
    # print(tokens)
    # print(token_lido)
    print(arvore.raiz(tokens,token_lido))
    # print(arvore.filhos)

    # print(arvore.getErro())
    # print(arvore.validada)
    