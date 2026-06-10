import re

EPSILON = "&"

gramatica = {
    "Programa": [["int", "main", "(", ")", "Bloco", "EOF"]],
    "Bloco": [["{", "ListaComandos", "}"]],
    "ListaComandos": [["Comando", "ListaComandos"], [EPSILON]],

    "Comando": [["Declaracao"], ["Atribuicao"], ["Condicao"], ["ChamadaIO"], ["Retorno"]],
    
    "Declaracao": [["int", "IDENTIFICADOR", "RestoDeclaracao"]],
    "RestoDeclaracao": [[";"], ["=", "Expressao", ";"]],
    
    "Atribuicao": [["IDENTIFICADOR", "=", "Expressao", ";"]],
    "Condicao": [["if", "(", "Expressao", ")", "Bloco"]],
    "ChamadaIO": [["printf", "(", "LITERAL", ")", ";"]],
    "Retorno": [["return", "NUMERAL", ";"]],
    
    "Expressao": [["Termo", "ExpressaoLinha"]],
    "ExpressaoLinha": [["+", "Termo", "ExpressaoLinha"], ["-", "Termo", "ExpressaoLinha"], [EPSILON]],
    "Termo": [["Fator", "TermoLinha"]],
    "TermoLinha": [["*", "Fator", "TermoLinha"], ["/", "Fator", "TermoLinha"], [EPSILON]],
    "Fator": [["IDENTIFICADOR"], ["NUMERAL"], ["(", "Expressao", ")"]]
}

terminais = {
    "IDENTIFICADOR", "NUMERAL", "LITERAL", "=", ";", "if", "(", ")", "{", "}", 
    "+", "-", "*", "/", "EOF", EPSILON, "int", "main", "printf", "return", "=="
}

def calcular_first():
    """Calcula o first da gramática"""

    # Não terminais começam vazios
    first = {nao_terminal: set() for nao_terminal in gramatica}
    
    mudou = True
    # O loop continua rodando enquanto novos itens forem descobertos
    while mudou:
        mudou = False
        
        # Pega uma regra por vez
        for nao_terminal, derivacoes in gramatica.items():
            # pega uma opção dessa regra
            for derivacao in derivacoes:
                for simbolo in derivacao: 
                    # Se o símbolo for um terminal, o FIRST dele é ele mesmo (A -> a...)
                    if simbolo in terminais:
                        simbolo_first = {simbolo}
                    else:
                        # Se for uma regra, pega o FIRST que já calculamos para ela (A -> B...)
                        simbolo_first = first[simbolo]
                    
                    tamanho_antes = len(first[nao_terminal])
                    
                    # Adiciona os tokens encontrados (ignorando o epsilon por enquanto)
                    first[nao_terminal].update(simbolo_first - {EPSILON})
                    
                    # Se o conjunto cresceu, marca que houve mudança para rodar de novo
                    if len(first[nao_terminal]) > tamanho_antes:
                        mudou = True
                    
                    # Se o símbolo atual NÃO pode virar vazio, para de olhar os próximos símbolos da regra.
                    if EPSILON not in simbolo_first:
                        break
                else:
                    # Se o 'for' terminou sem dar 'break', significa que TODOS 
                    # os símbolos dessa regra podem sumir (virar epsilon).
                    # Então, o próprio Não-Terminal também pode ser epsilon
                    if EPSILON not in first[nao_terminal]:
                        first[nao_terminal].add(EPSILON)
                        mudou = True
                        
    return first

def first_de_sequencia(sequencia, conjuntos_first):
    """Calcula o FIRST de uma lista de símbolos"""
    resultado = set()
    
    # Se a sequência for vazia, o FIRST é epsilon
    if not sequencia:
        return {EPSILON}
        
    for simbolo in sequencia:
        if simbolo in terminais:
            resultado.add(simbolo)
            break # Achou um terminal, para por aqui
        else:
            simbolo_first = conjuntos_first[simbolo]
            resultado.update(simbolo_first - {EPSILON})
            
            # Se a regra atual não pode virar vazio, para
            if EPSILON not in simbolo_first:
                break
    else:
        # Se o loop terminou e todo mundo podia virar epsilon
        resultado.add(EPSILON)
        
    return resultado

def calcular_follow(conjuntos_first):
    follow = {nao_terminal: set() for nao_terminal in gramatica}
    
    # O símbolo inicial recebe EOF
    follow["Programa"].add("EOF")
    
    mudou = True
    while mudou:
        mudou = False
        
        for nao_terminal, derivacoes in gramatica.items():
            for derivacao in derivacoes:
                for i, simbolo in enumerate(derivacao):
                    # Só calcula FOLLOW para Não-Terminais 
                    if simbolo in gramatica:
                        tamanho_antes = len(follow[simbolo])
                        
                        # Pega tudo que vem depois do símbolo atual
                        resto_da_regra = derivacao[i+1:]
                        first_do_resto = first_de_sequencia(resto_da_regra, conjuntos_first)
                        
                        # Adiciona o FIRST do "resto" no FOLLOW do símbolo atual 
                        follow[simbolo].update(first_do_resto - {EPSILON})
                        
                        # Se não sobrou nada na regra, ou se o resto
                        # pode sumir, o FOLLOW do pai desce pro filho
                        if EPSILON in first_do_resto or len(resto_da_regra) == 0:
                            follow[simbolo].update(follow[nao_terminal])
                            
                        if len(follow[simbolo]) > tamanho_antes:
                            mudou = True
                            
    return follow

