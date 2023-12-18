
# Compilador Python para C

Este repositório contém um compilador escrito em Python que reconhece estruturas da linguagem C. Este projeto foi desenvolvido como uma atividade prática para a disciplina de Construção de Compiladores, demonstrando conceitos fundamentais do processo de compilação.


## Estrutura do Repositório

- `main.py` - Implementação principal do compilador em Python.
- `example.c`, `exemplo1.c`, `exemplo2.c` - Exemplos de códigos fonte em C para testar o compilador.
- `README.md` e `Relatório-Compiladores.pdf` - Documentação do projeto.

## Sobre o Compilador

### Implementação e Funcionalidades

- **Análise Léxica e Sintática**: Utiliza a biblioteca PLY (Python Lex-Yacc) para realizar análise léxica e sintática. A análise léxica é feita através de expressões regulares para identificar tokens, enquanto a análise sintática segue as regras de produção da gramática da linguagem C.
- **Tabela de Símbolos**: Mantém uma tabela de símbolos para gerenciar identificadores e seus tipos, valores e contexto.
- **Reconhecimento de Estruturas**: Capaz de identificar declarações de variáveis, expressões aritméticas, lógicas, estruturas de controle como if, while e for, e operações como atribuição e incremento/decremento.
- **Gestão de Erros**: Reporta erros léxicos, sintáticos e semânticos, melhorando a depuração e compreensão do código.

### Uso da Biblioteca PLY

- PLY é utilizada para definir os tokens, as regras de produção da gramática e as ações associadas a cada regra.
- O projeto faz uso extensivo de expressões regulares para definir tokens e padrões na linguagem C.

## Como executar o código?

* Garanta que Python e PLY estão instalados.
* Pela linha de comando, digite `python main.py` para executar o arquivo principal e iniciar a análise do código C. O arquivo `example.c` é utilizado como entrada padrão.
* Certifique-se de definir, na linha 403 do arquivo, qual `arquivo.c` ou `arquivo.txt` ele deverá ler para analisar a linguagem.
* Na pasta, deverão ter 3 arquivos em linguagem C: `example.c` (default no `main.py`), `exemplo1.c` e `exemplo2.c`
* Escolha o que deseja ler, substitua na linha 403 do `main.py` e execute com o comando acima, ou com o auxílio de extensões para executar python em sua IDE de preferência.
* O compilador irá processar o arquivo de entrada e exibir a saída, incluindo quaisquer erros encontrados.

## Contribuições

Contribuições para melhorar ou expandir as funcionalidades do compilador são bem-vindas. Sugestões de melhorias ou relatórios de bugs podem ser enviados através de issues ou pull requests.

## Licença

Este projeto é distribuído sob a [Licença MIT](LICENSE).
