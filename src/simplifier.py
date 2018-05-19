# -*- coding: utf-8 -*-

import copy

class Simplifier:
    """Classe que contém métodos para simplificação de gramáticas"""

    @staticmethod
    def simplify(grammar):
        """Simplifica a gramática aplicando os três algoritmos na ordem recomendada"""
        print("\nSimplificando a gramática")

        # Remove produções vazias
        # TODO Não funcional
        # grammar = Simplifier.empty_productions(grammar)

        # Remove produções que substituem variáveis
        grammar = Simplifier.simple_production(grammar)

        # Remove símbolos inúteis
        # TODO Não funcional
        # grammar = Simplifier.useless_symbols(grammar)

        return grammar

    @staticmethod
    def empty_productions(grammar):
        """Simplifica produções vazias"""

        # Eliminação de Produções vazias (3 ETAPAS)
        print("Eliminação de produções vazias")
        print("Etapa 1: variáveis que constituem produções vazias")
        # ETAPA 1
        # forma do livro
        Ve = []  # conjunto de variáveis que geram o vazio de forma direta ou indireta
        for origin, productions in grammar.rules.items():
            for production in productions:
                if 'V' in production:
                    Ve.append(origin)  # adiciona todas as variáveis que produzem vazio à Ve
        
        contador = 0
        while (contador == 0):
            contador = 1
            for origin, productions in grammar.rules.items():
                for production in productions:
                    for emptyVariable in Ve:
                        if emptyVariable in production and origin not in Ve:
                            Ve.append(origin)
                            contador = 0
        print("Ve: ")
        print(Ve)


        # ETAPA 2
        
        print("Etapa 2: exclusão de produções vazias")
        P1 = {}
        for origin, productions in grammar.rules.items():
            for production in productions:
                if 'V' not in production:
                    if origin in P1:
                        P1[origin].append(production)
                    else:
                        P1[origin] = [production]

        contador = 0
        while (contador == 0):
            contador = 1
            for origin, productions in P1.items():
                for production in productions:
                    for variable in Ve:
                        if variable in production:
                            newProduction = copy.deepcopy(production)
                            newProduction.remove(variable)
                            if newProduction not in P1[origin] and newProduction: #se nao foi add, se nao gerou um vazio, add!
                                contador = 0
                                P1[origin].append(newProduction)

        # Etapa 3
        # Se possui V, inserir INICIO -> V
        print("Etapa 3: geração da palavra vazia, se necessário")

        if Ve:
            P1[grammar.start].append(['V'])


        print(P1)

        grammar.variables = Ve
        grammar.rules = P1
        print("Gramática resultante:")
        print(grammar)


        return grammar

    @staticmethod
    def useless_symbols(grammar):
        """Simplifica símbolos inúteis"""

        # ETAPA 1 - remove produções que não geram símbolos terminais

        print("GRAMATICA RECEBIDA\n")
        print(grammar)
        print("\n\n\n")

        V1 = []  # Variaveis que geram terminais

        contador = 0
        while contador == 0:
            contador = 1
            for origin, productions in grammar.rules.items():
                for production in productions:
                    for terminal in grammar.terminals:  # passa por todos os terminais
                        if terminal in production and len(production) == 1:
                            if origin not in V1:
                                V1.append(origin)  # adiciona produções do tipo A -> a à V1
                                contador = 0
                        
        print("\n\n")
        print("V1 DIRETO: {}".format(V1))  # variaveis que geram terminais diretamente
        print("\n\n")

        # V1 DIRETO CORRETO

        contador = 0
        while contador == 0:
            contador = 1
            for origin, productions in grammar.rules.items():
                for production in productions:
                    for variable in V1:
                        # se alguma variavel de V1 estiver nas produções
                        # a origem dessas produções será adicionada à V1 (Se já não estiver)
                        if variable in production and origin not in V1:
                            V1.append(origin)
                            contador = 0

        print("\n\n")
        print("V1 DIRETO E INDIRETO: {}".format(V1))
        # V1 DIRETO E INDIRETO CORRETO

        grammar.variables = V1

        # ETAPA 2 - Verificação do que é atingível a partir da Variável inicial (S),
        # as variáveis atingíveis são adicionadas à V2
        # e terminais atingíveis são adicionados à T2
        T2 = []
        V2 = ['S']

        for start in V2:  # variavel de onde vai partir
            print("START = {}".format(start))
            contador = 0
            while contador == 0:
                contador = 1
                for origin, productions in grammar.rules.items():  # ve as produções da variavel
                    for production in productions:
                        for variable in grammar.variables:
                            if variable in production and variable not in V2:  # se tiver alguma variavel nas produções, então ela é atingível
                                V2.append(variable)
                                for terminal in production:
                                    if terminal in grammar.terminals and terminal not in T2:
                                        T2.append(terminal)
                                        contador = 0

        print("\n\n")
        print("V2: {}".format(V2)) #CORRETO

        print("\n\n")
        print("T2: {}".format(T2)) #CORRETO


        grammar.terminals = T2
        grammar.variables = V2

        print("GRAMATICA:")
        print (grammar)

        return grammar

    @staticmethod
    def simple_production(grammar):
        """Simplifica produções que substituem variáveis"""
        print("\nSimplificação de produções que substituem variáveis")

        transitive_closure_list = Simplifier.simple_production_step_1(grammar)
        print("\nEtapa 1 - lista de fechos das variáveis:")
        print(transitive_closure_list)

        grammar = Simplifier.simple_production_step_2(grammar, transitive_closure_list)
        print("\nEtapa 2 - remoção de substituição de variáveis:")
        print(grammar)

        return grammar

    @staticmethod
    def simple_production_step_1(grammar):
        """Gera o fecho transitivo de cada variável da gramática"""
        # Lista de fechos transitivos
        transitive_closure_list = {}

        for variable in grammar.variables:
            transitive_closure = []

            # Na primeira execução obtém o fecho transitivo da variável
            new_transitive_closure = Simplifier.get_immediate_transitive_closure(grammar, variable)
            new_elements = list(set(new_transitive_closure))

            # Se há elementos no fecho transitivo da variável adiciona na lista
            if len(new_elements) > 0:
                transitive_closure = transitive_closure + new_elements

                inner_list = []
                inner_size = -1

                # Se o fecho transitivo não for vazio obtém o fecho transitivo de cada variável alcançada
                # recursivamente até nenhum novo elemento ser adicionado
                while inner_size != 0:
                    # Obtém o fecho transitivo de cada elemento
                    for new_variable in transitive_closure:
                        new_transitive_closure = Simplifier.get_immediate_transitive_closure(grammar, new_variable)
                        new_elements = list(set(new_transitive_closure) - set(transitive_closure))

                        if len(new_elements) > 0:
                            inner_list = inner_list + new_elements

                    # Obtém os novos elementos alcançados pelo fecho transitivo da variável
                    new_elements = list(set(inner_list))
                    inner_size = len(new_elements)

                    # Limpa a lista interna
                    inner_list.clear()

                    # Adiciona os novos elementos na lista
                    if inner_size > 0:
                        transitive_closure = transitive_closure + new_elements

            # Salva o fecho transitivo da variável em um dicionário
            transitive_closure_list[variable] = transitive_closure

        return transitive_closure_list

    @staticmethod
    def get_immediate_transitive_closure(grammar, variable):
        """Obtém o fecho transitivo imediato da variável dentro da gramática"""
        transitive_closure = []

        if variable in grammar.rules:
            productions = grammar.rules[variable]
            for production in productions:
                if len(production) == 1 and production[0] in grammar.variables:
                    transitive_closure.append(production[0])

        return transitive_closure

    @staticmethod
    def simple_production_step_2(grammar, transitive_closure_list):
        """Remove as produções que substituem variáveis"""
        for variable, transitive_closure in transitive_closure_list.items():
            for element in transitive_closure:
                # Itera sobre as variáveis do fecho
                if element in grammar.rules.keys():
                    productions = grammar.rules[element]
                    for production in productions:
                        # Verifica se a variável gera uma produção que não seja só outra variável
                        if len(production) != 1 or production[0] in grammar.terminals:
                            # Adiciona a produção da variável do fecho à lista de produções da variável original
                            grammar.rules[variable].append(production)
                            # Se a variável é produção direta da original, remove da lista de produções
                            production_of_element = [element]
                            if production_of_element in grammar.rules[variable]:
                                grammar.rules[variable].remove(production_of_element)

        return grammar
