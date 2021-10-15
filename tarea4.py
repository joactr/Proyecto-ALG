import numpy as np
from trie import Trie

def dp_levenshtein_trie(x, trie, th):
    """
    COMENTAR IGUAL QUE SAR Y ALGUN COMENTARIO DE LINEA
    """
    results = {}
    if th == None: th = float("inf")
    states = trie.get_num_states()
    tam_x = len(x)
    current = np.zeros(states)
    pre = np.zeros(states)

    for i in range(1, states): 
        current[i]= current[trie.get_parent(i)] + 1

    for i in range(1, tam_x + 1):
        pre[0] = i
        for j in range(1,states) :
            pre[j] = min(current[j] + 1,
                        pre[trie.get_parent(j)] + 1,
                        current[trie.get_parent(j)] if x[i-1] == trie.get_label(j) else current[trie.get_parent(j)] + 1
            )
        if min(pre) > th: return {}
        current, pre = pre, current

    for i in range(states):
        if trie.is_final(i):
            if current[i] <= th: results[trie.get_output(i)] = current[i]

    return results

def dp_restricted_damerau_trie(x, trie, th):
    # TODO
    return []

def dp_intermediate_damerau_trie(x, trie, th):
    # TODO
    return []


words = ["algortimo", "algortximo","lagortimo", "agaloritom", "algormio", "ba"]
words.sort()
trie = Trie(words)

test = ["algoritmo", "acb"]
thrs = range(1, 4)

for threshold in thrs:
    print(f"threshols: {threshold:3}")
    for x in test:
        for dist,name in (
                    (dp_levenshtein_trie,"levenshtein"),
                    (dp_restricted_damerau_trie,"restricted"),
                    (dp_intermediate_damerau_trie,"intermediate"),
                    ):
            print(f"\t{x:12} \t{name}\t", end="")
            print(dist(x, trie, threshold))
                 
"""
Salida del programa:

threshols:   1
	algoritmo    	levenshtein	[]
	algoritmo    	restricted	[('algortimo', 1)]
	algoritmo    	intermediate	[('algortimo', 1)]
	acb          	levenshtein	[]
	acb          	restricted	[]
	acb          	intermediate	[]
threshols:   2
	algoritmo    	levenshtein	[('algortimo', 2)]
	algoritmo    	restricted	[('algortimo', 1), ('lagortimo', 2)]
	algoritmo    	intermediate	[('algormio', 2), ('algortimo', 1), ('lagortimo', 2), ('algortximo', 2)]
	acb          	levenshtein	[]
	acb          	restricted	[]
	acb          	intermediate	[('ba', 2)]
threshols:   3
	algoritmo    	levenshtein	[('algormio', 3), ('algortimo', 2), ('algortximo', 3)]
	algoritmo    	restricted	[('algormio', 3), ('algortimo', 1), ('lagortimo', 2), ('algortximo', 3)]
	algoritmo    	intermediate	[('algormio', 2), ('algortimo', 1), ('lagortimo', 2), ('agaloritom', 3), ('algortximo', 2)]
	acb          	levenshtein	[('ba', 3)]
	acb          	restricted	[('ba', 3)]
	acb          	intermediate	[('ba', 2)]

"""         