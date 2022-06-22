
from src.lexico.Scan import Scan
from src.sintatico.sintatico_com_pilha import getAnalisadorSintatico
if __name__ == "__main__":
    scan = Scan("input.txt")
    tokens = scan.get_tokens()
    getAnalisadorSintatico(tokens)