# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from src.grammar import Grammar


def test_grammar_to_string():
    """Testa a representação em string do objeto que representa a gramática"""
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

    assert_equals(grammar.__str__(), "G = ({S,Z,B,X,Y,A}, {a,b,u,v}, {S -> XYZ | A -> a | B -> b | "
                                     "X -> AXA | X -> BXB | X -> Z | X -> V | Y -> AYB | Y -> BYA | "
                                     "Y -> Z | Y -> V | Z -> Zu | Z -> Zv | Z -> V}, S)")
