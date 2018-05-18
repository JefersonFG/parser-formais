# -*- coding: utf-8 -*-


class Grammar:
    """Classe que representa uma gramática na forma G = (V,T,P,S), onde:

    V - variables: conjunto de variáveis na forma de lista de strings
    T - terminals: conjunto de símbolos terminais na forma de lista de strings
    P - rules: regras de produção na forma de dicionário com uma string como
               chave e uma lista de lista de strings como valor
    S - start: símbolo inicial na forma de string
    """

    def __init__(self, v, t, p, s):
        self.variables = v
        self.terminals = t
        self.rules = p
        self.start = s

    def __str__(self):
        """Retorna a gramática em forma de string para exibição na tela"""
        string_return = "G = ({"

        for variable in self.variables:
            string_return += variable + ","

        string_return = string_return[:-1] + "}, {"

        for terminal in self.terminals:
            string_return += terminal + ","

        string_return = string_return[:-1] + "}, {"

        for origin, productions in self.rules.items():
            for production in productions:
                string_return += origin + " -> "
                for symbol in production:
                    string_return += symbol
                string_return += " | "

        string_return = string_return[:-3] + "}, " + self.start + ")"

        return string_return

    def __eq__(self, other):
        """Operador de comparação entre gramáticas"""
        return self.variables == other.variables and self.terminals == other.terminals and \
            self.rules == other.rules and self.start == other.start
