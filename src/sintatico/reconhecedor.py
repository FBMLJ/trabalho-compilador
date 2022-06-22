class Reconhecedor:
    def __init__(self, lista_reconhecedor, eh_folha=False, message_de_erro = "Houve um erro"):
        self.lista_reconhecedor = lista_reconhecedor
        self.eh_folha = eh_folha
        self.message_de_erro = message_de_erro

    def erro(self):
        print(self.message_de_erro)
        raise Exception(self.message_de_erro)

    def reconhecer(self, lista_token):
        if  self.eh_folha:
            pass
        else:
            foi_reconhecido = False
            for opcao_reconhecedor in self.lista_reconhecedor:
                eh_valido = True 
                self.filhos = []
                lista_token_ = lista_token.copy()
                for rec in opcao_reconhecedor:
                    try:
                        lista_token_ = rec.reconhecer(lista_token_)
                        
                        
                    except:
                        eh_valido = False
                        break
                        
                if eh_valido:
                    foi_reconhecido = True
                    break
            
            if not foi_reconhecido:
                self.erro()
    