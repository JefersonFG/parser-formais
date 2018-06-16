# -*- coding: utf-8 -*-

import argparse
from src.importer import Importer
from src.normalizer import Normalizer
from src.grammar_parser import Parser


parser = argparse.ArgumentParser(description="Parser de linguagem natural - formais 2018/1")
parser.add_argument('arquivo', help='nome do arquivo de onde importar a gramática')
parser.add_argument('sentenca', help='sentença a ser processada pela gramática', nargs='*')

args = parser.parse_args()

importer = Importer()

try:
    # Importa a gramática do arquivo
    grammar = importer.import_from_file(args.arquivo)

    # Converte a gramática para a Forma Normal de Chomsky
    grammar = Normalizer.to_chomsky_form(grammar)

    # Faz o reconhecimento da sentença na gramática usando o algoritmo CYK
    if Parser.parse_cyk(grammar, args.sentenca):
        print("\nA sentença \"{}\" foi aceita pela gramática {}".format(" ".join(args.sentenca), grammar))
    else:
        print("\nA sentença \"{}\" foi rejeitada pela gramática {}".format(" ".join(args.sentenca), grammar))

except FileNotFoundError:
    print("O arquivo " + args.arquivo + " não existe!")
