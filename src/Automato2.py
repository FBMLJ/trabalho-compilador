
from string import ascii_letters

from pyparsing import NoMatch
from .utils.helpers import is_number, is_letter

SPECIAL_CHARS = ' ()[];\{\}\n+-=<>*/!'
LETTER = ascii_letters
NUMBER = '1234567890'
SPACE = ' \n\t'

class Automato:
    def __init__(self, estados_de_aceitacao, transicoes, estados_tokens ):
        self.token_lido = ''
        self.estado_corrente = 0
        self.estados_de_aceitacao = estados_de_aceitacao
        self.estados_tokens = estados_tokens
        self.nome_token_atual = None
        self.transicoes = transicoes
        self.valido = True

    def __str__(self):
        print('---')
        return self.nome_token_atual

    def muda_estado(self, numero):
        self.estado_corrente = numero
        if numero in self.estados_tokens:
            self.nome_token_atual = self.estados_tokens[numero]

    # Adicionar char ao automato para mudar seu estado
    def read_new_char(self, char_, proximo_char):
        # verifica se o automato ainda está ativo
        if not self.valido:
            return False 
        self.append_char(char_)
        temp_estado = self.estado_corrente
        ehValido = self.append_char(proximo_char)
        self.token_lido = self.token_lido[:-1]
        if ehValido:
            return False
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
        print("programa invalido token não reconhecivel " + self.token_lido)
        exit()





def get_automato():
    return Automato(
    estados_de_aceitacao=[2],
    transicoes={
        0: {LETTER: 1},
        1: {LETTER: 1, (SPACE+SPECIAL_CHARS): 2}
    },
    estados_tokens= {
        1: "ID"
    }
    )