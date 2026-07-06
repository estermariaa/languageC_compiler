import re

EPSILON = "&"

gramatica = {
    # inseri símbolos artificiais
    "Programa": [["int", "main", "(", ")", "Bloco", "EOF"]],
    "Bloco": [["{", "@ABRE_ESCOPO", "ListaComandos", "}", "@FECHA_ESCOPO"]],
    "ListaComandos": [["Comando", "ListaComandos"], [EPSILON]],

    "Comando": [["Declaracao"], ["Atribuicao"], ["Condicao"], ["Repeticao"], ["ChamadaIO"], ["Retorno"]],
    
    "Tipo": [["int"], ["float"], ["char"], ["double"]],

    "Declaracao": [["Tipo", "IDENTIFICADOR", "@DECLARAR", "RestoDeclaracao"]],
    "RestoDeclaracao": [[";"], ["=", "Expressao", "@CHECAR_TIPO", "@GER_STORE_DECL", ";"]],
    
    "Atribuicao": [["IDENTIFICADOR", "@SALVAR_ALVO", "=", "Expressao", "@CHECAR_TIPO", "@GER_STORE", ";"]],
    "Condicao": [["if", "(", "Expressao", ")", "@GER_IF", "Bloco", "@GER_IF_END"]],
    "Repeticao": [["while", "@GER_WHILE_START", "(", "Expressao", ")", "@GER_WHILE", "Bloco", "@GER_WHILE_END"]],    
    "ChamadaIO": [["printf", "(", "LITERAL", ")", ";"]],
    "Retorno": [["return", "NUMERAL", ";"]],
    
    "Expressao": [["Termo", "ExpressaoLinha"]],
    "ExpressaoLinha": [["+", "Termo", "@GER_ADD", "ExpressaoLinha"], ["-", "Termo", "@GER_SUB", "ExpressaoLinha"], [EPSILON]],
    "Termo": [["Fator", "TermoLinha"]],
    "TermoLinha": [["*", "Fator", "@GER_MUL", "TermoLinha"], ["/", "Fator", "@GER_DIV", "TermoLinha"], [EPSILON]],
    "Fator": [["IDENTIFICADOR", "@TIPO_ID", "@GER_LOAD_ID"], ["NUMERAL", "@TIPO_NUM", "@GER_LOAD_NUM"], ["LITERAL", "@TIPO_LIT"], ["(", "Expressao", ")"]]
}

