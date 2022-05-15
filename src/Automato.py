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
    def read_new_char(self, char, proximo_char, eof):
        # verifica se o automato ainda está ativo
        if not self.valido:
            return False 
        
        self.token_lido += char
        existe_transicao_valida = self.search_valid_transition(char) # não passar token_lido ?
            
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


a = Automato([2,3], [{"<LETTER>": 1}, {"<LETTER>": 2}, {"<LETTER>": 3}, {}])
a.read_new_char("a", "b", False)
a.read_new_char("b", "c", False)
a.read_new_char("c", "", False)
print(a.__dict__)

