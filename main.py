
from src.lexico.Scan import Scan
from src.sintatico.sintatico_com_pilha import get_analisador_sintatico
if __name__ == "__main__":
    scan = Scan("input.txt")
    tokens = scan.get_tokens() # LÉXICO

    for token in tokens:
        print(token, end=',')
        
    print("\n\n")

    get_analisador_sintatico(tokens, scan.identificadores) # SINTÁTICO