import re

PALAVRAS_RESERVADAS = ["int", "main", "printf", "scanf", "return"]
NUMERAIS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
COMENTARIOS = ["/", "*"]
LITERAIS = ["'", '"']
OPERADORES = ["+", "-", "/", "*", "&&", "||", ">", "<", "=", "!", "%"]
SEPARADORES = [" ", "   ", "\n", "(", ")", "{", "}"]

def main():
    with open("codigo_entrada.c", "r") as file:
        arquivo = file.read()

    pivo = 0
    batedor = 0
    classes_atuais = []
    token_atual = ""
    tokens = []
    cont = 0
    linha = 0
    coluna = 0

    while batedor < len(arquivo):
        if(classes_atuais != None):
            if "PALAVRAS_RESERVADAS" in classes_atuais or "IDENTIFICADORES" in classes_atuais:
                if arquivo[batedor] in SEPARADORES or arquivo[batedor] in OPERADORES:
                    tokens.append(token_atual)
                    token_atual = ""
                    cont = 0
                    classes_atuais = []
                    pivo = batedor
                else: 
                    batedor += 1

            if "NUMERAIS" in classes_atuais:
                if arquivo[batedor] in SEPARADORES or arquivo[batedor] in OPERADORES:
                    tokens.append(token_atual)
                    token_atual = ""
                    cont = 0
                    classes_atuais = []
                    pivo = batedor
                else: 
                    batedor += 1

            if "LITERAIS" in classes_atuais:
                if re.match(r"[\"']", arquivo[batedor]):
                    tokens.append(token_atual)
                    token_atual = ""
                    cont = 0
                    classes_atuais = []
                    pivo = batedor
                else: 
                    batedor += 1
            
            if "COMENTARIOS" in classes_atuais:
                if arquivo[batedor] in COMENTARIOS:
                    tokens.append(token_atual)
                    token_atual = ""
                    cont = 0
                    classes_atuais = []
                    pivo = batedor
                else: 
                    batedor += 1

            if "OPERADORES" in classes_atuais:
                if arquivo[batedor] == "+" and arquivo[batedor+1] == "+":
                    token_atual += (arquivo[batedor+1])
                    cont +=1
                    tokens.append(token_atual)
                    token_atual = ""
                    cont = 0
                    classes_atuais = []
                    pivo = batedor
                elif arquivo[batedor] == "-" and arquivo[batedor+1] == "-":
                    token_atual += arquivo[batedor+1]
                    cont +=1
                    tokens.append(token_atual)
                    token_atual = ""
                    cont = 0
                    classes_atuais = []
                    pivo = batedor
                elif arquivo[batedor] == "<" and arquivo[batedor+1] == "=":
                    token_atual += arquivo[batedor+1]
                    cont +=1
                    tokens.append(token_atual)
                    token_atual = ""
                    cont = 0
                    classes_atuais = []
                    pivo = batedor
                elif arquivo[batedor] == ">" and arquivo[batedor+1] == "=":
                    token_atual += arquivo[batedor+1]
                    cont +=1
                    tokens.append(token_atual)
                    token_atual = ""
                    cont = 0
                    classes_atuais = []
                    pivo = batedor
                elif arquivo[batedor] == "=" and arquivo[batedor+1] == "=":
                    token_atual += arquivo[batedor+1]
                    cont +=1
                    tokens.append(token_atual)
                    token_atual = ""
                    cont = 0
                    classes_atuais = []
                    pivo = batedor
                elif arquivo[batedor] == "!" and arquivo[batedor+1] == "=":
                    token_atual += arquivo[batedor+1]
                    cont +=1
                    tokens.append(token_atual)
                    token_atual = ""
                    cont = 0
                    classes_atuais = []
                    pivo = batedor
                elif arquivo[batedor] == "&" and arquivo[batedor+1] == "&":
                    token_atual += arquivo[batedor+1]
                    cont +=1
                    tokens.append(token_atual)
                    token_atual = ""
                    cont = 0
                    classes_atuais = []
                    pivo = batedor
                elif arquivo[batedor] == "|" and arquivo[batedor+1] == "|":
                    token_atual += arquivo[batedor+1]
                    cont +=1
                    tokens.append(token_atual)
                    token_atual = ""
                    cont = 0
                    classes_atuais = []
                    pivo = batedor
        
        if re.match(r"[A-Za-z_]", arquivo[batedor]):
            classes_atuais.append("PALAVRAS_RESERVADAS")
            classes_atuais.append("IDENTIFICADORES")
            cont += 1 
            token_atual += arquivo[batedor]
        elif arquivo[batedor] in NUMERAIS:
            classes_atuais.append("NUMERAIS")
            cont += 1 
            token_atual += arquivo[batedor]
        elif arquivo[batedor] in LITERAIS:
            classes_atuais.append("LITERAIS")
            cont += 1 
            token_atual += arquivo[batedor]
        elif arquivo[batedor] in COMENTARIOS:
            classes_atuais.append("COMENTARIOS")
            cont += 1 
            token_atual += arquivo[batedor]
        elif arquivo[batedor] in COMENTARIOS and arquivo[batedor] in OPERADORES:
            classes_atuais.append("COMENTARIOS")
            classes_atuais.append("OPERADORES")
            cont += 1 
            token_atual += arquivo[batedor]
        elif arquivo[batedor] in OPERADORES:
            classes_atuais.append("OPERADORES")
            cont += 1 
            token_atual += arquivo[batedor]
        elif arquivo[batedor] == "\n":
            linha += 1 
            coluna = 0
        else: 
            print(f"Erro: caractere inválido na linha {linha} e coluna {coluna}")
            coluna += 1
          
main()
