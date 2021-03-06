

def dp_levenshtein_threshold(x, y, th):
    """
    Se permite insertar, borrar y sustituir
    Consta de un threshold que limita los resultados obtenidos a una distancia de edición (th)
    """
    tam_x = len(x) + 1
    tam_y = len(y) + 1 
    
    pre = [(n) for n in range(tam_y)] #Se puede usar np.arrange(...)
    current = [(1) for k in range(tam_y)]
    
    for i in range(1, tam_x):
        for j in range(1, tam_y):
            k = j
            current[j] = min(
                pre[k] + 1, 
                pre[k-1] if x[i - 1] == y[j - 1] else  pre[k-1] + 1, #sustitucion
                current[j-1] + 1
            )
            k += 1
            if (min(pre) > th): 
                return th + 1
        pre = current
        current = [(i + 1) for n in range(tam_y)]
    return pre[tam_y - 1]


def dp_restricted_damerau_threshold(x, y, th):
    """
    Se permite insertar, borrar, sustituir e intercambiar, pero tras intercambiar no se puede operar con esos símbolos
    Consta de un threshold que limita los resultados obtenidos a una distancia de edición (th)
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

    if(min(prev1)> th): return th + 1
    for i in range(2, tam_x):
        for j in range(1, tam_y):
            current[j] = min(
                prev1[j] + 1,
                prev1[j-1] if x[i - 1] == y[j - 1] else prev1[j-1] + 1, #sustitucion
                current[j-1] + 1, 
                prev2[j - 2] + 1 if x[i - 1] == y[j - 2] and y[j - 1] == x[i - 2] else float("inf")
            )
            if (min(prev1) > th): 
                return th + 1
            
        prev2, prev1 = prev1, current
        current = [(i + 1) for n in range(tam_y)]

    return prev1[tam_y - 1]

def dp_intermediate_damerau_threshold(x, y, th):
    """
    Se permite insertar, borrar, sustituir e intercambiar, y tras el intercambio podemos realizar edición tal que:
        ab ↔ ba coste 1
        acb ↔ ba coste 2
        ab ↔ bca coste 2

    Consta de un threshold que limita los resultados obtenidos a una distancia de edición (th)
    """
    tam_x = len(x) + 1
    tam_y = len(y) + 1
    prev3 = [(n) for n in range(tam_y)]
    prev2 = [(1) for n in range(tam_y)]
    prev1 = [(2) for k in range(tam_y)]
    current = [(3) for k in range(tam_y)]

    if (len(x) > 0):
        for i in range(1, tam_y):
            prev2[i] = min(
                prev3[i] + 1,
                prev3[i-1] if x[0] == y[i-1] else prev3[i-1] + 1,
                prev2[i-1] + 1
            )
        if(min(prev2) > th): return th + 1
    else: return len(y)

    if (len(x) > 1):
        for j in range(1, tam_y):
            prev1[j] = min(
                prev2[j] + 1,
                prev2[j - 1] if x[1] == y[j - 1] else prev2[j - 1] + 1,
                prev1[j - 1] + 1,
                prev3[j - 2] + 1 if j > 1 and x[0] == y[j - 1] and x[1] == y[j - 2] else float("inf"),
                prev3[j - 3] + 2 if j > 2 and x[0] == y[j - 1] and x[1] == y[j - 3] else float("inf")
            )
        if(min(prev1) > th): return th + 1
    else: return len(y) - (1 if x[0]==y[0] else 0)
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
        if (min(prev1) > th): return th + 1

        prev3 = prev2
        prev2 = prev1
        prev1 = current
        current = [(i+1) for _ in range(tam_y)]
    
    return prev1[tam_y - 1]

test = [
        ("algoritmo","algortimo"),
        ("algoritmo","algortximo"),
        ("algoritmo","lagortimo"),
        ("algoritmo","agaloritom"),
        ("algoritmo","algormio"),
        ("acb","ba")
        ]

thrs = range(1,4)

for threshold in thrs:
    """"
    print(f"thresholds: {threshold:3}")
    for x,y in test:
        print(f"{x:12} {y:12} \t",end="")
        for dist,name in ((dp_levenshtein_threshold,"levenshtein"),
                          (dp_restricted_damerau_threshold,"restricted"),
                          (dp_intermediate_damerau_threshold,"intermediate")):
        
            print(f" {name} {dist(x,y,threshold):2}",end="")
        print()
"""
"""
Salida del programa:

thresholds:   1
algoritmo    algortimo    	 levenshtein  2 restricted  1 intermediate  1
algoritmo    algortximo   	 levenshtein  2 restricted  2 intermediate  2
algoritmo    lagortimo    	 levenshtein  2 restricted  2 intermediate  2
algoritmo    agaloritom   	 levenshtein  2 restricted  2 intermediate  2
algoritmo    algormio     	 levenshtein  2 restricted  2 intermediate  2
acb          ba           	 levenshtein  2 restricted  2 intermediate  2
thresholds:   2
algoritmo    algortimo    	 levenshtein  2 restricted  1 intermediate  1
algoritmo    algortximo   	 levenshtein  3 restricted  3 intermediate  2
algoritmo    lagortimo    	 levenshtein  3 restricted  2 intermediate  2
algoritmo    agaloritom   	 levenshtein  3 restricted  3 intermediate  3
algoritmo    algormio     	 levenshtein  3 restricted  3 intermediate  2
acb          ba           	 levenshtein  3 restricted  3 intermediate  2
thresholds:   3
algoritmo    algortimo    	 levenshtein  2 restricted  1 intermediate  1
algoritmo    algortximo   	 levenshtein  3 restricted  3 intermediate  2
algoritmo    lagortimo    	 levenshtein  4 restricted  2 intermediate  2
algoritmo    agaloritom   	 levenshtein  4 restricted  4 intermediate  3
algoritmo    algormio     	 levenshtein  3 restricted  3 intermediate  2
acb          ba           	 levenshtein  3 restricted  3 intermediate  2
"""         