terminais = {
    "IDENTIFICADOR", "NUMERAL", "LITERAL", "=", ";", "if", "(", ")", "{", "}", "while",
    "+", "-", "*", "/", "EOF", EPSILON, "int", "float", "char", "double", "main", "printf", "return", "=="
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
        # Pula os marcadores
        if simbolo.startswith("@"):
            continue

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

def parser(tokens_lexico, tabela_ll1, terminais, conjuntos_follow):
    fita_entrada = []
    for token in tokens_lexico:
        classe, valor, linha, coluna = token[0], token[1], token[2], token[3]

        if classe in ["IDENTIFICADOR", "NUMERAL", "LITERAL"]:
            simbolo_gramatica = classe
        else:
            simbolo_gramatica = valor # Para palavras reservadas e operadores

        fita_entrada.append({
            "simbolo": simbolo_gramatica,
            "lexema": valor, 
            "linha": linha,
            "coluna": coluna
        })
            
    ultima_linha = fita_entrada[-1]["linha"] if fita_entrada else 1
    ultima_coluna = fita_entrada[-1]["coluna"] if fita_entrada else 1
    fita_entrada.append({"simbolo": "EOF", "lexema": "EOF", "linha": ultima_linha, "coluna": ultima_coluna}) 
    
    pilha = ["EOF", "Programa"] 
    ponteiro = 0 
    teve_erros = False

    # pilha_escopos é uma lista de dicionários. Cada dicionário é um bloco {} 
    pilha_escopos = [{}] # tabela de simbolos
    # Guarda temporariamente o nome da variável para o semântico
    ultimo_identificador = ""
    ultimo_tipo_lido = ""      # Guarda se é int, float...
    alvo_atribuicao = ""       # Guarda o nome de quem vai receber o valor
    pilha_tipos_expressao = [] # Acumula os tipos da conta matemática

    codigo_assembly = []
    ultimo_numero = ""

    contador_labels = 0 # para lidar com estruturas aninhadas
    pilha_labels = []
    
    print("\n=== INICIANDO ANÁLISE SINTÁTICA E SEMÂNTICA ===")
    
    while len(pilha) > 0:
        if ponteiro >= len(fita_entrada):
            break

        topo = pilha[-1] # o que preciso ler
        
        info_token = fita_entrada[ponteiro] # o que estou lendo
        token_atual = info_token["simbolo"]
        palavra_real = info_token["lexema"]
        linha_atual = info_token["linha"]
        coluna_atual = info_token["coluna"]

        # Guarda o nome da última variável lida
        if token_atual == "IDENTIFICADOR":
            ultimo_identificador = palavra_real
        elif token_atual == "NUMERAL":
            ultimo_numero = palavra_real
        elif token_atual in ["int", "float", "char"]:
            ultimo_tipo_lido = palavra_real

        # Se o topo da pilha for um marcador, o parser PAUSA a análise da fita: logica para o sintatico e o gerador
        if topo.startswith("@"):
            escopo_atual = pilha_escopos[-1] # Olha para o escopo mais interno
            
            if topo == "@ABRE_ESCOPO":
                pilha_escopos.append({})
                
            elif topo == "@FECHA_ESCOPO":
                print("\n" + "="*45)
                print("TABELA DE SÍMBOLOS")
                print("="*45)
                for var, ficha in escopo_atual.items():
                    status_uso = "Sim" if ficha["usada"] else "Não"
                    print(f" Variável: {var:15} | Tipo: {ficha['tipo']:6} | Linha: {ficha['linha']:2} | Usada: {status_uso}")
                    
                    if ficha["usada"] == False:
                        print(f"  WARNING: Variável '{var}' não foi utilizada.")
                print("="*45 + "\n")
                
                pilha_escopos.pop() # Variáveis locais morrem aqui

            elif topo == "@DECLARAR":
                if ultimo_identificador in escopo_atual:
                    teve_erros = True
                    print(f"ERRO SEMÂNTICO [L:{linha_atual}]: '{ultimo_identificador}' já declarada neste escopo!")
                else:
                    # Salva a variável usando o ultimo_tipo_lido
                    escopo_atual[ultimo_identificador] = {
                        "linha": linha_atual, 
                        "usada": False,
                        "tipo": ultimo_tipo_lido 
                    }
                # prepara a variável para caso venha um "= valor" logo na declaração
                alvo_atribuicao = ultimo_identificador
                pilha_tipos_expressao = []

            elif topo == "@VERIFICAR":
                achou = False
                # Procura a variável do escopo mais interno até o global (de trás pra frente)
                for escopo in reversed(pilha_escopos):
                    if ultimo_identificador in escopo:
                        escopo[ultimo_identificador]["usada"] = True
                        achou = True
                        break 
                        
                if not achou:
                    teve_erros = True
                    print(f"ERRO SEMÂNTICO [L:{linha_atual}]: '{ultimo_identificador}' está sendo usada sem ser declarada em nenhum escopo visível!")
            elif topo == "@SALVAR_ALVO":
                alvo_atribuicao = ultimo_identificador
                pilha_tipos_expressao = [] # Limpa a lista para analisar a nova expressão
                
                # Aproveita para verificar se a variável que vai receber o valor existe
                achou = False
                for escopo in reversed(pilha_escopos):
                    if alvo_atribuicao in escopo:
                        escopo[alvo_atribuicao]["usada"] = True
                        achou = True
                        break 
                if not achou:
                    teve_erros = True
                    print(f"ERRO SEMÂNTICO [L:{linha_atual}]: Tentando atribuir valor a '{alvo_atribuicao}', mas ela não existe!")
                    alvo_atribuicao = None

            elif topo == "@TIPO_ID":
                achou = False
                for escopo in reversed(pilha_escopos):
                    if ultimo_identificador in escopo:
                        escopo[ultimo_identificador]["usada"] = True
                        # Joga o tipo da variável na esteira da conta
                        pilha_tipos_expressao.append(escopo[ultimo_identificador]["tipo"])
                        achou = True
                        break 
                if not achou:
                    teve_erros = True
                    print(f"ERRO SEMÂNTICO [L:{linha_atual}]: '{ultimo_identificador}' está sendo usada sem ser declarada!")
                    pilha_tipos_expressao.append("erro")

            elif topo == "@TIPO_NUM":
                pilha_tipos_expressao.append("num") # Números puros servem para int e float

            elif topo == "@TIPO_LIT":
                pilha_tipos_expressao.append("char") # Texto entre aspas vira char

            elif topo == "@CHECAR_TIPO":
                if alvo_atribuicao:
                    tipo_alvo = None
                    for escopo in reversed(pilha_escopos):
                        if alvo_atribuicao in escopo:
                            tipo_alvo = escopo[alvo_atribuicao]["tipo"]
                            break

                    if tipo_alvo:
                        for tipo_expressao in pilha_tipos_expressao:
                            if tipo_expressao == "erro": continue
                            
                            # Não pode colocar char num int double ou float
                            if tipo_alvo in ["int", "float", "double"] and tipo_expressao == "char":
                                teve_erros = True
                                print(f"ERRO DE TIPO [L:{linha_atual}]: Incompatibilidade! Tentando guardar texto em uma variável '{tipo_alvo}' ('{alvo_atribuicao}').")
                                break
                            
                            # Não pode colocar número numa variável char
                            elif tipo_alvo == "char" and tipo_expressao in ["int", "float", "num"]:
                                teve_erros = True
                                print(f"ERRO DE TIPO [L:{linha_atual}]: Incompatibilidade! Tentando guardar número em uma variável 'char' ('{alvo_atribuicao}').")
                                break

                            # Guardar float em int
                            elif tipo_alvo == "int" and tipo_expressao in ["float", "double"]:
                                print(f"WARNING DE TIPO [L:{linha_atual}]: Conversão implícita. Guardando '{tipo_expressao}' na variável 'int' ('{alvo_atribuicao}'). Haverá perda das casas decimais.")
                           
        
                            # Guardar double em float (Perda de precisão)
                            elif tipo_alvo == "float" and tipo_expressao == "double":
                                print(f"WARNING DE TIPO [L:{linha_atual}]: Conversão implícita. Guardando 'double' na variável 'float' ('{alvo_atribuicao}'). Pode haver perda de precisão.")
            
            # gerador
            
            elif topo == "@GER_LOAD_ID":
                codigo_assembly.append(f"  LOAD {ultimo_identificador}")
                
            elif topo == "@GER_LOAD_NUM":
                codigo_assembly.append(f"  LOAD {ultimo_numero}")
                
            elif topo == "@GER_ADD":
                codigo_assembly.append("  ADD")
                
            elif topo == "@GER_SUB":
                codigo_assembly.append("  SUB")
                
            elif topo == "@GER_MUL":
                codigo_assembly.append("  MUL")
                
            elif topo == "@GER_DIV":
                codigo_assembly.append("  DIV")
                
            elif topo in ["@GER_STORE", "@GER_STORE_DECL"]:
                if alvo_atribuicao: # Só gera o GER_STORE se não teve erro semântico antes
                    codigo_assembly.append(f"  STORE {alvo_atribuicao}")

            elif topo == "@GER_WHILE_START":
                contador_labels += 1
                l_start = f"L_START_{contador_labels}"
                l_end = f"L_END_{contador_labels}"
                
                # Guarda na pilha para os próximos passos saberem quem são os labels atuais
                pilha_labels.append((l_start, l_end)) 
                codigo_assembly.append(f"{l_start}:")
                
            elif topo == "@GER_WHILE":
                # Pega os labels do topo da pilha (o while que estamos lendo agora)
                l_start, l_end = pilha_labels[-1]
                # Pula para o fim se a condição for falsa
                codigo_assembly.append(f"  JMPF {l_end}")
                
            elif topo == "@GER_WHILE_END":
                l_start, l_end = pilha_labels.pop() # Tira da pilha porque o while acabou
                # Comando para voltar ao início e testar de novo
                codigo_assembly.append(f"  JMP {l_start}")
                codigo_assembly.append(f"{l_end}:")

            elif topo == "@GER_IF":
                contador_labels += 1
                l_end_if = f"L_END_IF_{contador_labels}"
                
                # Guarda o label do fim desse if na pilha
                pilha_labels.append(l_end_if) 
                
                # Se a condição for falsa, pula lá pro final do bloco IF
                codigo_assembly.append(f"  JMPF {l_end_if}")
                
            elif topo == "@GER_IF_END":
                l_end_if = pilha_labels.pop() 
                # Imprime a linha de chegada para onde o programa vai pular se o IF for falso
                codigo_assembly.append(f"{l_end_if}:")
                    
            pilha.pop() 
            continue
        
        # SUCESSO
        if topo == "EOF" and token_atual == "EOF":
            if teve_erros:
                print("\nFINALIZADO: O código foi lido até o fim, mas contém os erros listados acima.")
            else:
                print("\nSUCESSO: A sintaxe e a semântica do código estão perfeitas!")
                print("\n" + "="*45)
                print(" CÓDIGO INTERMEDIÁRIO GERADO (ASSEMBLY)")
                print("="*45)
                for linha in codigo_assembly:
                    print(linha)
                print("="*45 + "\n")
            
            pilha.pop()
            break
            
        elif topo == token_atual:
            pilha.pop()     
            ponteiro += 1   
            
        # Faltou um terminal obrigatório
        elif topo in terminais:
            teve_erros = True
            print(f"ERRO SINTÁTICO [L:{linha_atual}, C:{coluna_atual}]: Faltou '{topo}' perto de '{palavra_real}'. (Inserindo virtualmente)")
            pilha.pop() # Recupera tirando da pilha
            
        # Regra não terminal: busca a tabela
        elif topo in tabela_ll1:
            if token_atual in tabela_ll1[topo]:
                derivacao = tabela_ll1[topo][token_atual]
                pilha.pop() 
                if derivacao != [EPSILON]:
                    for simbolo in reversed(derivacao):
                        pilha.append(simbolo)
                        
            # Modo Pânico
            else:
                teve_erros = True
                print(f"ERRO SINTÁTICO [L:{linha_atual}, C:{coluna_atual}]: A regra '{topo}' não esperava a palavra '{palavra_real}'.")
                print("   Modo Pânico: Descartando tokens até encontrar sincronização...")
                
                # Avança a fita até achar um token para recuperar
                while ponteiro < len(fita_entrada):
                    token_sync = fita_entrada[ponteiro]["simbolo"]
                    
                    # O token é aceito pela regra atual? 
                    if token_sync in tabela_ll1.get(topo, {}):
                        break
                        
                    # O token é aceito pelo que vem DEPOIS da regra? 
                    if token_sync in conjuntos_follow.get(topo, set()) or token_sync == "EOF":
                        break
                        
                    ponteiro += 1 # Descarta o lixo da fita
                    
                token_sync = fita_entrada[ponteiro]["simbolo"] if ponteiro < len(fita_entrada) else "EOF"
                
                # Se achamos um token de FOLLOW, a regra do topo foi corrompida. Removemos ela.
                # Se achamos um de FIRST, não fazemos nada com a pilha (ela vai ser resolvida na próxima rodada do while).
                if token_sync in conjuntos_follow.get(topo, set()) or token_sync == "EOF":
                    pilha.pop()
        
        else:
            print(f"ERRO [L:{linha_atual}]: Símbolo '{topo}' desconhecido na gramática.")
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
    
    tokens_reais = carregar_tokens_do_arquivo("lista_de_tokens_3.txt") 
    parser(tokens_reais, tabela_ll1, terminais, conjuntos_follow)