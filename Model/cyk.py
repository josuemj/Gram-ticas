#Este modulo se encarga de realizar el algoritmo de CYK, ingresando la gramática en CNF y la oración a evaluar. Retorna SI o No dependiendo si la oración pertenece a la gramática ingresada.
import itertools
import matplotlib.pyplot as plt

def piramide(n, rows, variables, rules, table):
    for j in range(n - rows):  # j va de 0 a n-2 para la tercera fila
        vertical = []
        diagonal = []
        cartesian_products = []

        for i in range(rows):
            vertical.append(table[i][j])
            if j + i + (rows - 1) <= (n+1):  # Verificar que no exceda el límite de la tabla
                diagonal.append(table[(rows - 1) - i][j + i + 1]) 
            product = [''.join(pair) for pair in itertools.product(vertical[i], diagonal[i])]
            cartesian_products.extend(product)
                
        for rule in rules:
            for variable in variables:
                if variable == ''.join(rule.keys()):
                    for production in rule[variable]:
                        if len(production) == 2:
                            for c_product in cartesian_products:  # Verifica cada producto cartesiano
                                if production[0] + production[1] == c_product:
                                    table[rows][j].add(variable)

def CYK(grammar, sentence):
    # Longitud de la oración
    n = len(sentence)
    
    if n == 0:
        return False
    
    variables = grammar["variables"]
    terminals = grammar["terminals"]
    rules = grammar["rules"]
    
    # Inicialización de la tabla CYK: una tabla de (n x n) de sets vacíos
    table = [[set() for _ in range(n)] for _ in range(n)]

    # Etapa 1: Llenar la tabla para las producciones de una sola palabra (terminales)
    for i, word in enumerate(sentence):
        for rule in rules:
            for variable in variables:
                if variable == ''.join(rule.keys()):
                    if word in rule[variable]:
                        table[0][i].add(variable)

    # Etapa 2: producto cartesiano para llenar la segunda fila de la tabla
    for j in range(n - 1):
        for k in range(1):
            for rule in rules:
                for variable in variables:
                    if variable == ''.join(rule.keys()):
                        for production in rule[variable]:
                            if len(production) == 2:
                                if production[0] in table[k][j] and production[1] in table[0][j + k + 1]:
                                    table[1][j].add(variable)
    
    # Etapa 3: Llenar la tercera fila (table[2]) usando producto cartesiano
    for i in range(2, n):
        piramide(n, i, variables, rules, table)
        
    
    # La oración pertenece al lenguaje si el símbolo inicial (S) está en la posición superior derecha de la tabla
    return 'S' in table[n-1][0]