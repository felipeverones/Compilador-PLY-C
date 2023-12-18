
int main()
{
    //isto é um comentário
    /* isto também é um comentário */

    /* int i; */
    int cont;
    int i, n, fact = 1;  //verificação semântica de variável i já declarada
    float j = 5.4;
    double aa = 5.68098;
    double a = 5.68;
    char c[] = "c string";
    char letra = 'z';

    aa =  1; // atribuição de int para float ou double
    aa = 5; // atribuição de int para float ou double

    aa ++;
    /* i = 12.7; */  // erro semântico: atribuição de não inteiro a inteiro

    aa = 1 + 1;       

    if( j == 5.4 && a == 5.68){
        int x = 0;
        printf("Teste");
         x += fact;
         /* x = naodeclarada; */ // verificação semântica de variável não declarada
    }
    else{
        a = 4;
    }
    /* letra = a; */    // verificação semântica de tipos incompatíveis

    
    
    printf("Enter a number: ");
    scanf("%d", &n);
    
    for (i = 1; i <= n; i++){
        fact *= i;
    }
    
    printf("Factorial of %d is %d\n", n, fact);
    if (n < 0)
    {
        printf("Error! Factorial of a negative number doesn't exist.");
    }
    else
    {
        printf("Factorial of %d is %d \n", n, fact);
    }
    
    while (n > 0)
    {
        printf("n = %d\n", n);
        n--;
    }
    
    return 0;
}