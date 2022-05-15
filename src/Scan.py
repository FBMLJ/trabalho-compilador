class Scan:
    def __init__(self, nome_arquivo):
        self.nome_arquivo  = nome_arquivo
        self.iterador = 0
        
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
        current_token = ""
        tokens = []
        parada = False
        
        while self.next_char_sem_acrescimo() != "" and not parada:
            _char = self.next_char()
            tokens.append(current_token)
            current_token = ''
            current_token += _char

        print(tokens)