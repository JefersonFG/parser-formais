# -*- coding: utf-8 -*-


class Simplifications:
    """Classe que contém algoritmos de simplificação para gramáticas"""

    # print(grammar.rules)
    # saida
    # defaultdict(None, {
    # 'S': [['X', 'Y', 'Z']],
    # 'A': [['a']], 'B': [['b']],
    # 'X': [['A', 'X', 'A'], ['B', 'X', 'B'], ['Z'], ['V']],
    # 'Y': [['A', 'Y', 'B'], ['B', 'Y', 'A'], ['Z'], ['V']],
    # 'Z': [['Z', 'u'], ['Z', 'v'], ['V']]})

    def simplify(grammar):

        #print(grammar.rules.items())

        # saida
        # dict_items([(
        # 'S', [['X', 'Y', 'Z']]),
        # ('A', [['a']]),
        # ('B', [['b']]),
        # ('X', [['A', 'X', 'A'], ['B', 'X', 'B'], ['Z'], ['V']]),
        # ('Y', [['A', 'Y', 'B'], ['B', 'Y', 'A'], ['Z'], ['V']]),
        # ('Z', [['Z', 'u'], ['Z', 'v'], ['V']])])
        #return

        # Elimina símbolos inúteis nas produções (2 ETAPAS)
        # ETAPA 1 - remove produções que não geram símbolos terminais

        V1 = [] #Variaveis que geram terminais

        for origin, productions in grammar.rules.items():
            for production in productions:
                #print("origem: {} producoes: {}".format(origin, production))
                for terminal in grammar.terminals: #passa por todos os terminais
                    if terminal in production and origin not in V1:
                        V1.append(origin)

        print("V1: {}".format(V1)) #variaveis que geram terminais diretamente

        for origin, productions in grammar.rules.items():
            for production in productions:
                for variable in V1:
                    if variable in production and origin not in V1: # se alguma variavel de V1 estiver nas produções, a origem dessas produções será adicionada à V1 (Se já não estiver)
                        V1.append(origin)

        print("V1: {}".format(V1))

        grammar.variables = V1

        #ETAPA 2 - Verificação do que é atingível a partir da Variável inicial (S), as variáveis atingíveis são adicionadas à V2
        # e terminais atingíveis são adicionados à T2
        T2 = []
        V2 = ['S']

        for start in V2: #variavel de onde vai partir
            for start, productions in grammar.rules.items(): #ve as produções da variavel
                for production in productions:
                    for variable in grammar.variables:
                        if variable in productions: # se tiver alguma variavel nas produções, então ela é atingível
                            V2.append(variable)
                        #tambem deve-se adicionar os terminais dessa produção
                        for terminal in grammar.terminals:
                            T2.append(terminal)


        grammar.terminals = T2
        grammar.variables = V2

        # Eliminação de Produções vazias (3 ETAPAS)

        # ETAPA 1 -
        '''
        for origin, productions in grammar.rules.items():
            for production in productions:
                #print("origem: {} producoes: {}".format(origin, production))
                    if 'V' in production and len(production) > 1:
                        #elimina apenas V
                        production = production.remove('V')
                    elif 'V' in production and len(production) == 1:
                        #elimina a produção, pois ela produz apenas vazio
                        del production #assim que se remove uma produção?
                        continue #encerra o laço pois não é possível testar mais nada na produção atual
        '''
        #forma do livro

        Ve = []  #conjunto de variáveis que geram o vazio de forma direta ou indireta

        for origin, productions in grammar.rules.items():
            for production in productions:
                if 'V' in production:
                    Ve.append(origin) #adiciona todas as variáveis que produzem vazio à Ve

        for origin, productions in grammar.rules.items():
            for production in productions:
                for emptyVar in Ve:
                    if emptyVar in production:
                        Ve.append(origin) #gera indiretamente o vazio

        # ETAPA 2

        P1 = {} #todas as produções que nao geram vazio

        for origin, productions in grammar.rules.items():
            for production in productions:
                if 'V' not in production:
                    P1.update({origin:production})  # adiciona todas as produções que não tem vazio do lado direito à P1

        for origin, productions in P1.items():
            for production in productions:
                for emptyVar in Ve:
                    if emptyVar in P1:
                        P1.update({origin: production.remove(emptyVar)}) #adiciona produção que antes tinha Y =>+ V, aYa|aa



        # ETAPA 3
        if len(Ve) > 0:
            P2 = P1
            P2.update({'S': 'V'})  # adiciona a produção vazia, caso ela faça parte da linguagem


        return grammar