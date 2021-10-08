def dp_levenshtein_threshold(x, y, th):
    tam_x = len(x) + 1
    tam_y = len(y) + 1 
    
    pre = [(n) for n in range(tam_y)]
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
    #TODO
    return 0

def dp_intermediate_damerau_threshold(x, y, th):
    #TODO
    return 0

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
    print(f"thresholds: {threshold:3}")
    for x,y in test:
        print(f"{x:12} {y:12} \t",end="")
        for dist,name in ((dp_levenshtein_threshold,"levenshtein"),
                          (dp_restricted_damerau_threshold,"restricted"),
                          (dp_intermediate_damerau_threshold,"intermediate")):
        
            print(f" {name} {dist(x,y,threshold):2}",end="")
        print()
                 
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