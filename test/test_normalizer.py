# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from src.grammar import Grammar
from src.normalizer import Normalizer


def test_chomsky_form():
    """Testa a transformação de uma gramática para a Forma Normal de Chomsky"""
    terminals = ["+", "*", "[", "]", "x"]
    variables = ["E"]
    initial = "E"
    rules = {"E": [["E", "+", "E"], ["E", "*", "E"], ["[", "E", "]"], ["x"]]}

    original_grammar = Grammar(variables, terminals, rules, initial)

    terminals = ["+", "*", "[", "]", "x"]
    variables = ["E", "C+", "C*", "C[", "C]", "D1", "D2", "D3"]
    initial = "E"
    rules = {"E": [["E", "D1"], ["E", "D2"], ["C[", "D3"], ["x"]],
             "D1": [["C+", "E"]],
             "D2": [["C*", "E"]],
             "D3": [["E", "C]"]],
             "C+": [["+"]],
             "C*": [["*"]],
             "C[": [["["]],
             "C]": [["]"]]}

    expected_grammar = Grammar(variables, terminals, rules, initial)

    normalized_grammar = Normalizer.to_chomsky_form(original_grammar)

    assert_equals(expected_grammar, normalized_grammar)


def test_chomsky_step_2():
    """Testa a segunda etapa da transformação de uma gramática para a Forma Normal de Chomsky"""
    terminals = ["+", "*", "[", "]", "x"]
    variables = ["E"]
    initial = "E"
    rules = {"E": [["E", "+", "E"], ["E", "*", "E"], ["[", "E", "]"], ["x"]]}

    original_grammar = Grammar(variables, terminals, rules, initial)

    terminals = ["+", "*", "[", "]", "x"]
    variables = ["E", "C+", "C*", "C[", "C]"]
    initial = "E"
    rules = {"E": [["E", "C+", "E"], ["E", "C*", "E"], ["C[", "E", "C]"], ["x"]],
             "C+": [["+"]],
             "C*": [["*"]],
             "C[": [["["]],
             "C]": [["]"]]}

    expected_grammar = Grammar(variables, terminals, rules, initial)

    normalized_grammar = Normalizer.chomsky_step_2(original_grammar)

    assert_equals(expected_grammar, normalized_grammar)


def test_chomsky_step_3():
    """Testa a terceira etapa da transformação de uma gramática para a Forma Normal de Chomsky"""
    terminals = ["+", "*", "[", "]", "x"]
    variables = ["E", "C+", "C*", "C[", "C]"]
    initial = "E"
    rules = {"E": [["E", "C+", "E"], ["E", "C*", "E"], ["C[", "E", "C]"], ["x"]],
             "C+": [["+"]],
             "C*": [["*"]],
             "C[": [["["]],
             "C]": [["]"]]}

    original_grammar = Grammar(variables, terminals, rules, initial)

    terminals = ["+", "*", "[", "]", "x"]
    variables = ["E", "C+", "C*", "C[", "C]", "D1", "D2", "D3"]
    initial = "E"
    rules = {"E": [["E", "D1"], ["E", "D2"], ["C[", "D3"], ["x"]],
             "D1": [["C+", "E"]],
             "D2": [["C*", "E"]],
             "D3": [["E", "C]"]],
             "C+": [["+"]],
             "C*": [["*"]],
             "C[": [["["]],
             "C]": [["]"]]}

    expected_grammar = Grammar(variables, terminals, rules, initial)

    normalized_grammar = Normalizer.chomsky_step_3(original_grammar)

    assert_equals(expected_grammar, normalized_grammar)
