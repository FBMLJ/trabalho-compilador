from enum import auto
from .Automato2 import get_automato
class Scan:
    def __init__(self, nome_arquivo):
        self.nome_arquivo  = nome_arquivo
        self.iterador = 0
        self.restart_automato()
        
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
        
        
        while self.next_char_sem_acrescimo() != "" and not parada:
            
            _char = self.next_char()
            
            automato = self.automato
            next_char = self.next_char_sem_acrescimo()
            if next_char == '':
                next_char = ' '

            control = automato.read_new_char(_char, next_char)
            
            if control:
                tokens.append(str(automato))
                print(automato, end=" ")
                self.restart_automato()
                
                break
        
            # current_token = ''
            # current_token += _char
        print(tokens)
        