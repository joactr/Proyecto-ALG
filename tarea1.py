import numpy as np


def dp_levenshtein_backwards(x, y):
    tam_x = len(x) + 1
    tam_y = len(y) + 1

    matriz = np.zeros ((tam_x, tam_y))

    for x1 in range(tam_x):
        matriz[x1, 0] = x1
    for y1 in range(tam_y):
        matriz[0, y1] = y1
    
    for s1 in range(1, tam_x):
        for s2 in range(1, tam_y):
            if x[s1 - 1] == y[s2 - 1]:
                matriz[s1,s2] = min(
                    matriz[s1-1,s2] + 1,
                    matriz[s1-1,s2-1],
                    matriz[s1,s2-1] + 1
                )
            else:
                matriz[s1,s2]=min(
                    matriz[s1-1,s2] + 1,
                    matriz[s1-1,s2-1] + 1,
                    matriz[s1,s2-1] + 1
                )

    return matriz[tam_x - 1, tam_y - 1]

def dp_restricted_damerau_backwards(x, y):
    return 0 # reemplazar/completar

def dp_intermediate_damerau_backwards(x, y):
    return 0 # reemplazar/completar

test = [("algoritmo","algortimo"),
        ("algoritmo","algortximo"),
        ("algoritmo","lagortimo"),
        ("algoritmo","agaloritom"),
        ("algoritmo","algormio"),
        ("acb","ba")]

for x,y in test:
    print(f"{x:12} {y:12}",end="")
    for dist,name in ((dp_levenshtein_backwards,"levenshtein"),
                      (dp_restricted_damerau_backwards,"restricted"),
                      (dp_intermediate_damerau_backwards,"intermediate")):
        print(f" {name} {dist(x,y):2}",end="")
    print()
                 
"""
Salida del programa:
algoritmo    algortimo    levenshtein  2 restricted  1 intermediate  1
algoritmo    algortximo   levenshtein  3 restricted  3 intermediate  2
algoritmo    lagortimo    levenshtein  4 restricted  2 intermediate  2
algoritmo    agaloritom   levenshtein  5 restricted  4 intermediate  3
algoritmo    algormio     levenshtein  3 restricted  3 intermediate  2
acb          ba           levenshtein  3 restricted  3 intermediate  2
"""         