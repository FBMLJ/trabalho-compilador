
from src.lexico.Scan import Scan

if __name__ == "__main__":
    scan = Scan("input.txt")
    tokens = scan.get_tokens()
    print(str(tokens[0]))