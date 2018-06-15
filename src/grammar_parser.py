# -*- coding: utf-8 -*-


class Parser:
    """Faz o reconhecimento de uma sentença para uma dada gramática"""

    @staticmethod
    def parse_cyk(grammar, sentence):
        """Faz o reconhecimento da sentença usando o algoritmo CYK

        A gramática deve estar na Forma Normal de Chomsky"""
        print("\nFazendo o reconhecimento da gramática utilizando o algoritmo CYK")

        if len(sentence) == 1 and sentence[0] not in grammar.terminals:
            sentence = list(sentence[0])

        # Matriz quadrada do tamanho da palavra
        n = len(sentence)

        # Inicializa tabela com '-' em todas as posições (equivalente ao vazio)
        matrix = [[['-'] for col in range(n)] for row in range(n)]

        # ETAPA 1
        # Produções que geram terminais da sentença diretamente A -> a

        for r in range(n):
            for origin, productions in grammar.rules.items():
                for production in productions:
                    if len(production) == 1 and production[0] == sentence[r]:
                        if matrix[0][r][0] == '-':
                            matrix[0][r] = [origin]
                        elif origin not in matrix[0][r]:
                            matrix[0][r].append(origin)

        # ETAPA 2
        # Produções que geram 2 variáveis A -> BC

        for s in range(2, n + 1):
            for r in range(1, n - s + 2):
                for k in range(1, s):
                    for origin, productions in grammar.rules.items():
                        for production in productions:
                            if len(production) == 2:
                                if production[0] in matrix[k-1][r-1] and production[1] in matrix[s-k-1][r+k-1]:
                                    if matrix[s-1][r-1][0] == '-':
                                        matrix[s-1][r-1] = [origin]
                                    elif origin not in matrix[s-1][r-1]:
                                        matrix[s-1][r-1].append(origin)

        # ETAPA 3
        # Condição de aceitação da entrada

        print("\nTabela de derivação da sentença no algoritmo CYK:")
        for row in reversed(matrix):
            print(row)

        return grammar.start in matrix[n-1][0]
