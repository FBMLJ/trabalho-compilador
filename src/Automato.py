from lib2to3.pgen2 import token
from .utils.helpers import is_number, is_letter

DEFAULT_BREAK_WORDS = ' ()[];\{\}\n+-=<>*/!'

class Automato:
    def __init__(self, estados_de_aceitacao, transicoes, break_words=DEFAULT_BREAK_WORDS, nome_token=''):
        self.token_lido = ''
        self.break_words = break_words
        self.estado_corrente = 0
        self.estados_de_aceitacao = estados_de_aceitacao
        self.nome_token = nome_token
        self.transicoes = transicoes
        self.valido = True

    def __str__(self):
        return '["{}",{}]'.format(self.token_lido, self.nome_token)
    # Adicionar char ao automato para mudar seu estado
    def read_new_char(self, char_, proximo_char, eof):
        # verifica se o automato ainda está ativo
        if not self.valido:
            return False 
        
        self.token_lido += char_
        existe_transicao_valida = self.search_valid_transition(char_) # não passar token_lido ?
            
        if not existe_transicao_valida:
            self.valido = False
            return False
        elif self.estado_corrente in self.estados_de_aceitacao: # transição é feita e estado é de aceitação
            if (eof or (not self.break_words) or (proximo_char in self.break_words)): # se break_word for uma lista vazia aceita qualquer char como fim
                return True
            else:
                return False
        else: # automato valido mas não no se encontra em estado de aceitação
            return False

    def valid_wildcard_input(self, char, key):
        #  string padronizadas para qualquer letras<LETTER> ou/e qualquer numero<NUMBER>
        return (key == "<LETTER>" and is_letter(char)) or (key == "<NUMBER>" and is_number(char))

    def search_valid_transition(self, char):
        
        transicoes_estado_corrente = self.transicoes[self.estado_corrente]
        for key, value in transicoes_estado_corrente.items():
            if (char in key) or self.valid_wildcard_input(char, key): # verifica se há transição válida para o estado atual com char
                self.estado_corrente = value # passa para o novo estado
                return True

        return False




def get_afd_reserved_words():
    return Automato(estados_de_aceitacao=[21],
    transicoes= {
        0: {"v": 5, "i": 1, "e": 3,"w": 2, "r": 4},
        1: {"f": 21,"n": 6},
        2: {"h": 8},
        3: {"l": 9},
        4: {"e": 10}, 
        5: {"o": 11},
        6: {"t": 21},
        8: {"i": 13},
        9: {"s": 14},
        10: {"t" : 15},
        11: {"i": 16},
        13: {"l": 17},
        14: {'e': 21},
        15: {"u": 19},
        16: {"d": 21},
        17: {"e": 21},
        19: {"r": 22},
        22: {"n": 21}
    }, nome_token="PALAVRA RESERVADA")

def get_afd_id():
    return Automato(estados_de_aceitacao=[1], transicoes={0:{"<LETTER>": 1}, 1: {"<LETTER>": 1}}, nome_token="ID")

def get_afd_number():
    return Automato(estados_de_aceitacao=[1], transicoes={0:{"<NUMBER>": 1}, 1: {"<NUMBER>": 1}}, nome_token="NUMERO")



# Exemplo
# a = Automato([2,3], [{"<LETTER>": 1}, {"<LETTER>": 2}, {"<LETTER>": 3}, {}])
# a.read_new_char("a", "b", False)
# a.read_new_char("b", "c", False)
# a.read_new_char("c", "", False)
# print(a.__dict__)

