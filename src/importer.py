# -*- coding: utf-8 -*-

from collections import defaultdict
from src.grammar import Grammar


class Importer:
    """Classe que lê uma gramática de um arquivo"""
    def __init__(self):
        self.state = 0
        self.keywords = ["#Terminais", "#Variaveis", "#Inicial", "#Regras"]

    def import_from_file(self, file_name):
        # Lê o arquivo e guarda as linhas em uma lista
        with open(file_name) as f:
            content = f.readlines()

        terminals = []
        variables = []
        initial = ""
        rules = defaultdict()

        for line in content:
            # Remove espaços, tabs e newlines
            line = line.replace(" ", "")
            line = line.replace("\t", "")
            line = line.replace("\n", "")

            # Verifica se a linha é uma keyword, se sim atualiza o estado
            if self.state < 4 and line.startswith(self.keywords[self.state]):
                self.state += 1
                continue

            # Remove comentários
            line = line.split('#', 1)[0]

            # Terminais
            if self.state == 1:
                # Remove [ e ]
                line = line.split('[', 1)[1]
                line = line.split(']', 1)[0]
                terminals.append(line)

            # Variáveis
            if self.state == 2:
                # Remove [ e ]
                line = line.split('[', 1)[1]
                line = line.split(']', 1)[0]
                variables.append(line)

            # Inicial
            if self.state == 3:
                # Remove [ e ]
                line = line.split('[', 1)[1]
                line = line.split(']', 1)[0]
                initial = line

            # Regras de produção
            if self.state == 4:
                # Separa em origem e produção
                origin = line.split('>')[0]
                production = line.split('>')[1]

                # Origem
                origin = origin.split('[', 1)[1]
                origin = origin.split(']', 1)[0]

                # Produção
                # Separa por '[' e remove a string vazia do início
                production = production.split('[')
                production = list(filter(None, production))

                # Remove ']' de cada elemento
                production[:] = [s[:-1] for s in production]

                if origin in rules:
                    rules[origin].append(production)
                else:
                    rules[origin] = [production]

        return Grammar(variables, terminals, rules, initial)
