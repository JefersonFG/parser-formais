# Formais 2018/1
[![Build Status](https://travis-ci.com/JefersonFG/parser_formais.svg?branch=master)](https://travis-ci.com/JefersonFG/parser_formais)

## Simplificação de GLCs, Forma Normal de Chomsky e Parsing de Linguagem Natural com CYK

## Uso

```bash
usage: parser [-h] arquivo sentenca

Parser de linguagem natural - formais 2018/1

positional arguments:
  arquivo     nome do arquivo de onde importar a gramática
  sentenca    sentença a ser processada pela gramática

optional arguments:
  -h, --help  show this help message and exit
```

## Testes

Para rodar todos os testes execute o seguinte comando à partir da pasta raíz:

```bash
python test/test_runner.py
```

## Trabalhando no projeto

Para trabalhar no projeto é preciso instalar o software [anaconda](https://www.anaconda.com/what-is-anaconda/) ou sua versão enxuta [miniconda](https://conda.io/miniconda.html). À partir dele é possível criar um ambiente virtual com os pacotes utilizados nesse projeto, descritos no arquivo "environment.yml":

```bash
conda env create -f environment.yml -n parser-formais
```

Para gerar um executável à partir do projeto utilizamos o pacote pyinstaller:

```bash
pyinstaller src/parser.py
```

Ele irá gerar o executável dentro da pasta "dist", que pode ser executado com o comando:

```bash
./dist/parser/parser -h
```
