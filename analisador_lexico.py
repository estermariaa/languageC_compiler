import re

# DEFINIÇÃO DAS CLASSES:
PALAVRAS_RESERVADAS = ["int", "float", "char", "double", "main", "printf", "scanf", "return", "include", "for", "while", "if", "else"]
SEPARADORES = [" ", "\n", "(", ")", "{", "}", ";", ",", "[", "]"]

# FUNÇÕES AUXILIARES
def eh_letra(char):
    # Verifica se o caractere é letra ou underscore (_)
    return re.match(r"[A-Za-z_]", char)

def eh_digito(char):
    # Verifica se é número
    return char.isdigit()

def eh_operador(char):
    # Verifica se é um operador SIMPLES
    return char in ["+", "-", "/", "*", ">", "<", "=", "!", "%", "&", "|"]

def eh_separador(char):
    return char in SEPARADORES

def eh_aspas(char):
    # Verifica se é início de literal
    return char in ("'", '"')

# FUNÇÕES DE LEITURA DE TOKENS
def ler_identificador(arquivo, i, linha, coluna):
    inicio = i
    col_inicio = coluna

    # Lê enquanto for número, letra ou underscore (identificador válido)
    while i<len(arquivo) and re.match(r"[A-Za-z0-9_]", arquivo[i]):
        i += 1
        coluna += 1

    texto = arquivo[inicio:i]

    if texto in PALAVRAS_RESERVADAS:
        return ("RESERVADA", texto, linha, col_inicio, i, coluna)
    else:
        return ("IDENTIFICADOR", texto, linha, col_inicio, i, coluna)

def ler_numero(arquivo, i, linha, coluna):
    inicio = i
    col_inicio = coluna

    # Enquanto for dígito continua lendo
    while i<len(arquivo) and arquivo[i].isdigit():
        i += 1
        coluna += 1

    # Parte decimal
    if i < len(arquivo) and arquivo[i] == ".":
        i += 1
        coluna += 1

        # Deve ter pelo menos um dígito depois do ponto
        if i < len(arquivo) and arquivo[i].isdigit():
            while i < len(arquivo) and arquivo[i].isdigit():
                i += 1
                coluna += 1
        else:
            valor = arquivo[inicio:i]
            return ("ERRO", valor, linha, col_inicio, i, coluna)
    
    # Número seguido de letra
    if i < len(arquivo) and re.match(r"[A-Za-z_]", arquivo[i]):
        while i < len(arquivo) and re.match(r"[A-Za-z0-9_]", arquivo[i]):
            i += 1
            coluna += 1

        valor = arquivo[inicio: i]

        return ("ERRO", valor, linha, col_inicio, i, coluna)

    return ("NUMERAL", arquivo[inicio:i], linha, col_inicio, i, coluna)

def ler_operador(arquivo, i, linha, coluna):
    col_inicio = coluna

    # Verifica se é operador de dois caracteres
    if i+1 < len(arquivo):
        dois = arquivo[i:i+2]

        # Erro léxico:
        if dois in ["=+", "=-", "=/", "=*", "=>", "=<", "=!"]:
            return ("ERRO", dois, linha, col_inicio, i+2, coluna+2)

        if dois in ["==", "!=", "<=", ">=", "&&", "||", "++", "--", "+=", "-=", "*=", "/=", "%="]:
            return ("OPERADOR", dois, linha, col_inicio, i+2, coluna+2)

    if arquivo[i] in ["&", "|"]:
        return ("ERRO", arquivo[i], linha, col_inicio, i+1, coluna+1)
    
    # Se não for é operador simples
    return ("OPERADOR", arquivo[i], linha, col_inicio, i+1, coluna+1)

def ler_literal(arquivo, i, linha, coluna):
    aspas = arquivo[i]
    col_inicio = coluna

    i += 1
    coluna += 1
    inicio = i

    while i < len(arquivo):
        if arquivo[i] == aspas:
            conteudo = arquivo[inicio:i]
            i += 1
            coluna += 1
            return ("LITERAL", conteudo, linha, col_inicio, i, coluna)

        if arquivo[i] == "\n":
            linha += 1
            coluna = 1
        else:
            coluna += 1

        i += 1

    # string não fechada
    return ("ERRO", "string não fechada", linha, col_inicio, i, coluna)

def ler_comentario(arquivo, i, linha, coluna):
    col_inicio = coluna

    # Comentário de linha
    if i + 1 < len(arquivo) and arquivo[i:i+2] == "//":
        i += 2
        coluna += 2
        inicio = i

        while i < len(arquivo) and arquivo[i] != "\n":
            i += 1
            coluna += 1

        return ("COMENTARIO", arquivo[inicio:i], linha, col_inicio, i, coluna)

    # Comentário de bloco
    elif i + 1 < len(arquivo) and arquivo[i:i+2] == "/*":
        i += 2
        coluna += 2
        inicio = i

        while i+1 < len(arquivo):
            if arquivo[i:i+2] == "*/":
                conteudo = arquivo[inicio:i]
                i += 2
                coluna += 2
                return ("COMENTARIO", conteudo, linha, col_inicio, i, coluna)

            if arquivo[i] == "\n":
                linha += 1
                coluna = 1
            else:
                coluna += 1

            i += 1

        # comentário não fechado
        return ("ERRO", "comentário não fechado", linha, col_inicio, i, coluna)

    return None



def main():
    with open("teste_sintatico_semantico.c", "r") as file:
        arquivo = file.read()

    linha = 1
    coluna = 1
    i = 0
    tokens = []
    erros = []

    while i < len(arquivo):
        char = arquivo[i]   

        # Trata nova linha
        if char == "\n":
            linha += 1
            coluna = 1
            i += 1
            continue

        if eh_letra(char):
            token = ler_identificador(arquivo, i, linha, coluna)
            tokens.append(token[:4])
            i = token[4]
            coluna = token[5]

        elif eh_digito(char):
            token = ler_numero(arquivo, i, linha, coluna)

            if token[0] == "ERRO":
                erros.append(token[:4])
            else:
                tokens.append(token[:4])

            i = token[4]
            coluna = token[5]

        elif eh_aspas(char):
            token = ler_literal(arquivo, i, linha, coluna)

            if token[0] == "ERRO":
                erros.append(token[:4])
            else:
                tokens.append(token[:4])

            i = token[4]
            linha = token[2]
            coluna = token[5]

        elif char == "/":
            resultado = ler_comentario(arquivo, i, linha, coluna)

            if resultado:
                if resultado[0] == "ERRO":
                    erros.append(resultado[:4])
                else:
                    tokens.append(resultado[:4])

                i = resultado[4]
                linha = resultado[2]
                coluna = resultado[5]
                continue

        elif eh_operador(char):
            token = ler_operador(arquivo, i, linha, coluna)
            if token[0] == "ERRO":
                erros.append(token[:4])  
            else:
                tokens.append(token[:4])

            i = token[4]
            coluna = token[5]

        elif eh_separador(char):
            if char != " ":
                tokens.append(("SEPARADOR", char, linha, coluna))
            i += 1
            coluna += 1

        # Erro léxico
        else:
            erros.append(("ERRO", char, linha, coluna)) 
            i += 1

    print("\n")
    print(tokens)

    with open("lista_de_tokens_2.txt", "w") as f:
        for classe, valor, linha, coluna in tokens:
            f.write(f"{classe:15} {valor:15} (linha {linha}, coluna {coluna})\n")

    with open("erros_lexicos_2.txt", "w") as f:
        for classe, valor, linha, coluna in erros:
            f.write(f"{classe:10} {valor:10} (linha {linha}, coluna {coluna})\n")

main()