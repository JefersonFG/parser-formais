# -*- coding: utf-8 -*-


class Simplifier:
    """Classe que contém métodos para simplificação de gramáticas"""

    @staticmethod
    def first_algorithms(grammar):
        # Elimina símbolos inúteis nas produções (2 ETAPAS)
        # ETAPA 1 - remove produções que não geram símbolos terminais

        V1 = [] # Variaveis que geram terminais

        for origin, productions in grammar.rules.items():
            for production in productions:
                for terminal in grammar.terminals:  # passa por todos os terminais
                    if terminal in production and origin not in V1:
                        V1.append(origin)

        print("V1: {}".format(V1))  # variaveis que geram terminais diretamente

        for origin, productions in grammar.rules.items():
            for production in productions:
                for variable in V1:
                    # se alguma variavel de V1 estiver nas produções
                    # a origem dessas produções será adicionada à V1 (Se já não estiver)
                    if variable in production and origin not in V1:
                        V1.append(origin)

        print("V1: {}".format(V1))

        grammar.variables = V1

        # ETAPA 2 - Verificação do que é atingível a partir da Variável inicial (S),
        # as variáveis atingíveis são adicionadas à V2
        # e terminais atingíveis são adicionados à T2
        T2 = []
        V2 = ['S']

        for start in V2:  # variavel de onde vai partir
            for start, productions in grammar.rules.items():  # ve as produções da variavel
                for production in productions:
                    for variable in grammar.variables:
                        if variable in productions:  # se tiver alguma variavel nas produções, então ela é atingível
                            V2.append(variable)
                        # tambem deve-se adicionar os terminais dessa produção
                        for terminal in grammar.terminals:
                            T2.append(terminal)

        grammar.terminals = T2
        grammar.variables = V2

        # Eliminação de Produções vazias (3 ETAPAS)

        # ETAPA 1
        # forma do livro

        Ve = []  # conjunto de variáveis que geram o vazio de forma direta ou indireta

        for origin, productions in grammar.rules.items():
            for production in productions:
                if 'V' in production:
                    Ve.append(origin)  # adiciona todas as variáveis que produzem vazio à Ve

        for origin, productions in grammar.rules.items():
            for production in productions:
                for emptyVar in Ve:
                    if emptyVar in production:
                        Ve.append(origin)  # gera indiretamente o vazio

        # ETAPA 2

        P1 = {}  # todas as produções que nao geram vazio

        for origin, productions in grammar.rules.items():
            for production in productions:
                if 'V' not in production:
                    P1.update({origin:production})  # adiciona todas as produções que não tem vazio do lado direito à P1

        for origin, productions in P1.items():
            for production in productions:
                for emptyVar in Ve:
                    if emptyVar in P1:
                        # adiciona produção que antes tinha Y =>+ V, aYa|aa
                        P1.update({origin: production.remove(emptyVar)})

        # ETAPA 3

        if len(Ve) > 0:
            P2 = P1
            P2.update({'S': 'V'})  # adiciona a produção vazia, caso ela faça parte da linguagem

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
