from enum import auto
from .Automato import *

class Scan:
    def __init__(self, nome_arquivo):
        self.nome_arquivo  = nome_arquivo
        self.iterador = 0
        self.restart_automato_list()
        
    def restart_automato_list(self):
        self.automato_list = [
            get_afd_reserved_words(),
            get_afd_id(),
            get_afd_number(),
            get_afd_algebric_op(),
            get_afd_special_char(),
            get_afd_relop(),
            get_afd_assignment(),
            # get_afd_comments(),
        ]
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
        print()
        
        while self.next_char_sem_acrescimo() != "" and not parada: # parada está sendo utilizado?
            while self.next_char_sem_acrescimo() in " \n":
                self.iterador += 1
                self.restart_automato_list()
            _char = self.next_char()
            
            for automato in self.automato_list:

                final_token = automato.read_new_char(_char, self.next_char_sem_acrescimo(), False)
                if final_token:
                    tokens.append(str(automato))
                    print(automato, end=" ")
                    self.restart_automato_list()
                    
                    break
        
        print()
        