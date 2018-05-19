# -*- coding: utf-8 -*-


def grammar_has_productions_longer_than(grammar, n):
    """Verifica se a gramática tem produções de comprimento maior que n"""
    for origin, productions in grammar.rules.items():
        for production in productions:
            if len(production) > n:
                return True
    return False
