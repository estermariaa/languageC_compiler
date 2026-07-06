int main() {
    // Declaração direta 
    int vidas = 3;
    int pontos = 0;
    int a;
    a = 0;
    
    // Laço de Repetição
    while (vidas) {
        
        // Matemática com precedência
        pontos = pontos + 1 * 50;
        
        // Condicional IF
        if (pontos) {
            int bonus = 10; // Escopo local! (Nasce e morre aqui)
            pontos = pontos + bonus;
        }
        
        vidas = vidas - 1;
    }
    
    return 0;
}