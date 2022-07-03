f = open("arq", "r")
for i in f.read().split("\n"):
    if len(" ") < 1:
        break
    # print(i)

    valor = i.split(" ")[1].replace("’", "_linha").replace('-',"_")
    print('{} = Producao("{}")'.format(valor, valor.upper()))
    # print(valor)