import re

# DEFINIÇÃO DAS CLASSES:
PALAVRAS_RESERVADAS = ["int", "main", "printf", "scanf", "return"]
NUMERAIS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
COMENTARIOS = ["/", "*"]
LITERAIS = ["'", '"']
OPERADORES = ["+", "-", "/", "*", "&&", "||", ">", "<", "=", "!", "%"]
SEPARADORES = [" ", "\n", "(", ")", "{", "}", ";", ","]

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
    # Verifica se é separador (espaço, quebra de linha, etc)
    return char in [" ", "\n", "(", ")", "{", "}", ";", ","]

def eh_aspas(char):
    # Verifica se é início de string
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

    return ("NUMERAL", arquivo[inicio:i], linha, col_inicio, i, coluna)

def ler_operador(arquivo, i, linha, coluna):
    col_inicio = coluna

    # Verifica se é operador de dois caracteres
    if i+1 < len(arquivo):
        dois = arquivo[i:i+2]
        if dois in ["==", "!=", "<=", ">=", "&&", "||", "++", "--"]:
            return ("OPERADOR", dois, linha, col_inicio, i+2, coluna+2)

    # Se não for é operador simples
    return ("OPERADOR", arquivo[i], linha, col_inicio, i+1, coluna+1)

def ler_literal(arquivo, i, linha, coluna):
    # Verifica qual tipo de aspas iniciou o literal
    aspas = arquivo[i]
    col_inicio = coluna

    # Avança para dentro do literal
    i += 1
    coluna += 1
    inicio = i

    # Lê até achar a mesma aspas 
    while i<len(arquivo) and arquivo[i] != aspas:
        if arquivo[i] == "\n":
            linha += 1
            coluna = 1
        else:
            coluna += 1
        i += 1

    conteudo = arquivo[inicio:i]
    i += 1
    coluna += 1

    return ("LITERAL", conteudo, linha, col_inicio, i, coluna)

def ler_comentario(arquivo, i, linha, coluna):
    col_inicio = coluna

    # Comentário de linha
    if arquivo[i:i+2] == "//":
        i += 2
        coluna += 2
        inicio = i

        # Vai até o fim da linha
        while i<len(arquivo) and arquivo[i] != "\n":
            i += 1
            coluna += 1

        return ("COMENTARIO", arquivo[inicio:i], linha, col_inicio, i, coluna)

    # Comentário de bloco
    elif arquivo[i:i+2] == "/*":
        i += 2
        coluna += 2
        inicio = i

        # Procuroa */
        while i+1 < len(arquivo) and arquivo[i:i+2] != "*/":
            if arquivo[i] == "\n":
                linha += 1
                coluna = 1
            else:
                coluna += 1
            i += 1

        # Pula o */
        i += 2
        coluna += 2

        return ("COMENTARIO", arquivo[inicio:i], linha, col_inicio, i, coluna)

    return None

def main():
    with open("codigo_entrada.c", "r") as file:
        arquivo = file.read()

    linha = 1
    coluna = 1
    i = 0
    tokens = []

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
            tokens.append(token[:4])
            i = token[4]
            coluna = token[5]

        elif eh_aspas(char):
            token = ler_literal(arquivo, i, linha, coluna)
            tokens.append(token[:4])
            i = token[4]
            linha = token[2]
            coluna = token[5]

        elif char == "/":
            resultado = ler_comentario(arquivo, i, linha, coluna)

            if resultado:
                tokens.append(resultado[:4])
                i = resultado[4]
                linha = resultado[2]
                coluna = resultado[5]
                continue

        elif eh_operador(char):
            token = ler_operador(arquivo, i, linha, coluna)
            tokens.append(token[:4])
            i = token[4]
            coluna = token[5]

        elif eh_separador(char):
            i += 1
            coluna += 1

        # Erro léxico
        else:
            print(f"Erro: caractere inválido {char}")
            i += 1

    print(tokens)

    with open("tokens.txt", "w") as f:
        for classe, valor, linha, coluna in tokens:
            f.write(f"{classe:15} {valor:10} (linha {linha}, coluna {coluna})\n")


main()