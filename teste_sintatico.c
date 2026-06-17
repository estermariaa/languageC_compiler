
// ERRO 1: Assinatura do programa errada.
printf("ola"); 

int main() {
    
    // ERRO 2: Declaração com número no lugar do identificador
    int 5;

    // ERRO 3: Esquecer o ponto e vírgula (O clássico dos programadores C!)
    int x = 10
    
    // ERRO 4: Matemática maluca (dois operadores seguidos)
    int y = 5 + * 3;
    
    // ERRO 5: Variável recebendo palavra reservada
    x = if;
    
    // ERRO 6: Parênteses não fechados na expressão
    x = (5 + 3 ;
    
    // ERRO 7: Chamada de IO (printf) com tipo errado
    printf(100);
    
    // ERRO 8: IF sem o Bloco de chaves {}
    if (x) x = 1;
    
    // ERRO 9: Return com tipo errado
    return x;

}