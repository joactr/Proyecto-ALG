
import numpy as np


def dp_levenshtein_backwards(x, y):
    """
    Se permite insertar, borrar y sustituir
    """
    tam_x = len(x) + 1
    tam_y = len(y) + 1 
    
    pre = [(n) for n in range(tam_y)]
    current = [(1) for k in range(tam_y)]
    
    for i in range(1, tam_x):
        for j in range(1, tam_y):
            k = j
            current[j] = min(
                pre[k] + 1, #borrado
                pre[k-1] if x[i - 1] == y[j - 1] else  pre[k-1] + 1, #sustitucion
                current[j-1] + 1 #insercion
            )
            k += 1
        pre = current
        current = [(i + 1) for n in range(tam_y)]
    return pre[tam_y - 1]


def dp_restricted_damerau_backwards(x, y):
    """
    Se permite insertar, borrar, sustituir e intercambiar, pero tras intercambiar no se puede operar con esos símbolos
    """
    tam_x = len(x) + 1
    tam_y = len(y) + 1
    prev2 = [(n) for n in range(tam_y)]
    prev1 = [(1) for k in range(tam_y)]
    current = [(2) for k in range(tam_y)]
    if(len(x) >= 1):
        for i in range(1, tam_y):
            prev1[i] = min(
                prev2[i] + 1,
                prev2[i-1] if x[0] == y[i-1] else prev2[i-1] + 1, #sustitucion
                prev1[i-1] + 1
            )
    else: return len(y)
    if (len(x) > 1 and len(y) > 1):
        for i in range(2, tam_x):
            for j in range(1, tam_y):
                current[j] = min(
                    prev1[j] + 1,
                    prev1[j-1] if x[i - 1] == y[j - 1] else prev1[j-1] + 1, #sustitucion
                    current[j-1] + 1, 
                    prev2[j - 2] + 1 if x[i - 2] == y[j - 1] and x[i - 1] == y[j - 2] else float("inf") #intercambio
                )
                
            prev2, prev1 = prev1, current
            current = [(i + 1) for n in range(tam_y)]

    return prev1[tam_y - 1]
    

def dp_intermediate_damerau_backwards(x, y):
    """
    Se permite insertar, borrar, sustituir e intercambiar, y tras el intercambio podemos realizar edición tal que:
        ab ↔ ba coste 1
        acb ↔ ba coste 2
        ab ↔ bca coste 2
    """
    tam_x = len(x) + 1
    tam_y = len(y) + 1
    prev3 = [(n) for n in range(tam_y)]
    prev2 = [(1) for n in range(tam_y)]
    prev1 = [(2) for k in range(tam_y)]
    current = [(3) for k in range(tam_y)]

    for i in range(1, tam_y):
        if x[0] == y[i-1]:
            prev2[i] = min(
                prev3[i] + 1,
                prev3[i-1],
                prev2[i-1] + 1
            )
        else:
            prev2[i] = min(
                prev3[i] + 1,
                prev3[i-1] + 1,
                prev2[i-1] + 1
            )

    if (len(y) > 1 and len(x) > 1):
        for j in range(1, tam_y):
                prev1[j] = min(
                    prev2[j] + 1,
                    prev2[j - 1] if x[1] == y[j - 1] else prev2[j - 1] + 1,
                    prev1[j - 1] + 1,
                    prev3[j - 2] + 1 if x[0] == y[j - 1] and x[1] == y[j - 2] else float("inf") #intercambio
                )
            
    for i in range(3, tam_x):
        for j in range(1, tam_y):
            current[j] = min(
                    prev1[j] + 1,
                    prev1[j - 1] if x[i - 1] == y[j - 1] else prev1[j - 1] + 1,
                    current[j - 1] + 1,
                    prev2[j - 3] + 2 if j > 2 and x[i - 2] == y[j - 1] and x[i - 1] == y[j - 3] else float("inf"),
                    prev2[j - 2] + 1 if j > 1 and x[i - 2] == y[j - 1] and x[i - 1] == y[j - 2] else float("inf"),
                    prev3[j - 2] + 2 if j > 1 and x[i - 3] == y[j - 1] and x[i - 1] == y[j - 2] else float("inf")
                )

        prev3 = prev2
        prev2 = prev1
        prev1 = current
        current = [(i+1) for _ in range(tam_y)]
    
    return prev1[tam_y - 1]
        
                    
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