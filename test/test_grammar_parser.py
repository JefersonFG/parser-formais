# -*- coding: utf-8 -*-

from src.grammar_parser import Parser
from src.grammar import Grammar


def test_cyk():
    """Testa o reconhecimento de sentença utilizando o algoritmo cyk"""
    terminals = ["a", "b"]
    variables = ["S", "A"]
    initial = "S"
    rules = {"S": [["A", "A"], ["A", "S"], ["b"]],
             "A": [["S", "A"], ["A", "S"], ["a"]]}

    grammar = Grammar(variables, terminals, rules, initial)
    sentence = "abaab"

    assert(Parser.parse_cyk(grammar, sentence))


def test_cyk_2():
    """Testa o reconhecimento de sentença utilizando o algoritmo cyk para um segundo caso"""
    terminals = ["she", "eats", "fish", "with", "a", "fork"]
    variables = ["S", "VP", "PP", "NP", "V_", "P", "N", "Det"]
    initial = "S"
    rules = {"S": [["NP", 'VP']],
             "VP": [["VP", "PP"], ["V", "NP"], ["eats"]],
             "PP": [["P", "NP"]],
             "NP": [["Det", "N"], ["she"]],
             "V": [["eats"]],
             "P": [["with"]],
             "N": [["fish"], ["fork"]],
             "Det": [["a"]]}

    grammar = Grammar(variables, terminals, rules, initial)
    sentence = "she eats a fish with a fork"

    assert(Parser.parse_cyk(grammar, sentence))
