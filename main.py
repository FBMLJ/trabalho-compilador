
from src.lexico.Scan import Scan
from src.sintatico.sintatico_com_pilha import get_analisador_sintatico
if __name__ == "__main__":
    scan = Scan("input.txt")
    tokens = scan.get_tokens()
    # print([t.__dict__ for t in tokens])
    get_analisador_sintatico(tokens, scan.identificadores)