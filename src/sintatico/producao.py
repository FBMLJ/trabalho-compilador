# classe que determinam as produções do gramatica
class Producao:
    def __init__(self, nome , eh_terminal = False, derivacao = [], reconhecedor_terminal = None):
        self.eh_terminal = eh_terminal
        self.derivacao = derivacao
        self.reconhecedor_terminal = reconhecedor_terminal
        self.nome = nome
#  criando as producoes

# TERMINAIS
producao_virgula = Producao("VIRGULA", eh_terminal=True, reconhecedor_terminal=lambda x: x==",")
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
producao_ponto_virgula = Producao("PONTO E VIRGULA", eh_terminal=True, reconhecedor_terminal= lambda x: x.token_lido == ";")
producao_return  = Producao("RETURN", eh_terminal=True, reconhecedor_terminal= lambda x: x.token_lido == "return")
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

#17. statement → expressao-stmt | compound-stmt | selecao-stmt | iteracao-stmt | return-stmt
producao_statement = Producao("STATEMENT")
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

# 33. chamada → ID ( argumentos )
producao_chamada = Producao("CHAMADA")

# 34. chamada -> argumentos-list | ε
producao_argumentos = Producao("ARGUMENTOS")

# 35. argumentos-list → expressao argumentos-list’
producao_arg_list = Producao("ARGUMENTOS-LIST")

# 36.  argumentos-list’ → , expressao argumentos-list’ | ε
producao_arg_list1 = Producao("ARGUMENTOS-LIST'")


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

producao_fator.derivacao = [
    [producao_abre_parenteses, producao_expressao, producao_fecha_parenteses],
    [producao_var],
    [producao_numero],
    #[producao_chamada]
]

producao_exp_stmt.derivacao = [
    [producao_expressao, producao_ponto_virgula],
    [producao_ponto_virgula]
]

producao_ret_stmt.derivacao = [
    [producao_return, producao_ponto_virgula],
    [producao_return, producao_expressao, producao_ponto_virgula]
]

producao_arg_list.derivacao = [
    [producao_expressao, producao_arg_list]
]

producao_arg_list1.derivacao = [
    [producao_virgula, producao_expressao, producao_arg_list1],
    []
]

producao_argumentos.derivacao = [
    [producao_arg_list],
    []
]

producao_chamada.derivacao = [
    [producao_identificador, producao_abre_parenteses, producao_argumentos, producao_fecha_parenteses]
]

producao_statement.derivacao = [
    [producao_exp_stmt],
    [producao_ret_stmt]
]


producao_stmt_list.derivacao = [
    [producao_stmt_list1],
    [producao_statement, producao_stmt_list1]
]

producao_stmt_list1.derivacao = [
    [producao_statement, producao_stmt_list1],
    []
]

def get_producao_raiz():
    return producao_stmt_list