def construir_tabela(conjuntos_first, conjuntos_follow):
    tabela = {nt: {} for nt in gramatica}
    
    for nao_terminal, derivacoes in gramatica.items():
        for derivacao in derivacoes:
            # Qual é o FIRST?
            first_da_derivacao = first_de_sequencia(derivacao, conjuntos_first)
            
            # Preenche as colunas do FIRST
            for terminal in first_da_derivacao - {EPSILON}:
                # Verificação de segurança: Se já tiver algo na célula, a gramática não é LL(1) pura
                if terminal in tabela[nao_terminal]:
                    print(f"Conflito na tabela! Célula [{nao_terminal}][{terminal}] já está ocupada.")
                
                tabela[nao_terminal][terminal] = derivacao
                
            # Trata o vazio usando o FOLLOW
            if EPSILON in first_da_derivacao:
                for terminal_follow in conjuntos_follow[nao_terminal]:
                    # Evita sobrescrever se já existir uma regra válida
                    if terminal_follow not in tabela[nao_terminal]:
                        tabela[nao_terminal][terminal_follow] = derivacao

    return tabela

def imprimir_tabela(tabela):
    print("\n=== TABELA DE PARSING LL(1) ===")
    for nao_terminal, transicoes in tabela.items():
        print(f"\n[{nao_terminal}]")
        for terminal, derivacao in transicoes.items():
            regra_texto = " ".join(derivacao) if derivacao != [EPSILON] else "EPSILON (Vazio)"
            print(f"  se encontrar '{terminal}' -> usar regra: {regra_texto}")

def parser(tokens_lexico, tabela_ll1, terminais):
    # Preparar a fita de entrada 
    # O léxico gera tuplas: ("IDENTIFICADOR", "a", 1, 1)
    fita_entrada = []
    for token in tokens_lexico:
        classe = token[0]
        valor = token[1]
        linha = token[2]
        coluna = token[3]

        if classe in ["IDENTIFICADOR", "NUMERAL", "LITERAL"]:
            simbolo_gramatica = classe
        else:
            simbolo_gramatica = valor
            
        fita_entrada.append({
            "simbolo": simbolo_gramatica,
            "lexema": valor, # A palavra exata que o usuário digitou
            "linha": linha,
            "coluna": coluna
        })
            
    # Adiciona o EOF pegando a linha/coluna da última palavra (para não dar erro de índice)
    ultima_linha = fita_entrada[-1]["linha"] if fita_entrada else 1
    ultima_coluna = fita_entrada[-1]["coluna"] if fita_entrada else 1
    fita_entrada.append({"simbolo": "EOF", "lexema": "EOF", "linha": ultima_linha, "coluna": ultima_coluna}) 
    
    # A pilha começa com EOF na base e "Programa" no topo.
    pilha = ["EOF", "Programa"] 
    ponteiro = 0 
    
    print("\n=== INICIANDO ANÁLISE SINTÁTICA ===")
    
    while len(pilha) > 0:
        # Enquanto a pilha não estiver vazia
        if ponteiro >= len(fita_entrada):
            break

        topo = pilha[-1]
        
        info_token = fita_entrada[ponteiro]
        token_atual = info_token["simbolo"]
        palavra_real = info_token["lexema"]
        linha_atual = info_token["linha"]
        coluna_atual = info_token["coluna"]
        
        if topo == "EOF" and token_atual == "EOF":
            print("A sintaxe do código está perfeita!")
            pilha.pop()
            break
            
        elif topo == token_atual:
            pilha.pop()     # Remove do topo
            ponteiro += 1   # Avança para o próximo token do código
            
        elif topo in terminais:
            print(f"ERRO SINTÁTICO [Linha {linha_atual}, Coluna {coluna_atual}]: Esperava '{topo}', mas encontrou '{palavra_real}'.")
            break
            
        # é não terminal/regra
        elif topo in tabela_ll1:
            if token_atual in tabela_ll1[topo]:
                derivacao = tabela_ll1[topo][token_atual]
                
                pilha.pop() # Remove a regra antiga
                
                if derivacao != [EPSILON]:
                    for simbolo in reversed(derivacao):
                        pilha.append(simbolo)
                        
            else:
                print(f"ERRO SINTÁTICO [Linha {linha_atual}, Coluna {coluna_atual}]: A regra '{topo}' não esperava a palavra '{palavra_real}'.")
                break
        
        else:
            print(f"ERRO INTERNO [Linha {linha_atual}]: Símbolo '{topo}' desconhecido na gramática.")
            break

def carregar_tokens_do_arquivo(nome_arquivo):
    tokens_lidos = []
    padrao = re.compile(r"^([A-Z_]+)\s+(.*?)\s+\(linha (\d+),\s*coluna (\d+)\)$")

    with open(nome_arquivo, "r", encoding="utf-8") as f:
        for texto_linha in f:
            texto_linha = texto_linha.strip()
            if not texto_linha: continue
            
            match = padrao.match(texto_linha)
            if match:
                classe, valor = match.group(1), match.group(2).strip()
                if classe == "COMENTARIO": continue
                tokens_lidos.append((classe, valor, int(match.group(3)), int(match.group(4))))
                
    return tokens_lidos

if __name__ == "__main__":
    conjuntos_first = calcular_first()
    conjuntos_follow = calcular_follow(conjuntos_first)
    tabela_ll1 = construir_tabela(conjuntos_first, conjuntos_follow)
    
    tokens_reais = carregar_tokens_do_arquivo("lista_de_tokens_2.txt") 
    parser(tokens_reais, tabela_ll1, terminais)