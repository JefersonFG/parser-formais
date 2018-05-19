# -*- coding: utf-8 -*-

import argparse
from src.importer import Importer
from src.normalizer import Normalizer


parser = argparse.ArgumentParser(description="Parser de linguagem natural - formais 2018/1")
parser.add_argument('arquivo', help='nome do arquivo de onde importar a gramática')
parser.add_argument('sentenca', help='sentença a ser processada pela gramática')

args = parser.parse_args()

importer = Importer()

try:
    # Importa a gramática do arquivo
    grammar = importer.import_from_file(args.arquivo)

    # Converte a gramática para a Forma Normal de Chomsky
    grammar = Normalizer.to_chomsky_form(grammar)

except FileNotFoundError:
    print("O arquivo " + args.arquivo + " não existe!")
