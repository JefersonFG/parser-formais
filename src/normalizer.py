# -*- coding: utf-8 -*-

from collections import defaultdict
from src.helper import grammar_has_productions_longer_than
from src.simplifier import Simplifier


class Normalizer:
    """Transforma uma gramática livre de contexto qualquer em uma forma normal"""
    @staticmethod
    def to_chomsky_form(grammar):
        """Transforma na forma normal de Chomsky"""
        print("\nTransformação da gramática para a Forma Normal de Chomsky")

        grammar = Simplifier.simplify(grammar)
        print("\nEtapa 1 - gramática simplificada:")
        print(grammar)

        grammar = Normalizer.chomsky_step_2(grammar)
        print("\nEtapa 2 - produções de tamanho maior ou igual a dois só geram variáveis:")
        print(grammar)

        grammar = Normalizer.chomsky_step_3(grammar)
        print("\nEtapa 3 - produções de tamanho maior ou igual a três geram exatamente duas variáveis:")
        print(grammar)

        return grammar

    @staticmethod
    def chomsky_step_2(grammar):
        """Garante que produções de tamanho maior ou igual a dois tenham somente variáveis"""
        # Cria um novo dicionário para manter as novas produções durante a execução da etapa
        new_rules = defaultdict()

        for origin, productions in grammar.rules.items():
            for production in productions:
                num_symbols = len(production)
                # Se a produção tiver mais de dois símbolos
                if num_symbols >= 2:
                    for i in range(num_symbols):
                        # Verifica se existe um símbolo que é terminal
                        if production[i] in grammar.terminals:
                            # Salva o terminal e o substitui na produção por uma nova variável
                            terminal = production[i]
                            new_variable = "C" + terminal
                            production[i] = new_variable
                            # Adiciona a nova variável a lista de variáveis
                            grammar.variables.append(new_variable)
                            # Adiciona uma nova regra levando a variável ao terminal
                            new_rules[new_variable] = [[terminal]]

        # Atualiza as regras de produção da gramática
        grammar.rules = {**grammar.rules, **new_rules}

        return grammar

    @staticmethod
    def chomsky_step_3(grammar):
        """Substitui produções de tamanho maior ou igual a três por produções com exatamente duas variáveis"""
        # Cria um novo dicionário para manter as novas produções durante a execução da etapa
        new_rules = defaultdict()

        # Contador para as variáveis
        n = 1

        # Enquanto houver produções de tamanho maior que dois elementos executa o algoritmo
        while grammar_has_productions_longer_than(grammar, 2):
            for origin, productions in grammar.rules.items():
                for i in range(len(productions)):
                    # Se a produção tiver mais de três símbolos
                    if len(productions[i]) >= 3:
                        # Mantém o primeiro elemento da produção e cria uma variável para gerar os demais
                        production_excedent = productions[i][1:]
                        new_variable = "D" + str(n)
                        n = n + 1
                        # Adiciona a nova variável a lista de variáveis
                        grammar.variables.append(new_variable)
                        # Modifica a produção para levar a primeira variável original junto da nova variável
                        productions[i] = [productions[i][0], new_variable]
                        # Adiciona a nova regra levando a variável aos elementos restantes da produção original
                        new_rules[new_variable] = [production_excedent]

            # Atualiza as regras de produção da gramática
            grammar.rules = {**grammar.rules, **new_rules}

        return grammar
