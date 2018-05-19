# -*- coding: utf-8 -*-


class Simplifier:
    """Classe que contém métodos para simplificação de gramáticas"""

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
