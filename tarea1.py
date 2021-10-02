import numpy as np


def dp_levenshtein_backwards(x, y):
    tam_x = len(x) + 1
    tam_y = len(y) + 1 
    
    pre = [(n) for n in range(tam_y)]
    current = [(1) for k in range(tam_y)]
    
    for i in range(1, tam_x):
        for j in range(1, tam_y):
            k = j
            if x[i - 1] == y[j - 1]:
                current[j] = min(
                    pre[k] + 1,
                    pre[k-1],
                    current[j-1] + 1
                )
            else:
                current[j] = min(
                    pre[k] + 1,
                    pre[k-1] + 1,
                    current[j-1] + 1
                )
            k += 1
        pre = current
        current = [(i + 1) for n in range(tam_y)]
    return pre[tam_y - 1]


def dp_restricted_damerau_backwards(x, y):
    tam_x = len(x) + 1
    tam_y = len(y) + 1
    
    prev2 = [(n) for n in range(tam_y)]
    prev1 = [(1) for k in range(tam_y)]
    current = [(1) for k in range(tam_y)]

    for i in range(1, tam_y):
        if x[0] == y[i-1]:
            prev1[i] = min(
                prev2[i] + 1,
                prev2[i-1],
                prev1[i-1] + 1
            )
        else:
            prev1[i] = min(
                prev2[i] + 1,
                prev2[i-1] + 1,
                prev1[i-1] + 1
            )

    if (len(x) > 1):
        for i in range(1, tam_x):
            for j in range(1, tam_y):
                k = j
                if x[i - 1] == y[j - 1]:
                    current[j] = min(
                        prev2[k] + 1,
                        prev2[k-1],
                        prev1[j-1] + 1
                    )
                else:
                    current[j] = min(
                        prev2[k] + 1,
                        prev2[k-1] + 1,
                        prev1[j-1] + 1
                    )
                k += 1
            print(prev2)
            prev2 = prev1
            prev1 = current
            current = [(i + 1) for n in range(tam_y)]

    print(prev2)
    print(prev1)
    return prev1[tam_y - 1]


    return 0 # reemplazar/completar

def dp_intermediate_damerau_backwards(x, y):
    i = len(x)
    j = len(y) 

    if i == j == 0:
        return 0
        
    else:
        select_min = []
        if i > 0:
            select_min.append(dp_intermediate_damerau_backwards(x[:-1], y) + 1)
        if j > 0:
            select_min.append(dp_intermediate_damerau_backwards(x, y[:-1]) + 1)
        
        if i > 0 and j > 0:
            if x[-1] == y[-1]:
                select_min.append(dp_intermediate_damerau_backwards(x[:-1], y[:-1]))
            else:
                select_min.append(dp_intermediate_damerau_backwards(x[:-1], y[:-1]) + 1)
        
        if i > 1 and j > 1 and x[-2] == y[-1] and x[-1] == y[-2]:
            select_min.append(dp_intermediate_damerau_backwards(x[:-2], x[:-2] + 1))

        return min(select_min)
        
                    
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