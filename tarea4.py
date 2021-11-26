import numpy as np
from trie import Trie

def dp_levenshtein_trie(x, trie, th):
    """
    Encuentra la distancia de edición de Levenshtein entre dos cadenas x e y
    Los resultados devueltos están limitados a una distancia de edición th
    Hace uso de la estructura de datos trie (árbol de prefijos)
    """
    if th == None: th = float("inf")
    results = {}
    states = trie.get_num_states()
    tam_x = len(x)
    current = np.zeros(states)
    pre = np.zeros(states)

    #Recorremos todos los nodos del trie y asignamos un coste a cada prefijo
    for i in range(1, states): 
        current[i]= current[trie.get_parent(i)] + 1

    #Vamos recorriendo las letras de la palabra x
    for i in range(1, tam_x + 1):
        pre[0] = i
        #Para cada letra cogemos la operación de coste mínimo
        for j in range(1,states) :
            pre[j] = min(current[j] + 1, #insercion
                        pre[trie.get_parent(j)] + 1, #borrado
                        current[trie.get_parent(j)] if x[i-1] == trie.get_label(j) else current[trie.get_parent(j)] + 1 #sustitucion
            )

        if min(pre) > th: return {} #Si supera el threshold salimos
        current, pre = pre, current

    #Recorremos todos los estados, si son finales y menores que el threshold añadimos a result
    for i in range(states):
        if trie.is_final(i):
            if current[i] <= th: results[trie.get_output(i)] = current[i]

    return results

def dp_restricted_damerau_trie(x, trie, th):
    d = np.zeros((trie.get_num_states() + 1, len(x) + 1))
    results = {}

    for i in range(1, trie.get_num_states() + 1):
        d[i, 0] = d[trie.get_parent(i), 0] + 1

    for j in range(1, len(x) + 1):
        d[0, j] = d[0, j - 1] + 1

        for i in range(1, trie.get_num_states() + 1):
            d[i, j] = min(
                d[trie.get_parent(i), j] + 1,
                d[i, j - 1] + 1,
                d[trie.get_parent(i), j - 1] + (trie.get_label(i) != x[j - 1])
            )

            if i > 1 and j > 1 and x[j - 2] == trie.get_label(i) and x[j - 1] == trie.get_label(
                    trie.get_parent(i)):
                d[i, j] = min(
                    d[i, j],
                    d[trie.get_parent(trie.get_parent(i)), j - 2] + 1
                )

        if (min(d[:, j]) > th):
            return th + 1

    for i in range(trie.get_num_states()):
        if trie.is_final(i):
            if d[i, len(x)] <= th: results[trie.get_output(i)] = d[i, len(x)]
    return results

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