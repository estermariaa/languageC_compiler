# Compilador para Linguagem C (em desenvolvimento)

Este projeto tem como objetivo a construção de um **compilador para a linguagem C**, desenvolvido de forma incremental como parte de estudos em **Compiladores**.

Atualmente, o projeto implementa a primeira etapa do processo de compilação:

## Analisador Léxico (Scanner)

O analisador léxico é responsável por percorrer o código-fonte caractere por caractere e identificar os **tokens** da linguagem, além de detectar **erros léxicos**.

---

## Funcionalidades implementadas

O analisador léxico reconhece:

*  **Palavras reservadas**

    * Ex: `int`, `main`, `printf`, `scanf`, `return`

*  **Identificadores**

    * Ex: `x`, `contador`, `aluno1`, `_teste`

*  **Números inteiros positivos**

    * Ex: `10`, `42`, `0`
    * Detecta erro em casos inválidos como: `34a56`

*  **Operadores**

    * Simples: `+`, `-`, `*`, `/`, `=`, `<`, `>`
    * Compostos: `==`, `!=`, `<=`, `>=`, `&&`, `||`, `++`, `--`, `+=`, etc.
    * Detecta operadores inválidos como: `=+`
    * Não permite `&` ou `|` isolados

*  **Literais (strings)**

    * Ex: `"Hello World"`
    * Detecta erro de string não fechada

* **Comentários**

    * Linha: `// comentário`    
    * Bloco: `/* comentário */`
    * Detecta comentário de bloco não fechado

* **Separadores**

    * `(` `)` `{` `}` `;` `,` `[` `]` ` ` `   ` `\n`

---

## Tratamento de erros léxicos

O analisador identifica e registra:

* Caracteres inválidos (ex: `#`)
* Números com sequência inválida (`123abc`)
* Strings não fechadas
* Comentários não fechados
* Operadores inválidos (`=+`, `&`, `|`)

Os erros são armazenados separadamente.

---

## Estrutura de saída

Após a execução, são gerados dois arquivos:

### `tokens.txt`

Contém os tokens válidos identificados:

```
CLASSE          VALOR           (linha X, coluna Y)
```

Exemplo:

```
RESERVADA       int             (linha 1, coluna 1)
IDENTIFICADOR   x               (linha 1, coluna 5)
OPERADOR        =               (linha 1, coluna 7)
NUMERAL         10              (linha 1, coluna 9)
```

---

### `erros.txt`

Contém os erros léxicos encontrados:

```
ERRO        valor        (linha X, coluna Y)
```

Exemplo:

```
ERRO        34a56        (linha 2, coluna 3)
ERRO        =+           (linha 4, coluna 10)
```

---

## Como executar

1. Certifique-se de ter o Python instalado
2. Coloque o código de entrada em um arquivo chamado:

```
codigo_entrada.c
```

3. Execute o analisador:

```bash
python analisador_lexico.py
```

4. Verifique os arquivos gerados:

* `tokens.txt`
* `erros.txt`

---

## Próximas etapas

Este projeto faz parte da construção de um compilador completo. As próximas fases incluem:

* Análise Sintática 
* Análise Semântica
* Otimizações
* Geração de Código 

---

## Autora

Ester Maria

---
