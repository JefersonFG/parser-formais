# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from collections import Counter
from src.grammar import Grammar
from src.simplifier import Simplifier


def test_empty_productions():
    """Testa a simplificação de produções vazias"""
    terminals = ["a", "b"]
    variables = ["S", "X", "Y"]
    initial = "S"
    rules = {"S": [["a", "X", "a"], ["b", "X", "b"], ["V"]],
             "X": [["a"], ["b"], ["Y"]],
             "Y": [["V"]]}

    original_grammar = Grammar(variables, terminals, rules, initial)

    terminals = ["a", "b"]
    variables = ["S", "X", "Y"]
    initial = "S"
    rules = {"S": [["a", "X", "a"], ["b", "X", "b"], ["a", "a"], ["b", "b"], ["V"]],
             "X": [["a"], ["b"], ["Y"]]}

    expected_grammar = Grammar(variables, terminals, rules, initial)

    simplified_grammar = Simplifier.empty_productions(original_grammar)

    assert_equals(expected_grammar, simplified_grammar)


def test_useless_symbols():
    """Testa a simplificação de símbolos inúteis"""
    terminals = ["a", "b", "c"]
    variables = ["S", "A", "B", "C"]
    initial = "S"
    rules = {"S": [["a", "A", "a"], ["b", "B", "b"]],
             "A": [["a"], ["S"]],
             "C": [["c"]]}

    original_grammar = Grammar(variables, terminals, rules, initial)

    terminals = ["a"]
    variables = ["S", "A"]
    initial = "S"
    rules = {"S": [["a", "A", "a"]],
             "A": [["a"], ["S"]]}

    expected_grammar = Grammar(variables, terminals, rules, initial)

    simplified_grammar = Simplifier.useless_symbols(original_grammar)

    assert_equals(expected_grammar, simplified_grammar)


def test_simple_production_simplification():
    """Testa a simplificação de produções que substituem variáveis"""
    terminals = ["a", "b"]
    variables = ["S", "X"]
    initial = "S"
    rules = {"S": [["a", "X", "a"], ["b", "X", "b"]],
             "X": [["a"], ["b"], ["S"], ["V"]]}

    original_grammar = Grammar(variables, terminals, rules, initial)

    terminals = ["a", "b"]
    variables = ["S", "X"]
    initial = "S"
    rules = {"S": [["a", "X", "a"], ["b", "X", "b"]],
             "X": [["a"], ["b"], ["V"], ["a", "X", "a"], ["b", "X", "b"]]}

    expected_grammar = Grammar(variables, terminals, rules, initial)

    simplified_grammar = Simplifier.simple_production(original_grammar)

    assert_equals(expected_grammar, simplified_grammar)


def test_simple_production_simplification_step_1():
    """Testa a primeira etapa da simplificação de produções que substituem variáveis"""
    terminals = ["a", "b", "c", "d", "e"]
    variables = ["A", "B", "C", "D", "E"]
    initial = "A"
    rules = {"A": [["A", "a"], ["B"], ["C"]],
             "B": [["b", "B", "b"], ["D"]],
             "C": [["c"], ["E"]],
             "D": [["d"]],
             "E": [["e"]]}

    grammar = Grammar(variables, terminals, rules, initial)

    expected_transitive_closure_list = {"A": ["B", "C", "D", "E"], "B": ["D"], "C": ["E"], "D": [], "E": []}

    transitive_closure_list = Simplifier.simple_production_step_1(grammar)

    # Converte as listas para contadores para a comparação
    # Dessa forma a ordem dos elementos não afeta o resultado, mas sim suas quantidades
    for key in expected_transitive_closure_list:
        expected_transitive_closure_list[key] = Counter(expected_transitive_closure_list[key])

    for key in transitive_closure_list:
        transitive_closure_list[key] = Counter(transitive_closure_list[key])

    assert_equals(transitive_closure_list, expected_transitive_closure_list)


def test_simple_production_simplification_step_2():
    """Testa a segunda etapa da simplificação de produções que substituem variáveis"""
    terminals = ["a", "b", "c", "d", "e"]
    variables = ["A", "B", "C", "D", "E"]
    initial = "A"
    rules = {"A": [["A", "a"], ["B"], ["C"]],
             "B": [["b", "B", "b"], ["D"]],
             "C": [["c"], ["E"]],
             "D": [["d"]],
             "E": [["e"]]}

    original_grammar = Grammar(variables, terminals, rules, initial)

    terminals = ["a", "b", "c", "d", "e"]
    variables = ["A", "B", "C", "D", "E"]
    initial = "A"
    rules = {"A": [["A", "a"], ["b", "B", "b"], ["c"], ["d"], ["e"]],
             "B": [["b", "B", "b"], ["d"]],
             "C": [["c"], ["e"]],
             "D": [["d"]],
             "E": [["e"]]}

    expected_grammar = Grammar(variables, terminals, rules, initial)

    transitive_closure_list = Simplifier.simple_production_step_1(original_grammar)
    simplified_grammar = Simplifier.simple_production_step_2(original_grammar, transitive_closure_list)

    assert_equals(expected_grammar, simplified_grammar)
