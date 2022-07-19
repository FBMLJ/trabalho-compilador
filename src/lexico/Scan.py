from lib2to3.pgen2 import token
from .Automato import get_automato
class Scan:
    def __init__(self, nome_arquivo):
        self.nome_arquivo  = nome_arquivo
        self.iterador = 0
        self.restart_automato()
        self.identificadores = []
        
    #cria os atomatos do scanner alem de reinicializa-los quando necessario
    def restart_automato(self):
        self.automato = get_automato()


    def next_char_sem_acrescimo(self):
        with open(self.nome_arquivo,'r',encoding = 'utf-8') as f:
            try:
                valor =  f.read()[self.iterador]
            except(IndexError):
                return ""
            return valor

    def next_char(self):
        with open(self.nome_arquivo,'r',encoding = 'utf-8') as f:
            valor =  f.read()[self.iterador]
            self.iterador +=1
            return valor

    def get_tokens(self):
        tokens = []
        parada = False
        linha_atual = 1
        
        while self.next_char_sem_acrescimo() != "" and not parada:
            _char = self.next_char()
            if _char == '\n':
                linha_atual += 1
            automato = self.automato
            next_char = self.next_char_sem_acrescimo()
            if next_char == '':
                next_char = ' '

            token_aceito = automato.read_new_char(_char, next_char)
            
            if token_aceito:
                token = automato.get_token() 

                if tokens:
                    # caso exista um token prévio de tipo, adicionamos var a lista de identificadores
                    if token.token_nome == "ID" and tokens[-1].token_lido in ["int", "void"] and token.token_lido not in self.identificadores:
                        self.identificadores.append(token.token_lido)

                tokens.append(token)
                tokens[-1].linha = linha_atual
                
                
                self.restart_automato()
        return tokens