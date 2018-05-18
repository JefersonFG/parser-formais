# -*- coding: utf-8 -*-

import argparse
from src.importer import Importer


parser = argparse.ArgumentParser(description="Parser de linguagem natural - formais 2018/1")
parser.add_argument('arquivo', help='nome do arquivo de onde importar a gramática')
parser.add_argument('sentenca', help='sentença a ser processada pela gramática')

args = parser.parse_args()

importer = Importer()

try:
    grammar = importer.import_from_file(args.arquivo)

    print("Gramática importada:")
    print(grammar.to_string())

    # TODO Simplificar a gramática aqui (exibição na tela fica mais limpa)

    # TODO Transformar a gramática para a FNC

except FileNotFoundError:
    print("O arquivo " + args.arquivo + " não existe!")
