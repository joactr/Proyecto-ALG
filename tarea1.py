import numpy as np


def dp_levenshtein_backwards(x, y):
    tam_x = len(x) + 1
    tam_y = len(y) + 1 
    
    vector1 = [(n) for n in range(tam_y)]
    vector2 = [(1) for k in range(tam_y)]
    
    for i in range(1, tam_x):
        for j in range(1, tam_y):
            k = j
            if x[i - 1] == y[j - 1]:
                vector2[j] = min(
                    vector1[k] + 1,
                    vector1[k-1],
                    vector2[j-1] + 1
                )
            else:
                vector2[j] = min(
                    vector1[k] + 1,
                    vector1[k-1] + 1,
                    vector2[j-1] + 1
                )
            k += 1
        vector1 = vector2
        vector2 = [(i + 1) for n in range(tam_y)]
    return vector1[tam_y - 1]


def dp_restricted_damerau_backwards(x, y):
    return 0 # reemplazar/completar si

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