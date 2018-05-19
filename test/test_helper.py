# -*- coding: utf-8 -*-

from src.grammar import Grammar
from src.helper import grammar_has_productions_longer_than


def test_grammar_has_productions_longer_than():
    """Testa a função que verifica se a gramática tem produções maiores que x"""
    terminals = ["a", "b", "u", "v"]
    variables = ["S", "Z", "B", "X", "Y", "A"]
    initial = "S"
    rules = {"S": [["X", "Y", "Z"]],
             "A": [["a"]],
             "B": [["b"]],
             "X": [["A", "X", "A"], ["B", "X", "B"], ["Z"], ["V"]],
             "Y": [["A", "Y", "B"], ["B", "Y", "A"], ["Z"], ["V"]],
             "Z": [["Z", "u"], ["Z", "v"], ["V"]]}

    grammar = Grammar(variables, terminals, rules, initial)

    assert grammar_has_productions_longer_than(grammar, 2)
    assert not grammar_has_productions_longer_than(grammar, 3)
