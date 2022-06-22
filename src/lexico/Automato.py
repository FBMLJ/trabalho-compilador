from string import ascii_letters

#Constantes
OTHER_SPECIAL_CHAR = '()[];\{\},'
CLOSE_CHAR = ' ()[];\{\}\n+-=<>*/!'
LETTER = ascii_letters
DIGITS:4 = '1234567890'
SPACE = ' \n\t'
OPERADOR = "+-*/"
TUDO = CLOSE_CHAR+LETTER+DIGITS+SPACE+OPERADOR
PALAVRAS_RESERVADAS = ["if","else","while","void","int","return"]

class Token:
    def __init__(self, token_nome, token_lido):
        self.token_nome = token_nome
        self.token_lido = token_lido
    def __str__(self):
        return "[{},{}]".format(self.token_lido,self.token_nome)

class Automato:
    def __init__(self, estados_de_aceitacao, transicoes, estados_tokens):
        self.token_lido = ''
        self.estado_corrente = 0
        self.estados_de_aceitacao = estados_de_aceitacao
        self.estados_tokens = estados_tokens
        self.nome_token_atual = None
        self.transicoes = transicoes
        self.valido = True

    def __str__(self):
        return "[{},{}]".format(self.token_lido,self.nome_token_atual)
    def get_token(self):
        return Token(self.token_lido,self.nome_token_atual)
    def muda_estado(self, numero):
        self.estado_corrente = numero
        if numero == 0:
            self.token_lido = ""
            self.nome_token_atual = ""
        elif numero in self.estados_tokens:
            self.nome_token_atual = self.estados_tokens[numero]

    # Adicionar char ao automato para mudar seu estado
    def read_new_char(self, char_, proximo_char):
        # verifica se o automato ainda está ativo
        if not self.valido:
            return False 
        self.append_char(char_)
        temp_estado = self.estado_corrente
        estado_de_aceitacao = self.append_char(proximo_char)
        self.token_lido = self.token_lido[:-1]
        
        if estado_de_aceitacao:
            if self.nome_token_atual == "ID" and  self.token_lido in PALAVRAS_RESERVADAS:
                self.nome_token_atual = "PALAVRA_RESERVADA"
            return True
        else:
            self.muda_estado(temp_estado)
 

    def append_char(self, char):
        self.token_lido += char
        transicoes_estado_corrente = self.transicoes[self.estado_corrente]

        for key, value in transicoes_estado_corrente.items():
            matching_character = char in key
            if key[0] == "¬":
                matching_character = char not in key[1:]
            if matching_character: # verifica se há transição válida para o estado atual com char
                self.muda_estado(value) # passa para o novo estado
                if self.estado_corrente in self.estados_de_aceitacao:
                    return True
                else:
                    return False

        print("PROGRAMA INVÁLIDO - O TOKEN NÃO PODE SER RECONHECIDO " + self.token_lido)
        exit()


def get_automato():
    return Automato(
        estados_de_aceitacao=[2],
        transicoes={
            0: {SPACE: 0, LETTER: 1, "+-*": 3, DIGITS:4,"=": 5,"><": 6, "!": 8,OTHER_SPECIAL_CHAR: 9, "/": 10},
            1: {LETTER: 1, (SPACE+CLOSE_CHAR): 2}, #id e palavra reservada
            # 2: FIM (TOKEN ACEITO)
            3: {TUDO: 2}, # operadores algébricos
            4: {DIGITS: 4, ("¬"+DIGITS): 2}, # números
            5: {"¬=": 2,"=": 7}, # atribuicao
            6: {"¬=": 2,"=": 7}, # operadores logicos
            7: {TUDO: 2},
            8: {"=": 7},
            9: {TUDO: 2},
            # comentários e divisão
            10: {"¬*": 2,"*": 11}, # 10 -> 2: divisão
            11: {"¬*": 11, "*": 12},
            12: {"*": 12, "/": 0, "¬*/":11},
        },

        estados_tokens= {
            1: "ID",
            3: "OPERADOR_ALGEBRICO",
            4: "NUMBER",
            5: "ATRIBUICAO",
            6: "OPERADOR_LOGICO", # >= <= == ><
            7:"OPERADOR_LOGICO", # != ==
            9: "CARACTERE_ESPECIAL",
            10: "OPERADOR_ALGEBRICO",
        }
    )