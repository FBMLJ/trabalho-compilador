def isLetter(c):
    return c in "abcdefghijklmnopqrstuvxwyzABCDEFGHIJKLMNOPQRSTUVXWYZ"
def isNumber(c):
    return c in '0123456789'


class Atomato:
    def __init__(self,  estados_de_aceitacao,transicao,break_words = ' ()[];\{\}\n+-=<>*/!', nome_token=""):
        self.token_lido = ''
        self.estado_corrente = 0
        self.transicao = transicao
        self.break_words = break_words
        self.estados_de_aceitacao = estados_de_aceitacao
        self.valido = True
        self.nome_token = nome_token

    def __str__(self):
        return '["{}",{}]'.format(self.token_lido, self.nome_token)
    # Adicionar caracter ao automato para mudar seu estado
    def learn_new_char(self,c,c_prox, eof):
        #verifica se o automato ainda está ativo
        if not self.valido:
            return False 
        
        self.token_lido += c

        #pegando estado atual
        estado = self.transicao[self.estado_corrente]
        controle = True
        for key, value in estado.items():

            #string padronizadas para qualquer letras<LETTER> ou/e qualquer numero<NUMBER> 
            if (key == "<LETTER>" and isLetter(c))  or  (key == "<NUMBER>"  and isNumber(c)):
                controle = False
                self.estado_corrente = value
                break
            #ler um caracter especifico 
            elif (c in key):
                controle = False
                self.estado_corrente = value
                break
            
        #atomato invalido retornando falso
        if controle:
            self.valido = False
            return False

        #verifica a proxima letra
        elif self.estado_corrente in self.estados_de_aceitacao:

            #se break_word for uma lista vazia aceita qualquer caracter com fim
            if eof:
                return True
            if self.break_words == '':
                return True
            
            elif c_prox in self.break_words:
               return True

            else:
                return False

        #atomato valido mas não no estado de aceitação
        else:
            return False
        
