int main() {
    // 1. Declarada e Usada
    int nota_prova;
    nota_prova = 10;

    int global_var;
    global_var = 10;

    // 2. ERRO SEMÂNTICO: Tentando declarar a mesma variável de novo
    int nota_prova;

    // 3. WARNING: Variável declarada, mas nunca usada
    int media_final;
    int aluno_fantasma;

    // 4. ERRO SEMÂNTICO: Usando uma variável que não existe
    nota_trabalho = 8;

    // 5. Cenário misto: A regra do '@VERIFICAR' agindo dentro da expressão
    // 'media_final' existe e vai ser validada, mas 'bonus' não existe.
    media_final = nota_prova + bonus;

    if (global_var) {
        // Entramos num novo escopo!
        int local_var;
        int fantasma_local;
        
        // Funciona, porque o local enxerga o global:
        local_var = global_var; 
        
    }
    // ERRO! Tentando usar a variável local do lado de fora do bloco
    local_var = 5;

    int nota;
    float media;
    char conceito;

    // Teste 1: Atribuição correta
    nota = 10;
    
    // Teste 2: ERRO DE TIPO - Tentando guardar string num inteiro
    nota = "Aprovado"; 
    
    // Teste 3: ERRO DE TIPO - Tentando guardar número num char
    conceito = 100;
    
    // Teste 4: Expressões mistas corretas 
    media = nota + 5;
    
    // Teste 5: ERRO DE TIPO no meio de uma conta grande
    // A soma envolve uma variável char, o que contamina a expressão
    conceito = "A";
    media = nota + conceito;

    nota = nota + media;

    return 0;
}