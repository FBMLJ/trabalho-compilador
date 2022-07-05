

# falta implementar 
class Arvore:
    def __init__(self, producao):
        self.nome = producao.nome
        self.folha = producao.eh_terminal
        self.filhos = []
        self.validada = False
    
    def limpar_arvore(self):
        if self.folha:
            if self.validada:
                return True
            else: 
                return False
        

        for i in range(len(self.filhos)-1,-1,-1):
            filho = self.filhos[i]
            validador = True
            for  f in filho:
                validador = validador and f.limpar_arvore()
            if not validador:
                self.filhos.pop(i)
        if len(self.filhos) > 0:
            print(self.filhos[0])
            self.filhos = self.filhos[0]
            return True
        else:

            return False

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
        self.arvore = Arvore(producao_inicial)
        # falta implementar a arvore
        self.arvores = None
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
                        vetor_arvore.append(Arvore(j))
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
                    vetor_arvore.append(Arvore(j))
                proxima_arvore.filhos.append(vetor_arvore)
                self.pilha.append({"tokens": atual["tokens"] , "producoes": i+atual["producoes"][1:], "arvore": vetor_arvore+atual["arvore"][1:]})
            return self.reconhece()
        else:
            # caso seja terminal vamos fazer uma verificação se reconhece o primeiro token
            if proxima_producao.reconhecedor_terminal(proximo_token):
                proxima_arvore.validada = True
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
                return self.reconhece()



#  criando as producoes

# TERMINAIS
producao_numero = Producao("NUMERO", eh_terminal= True, reconhecedor_terminal= lambda x: x.token_nome == "NUMBER")
producao_operador_aditivo = Producao("OPERADOR ADITIVO", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_lido in "+-")
producao_operador_multiplicativo = Producao("OPERADOR MULTIPLICATIVO", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_lido in "*/")
producao_abre_colchetes = Producao("ABRE COLCHETES", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_lido == "[")
producao_fecha_colchetes = Producao("FECHA COLCHETES", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_lido == "]")
producao_abre_parenteses = Producao("ABRE PARÊNTESES", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_lido == "(")
producao_fecha_parenteses = Producao("FECHA PARÊNTESES", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_lido == ")")
producao_identificador = Producao("ID", eh_terminal= True , reconhecedor_terminal= lambda x: x.token_nome == "ID")
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


producao_stmt_list = Producao("STATEMENT-LIST")
producao_stmt_list1 = Producao("STATEMENT-LIST'")
producao_exp_stmt = Producao("EXPRESSAO-STMT")
producao_sel_stmt = Producao("SELECAO-STMT")
producao_iter_stmt = Producao("ITERACAO-STMT")
producao_ret_stmt = Producao("RETURN-STMT")
producao_exp_stmt = Producao("EXPRESSAO")

# 22. expressao → var = expressao | expressao-simples
producao_expressao = Producao("EXPRESSAO")

# 23. var → ID | ID [ expressao ]
producao_var = Producao("VAR")

# 24. expressao-simples → expressao-aditiva operador-logico expressao-aditiva | expressao-aditiva
producao_expressao_simples = Producao("EXPRESSAO SIMPLES")

# 26. expressao-aditiva → termo expressao-aditiva’
# 27. expressao-aditiva’ → operador-aditivo termo expressao-aditiva’ | ε
producao_expressao_aditiva = Producao("EXPRESSAO ADITIVA")


producao_token_atribuicao = Producao("=", eh_terminal= True, reconhecedor_terminal= lambda x: x.token_nome == "ATRIBUICAO")

#29 termo => fator termo'
producao_termo = Producao("TERMO")

#32. fator → ( expressao ) | var | chamada | NUM
producao_fator = Producao("FATOR")


#30. termo’ → operador-multiplicativo fator termo’ | ε
producao_termo1 = Producao("TERMO'")


#27. expressao-aditiva’ → operador-aditivo termo expressao-aditiva’ | e
producao_expressao_aditiva1 = Producao("EXPRESSAO ADITIVA'")
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
    arvore = analisador.arvore
    arvore.limpar_arvore()
    print(len(arvore.filhos))