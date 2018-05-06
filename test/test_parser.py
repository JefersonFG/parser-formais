# -*- coding: utf-8 -*-

from src.parser import my_sum


def test_my_sum():
    """Teste para causar a primeira build do Travis"""
    assert(my_sum(1, 2) == 3)
