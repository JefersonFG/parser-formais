# -*- coding: utf-8 -*-

from anytree import Node, RenderTree
from copy import deepcopy


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
        table = [[['-'] for _ in range(n)] for _ in range(n)]

        # ETAPA 1
        # Produções que geram terminais da sentença diretamente A -> a

        nodes = [[[] for _ in range(n)] for _ in range(n)]

        for r in range(n):
            for origin, productions in grammar.rules.items():
                for production in productions:
                    if len(production) == 1 and production[0] == sentence[r]:
                        parent = Node(origin)
                        node = Node(sentence[r], parent=parent)

                        if table[0][r][0] == '-':
                            table[0][r] = [origin]
                            nodes[0][r] = [parent]
                        elif origin not in table[0][r]:
                            table[0][r].append(origin)
                            nodes[0][r].append(parent)

        # ETAPA 2
        # Produções que geram 2 variáveis A -> BC

        for s in range(2, n + 1):
            for r in range(1, n - s + 2):
                for k in range(1, s):
                    for origin, productions in grammar.rules.items():
                        for production in productions:
                            if len(production) == 2:
                                if production[0] in table[k-1][r-1] and production[1] in table[s-k-1][r+k-1]:
                                    parent = Node(origin)

                                    for node in nodes[k-1][r-1]:
                                        new_node = deepcopy(node)
                                        if new_node.name == production[0]:
                                            new_node.parent = parent

                                    for node in nodes[s-k-1][r+k-1]:
                                        new_node = deepcopy(node)
                                        if new_node.name == production[1]:
                                            new_node.parent = parent

                                    if table[s-1][r-1][0] == '-':
                                        table[s-1][r-1] = [origin]
                                        nodes[s-1][r-1] = [parent]
                                    elif origin not in table[s-1][r-1]:
                                        table[s-1][r-1].append(origin)
                                        nodes[s-1][r-1].append(parent)
                                    else:
                                        nodes[s-1][r-1].append(parent)

        # ETAPA 3
        # Condição de aceitação da entrada

        print("\nTabela de derivação da sentença no algoritmo CYK:")
        Parser.print_cyk_table(table, sentence)

        print("\nÁrvores de derivação da sentença:")
        if len(nodes[n-1][0]) > 0:
            for node in nodes[n-1][0]:
                if node.name == grammar.start:
                    for pre, _, node in RenderTree(node):
                        print("%s%s" % (pre, node.name))
        else:
            print("Não há árvore de derivação possível para essa sentença")

        return grammar.start in table[n-1][0]

    @staticmethod
    def print_cyk_table(table, sentence):
        """Exibe a tabela gerada pelo algoritmo CYK na tela"""
        size = len(sentence)
        width_list = [-1 for _ in range(size)]
        sentence_copy = deepcopy(sentence)

        for i in range(size):
            if len(sentence[i]) > width_list[i]:
                width_list[i] = len(sentence[i])

        for row in table:
            for i in range(size):
                row[i] = ", ".join(row[i])
                if len(row[i]) > width_list[i]:
                    width_list[i] = len(row[i])

        lines = [[] for _ in range(size)]

        for i in range(size):
            for j in range(size - i):
                lines[i].append(table[i][j].ljust(width_list[j]))
                sentence_copy[i] = sentence[i].ljust(width_list[i])

        for line in reversed(lines):
            print("| {} |".format(" | ".join(line)))

        print("  {}  ".format("   ".join(sentence_copy)))
