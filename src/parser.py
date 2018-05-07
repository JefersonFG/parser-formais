# -*- coding: utf-8 -*-

import argparse
from src.importer import Importer


parser = argparse.ArgumentParser(description="Parser de linguagem natural - formais 1028/1")
parser.add_argument('arquivo', help='nome do arquivo de onde importar a gramática')
parser.add_argument('sentenca', help='sentença a ser processada pela gramática')

args = parser.parse_args()

importer = Importer()

try:
    grammar = importer.import_from_file(args.arquivo)

    print("Gramática importada:")
    print(grammar.to_string())

except FileNotFoundError:
    print("O arquivo " + args.arquivo + " não existe!")
