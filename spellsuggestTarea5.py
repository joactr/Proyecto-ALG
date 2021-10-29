# -*- coding: utf-8 -*-
import re
import tarea2 
from trie import Trie
import numpy as np
from time import process_time
from collections import Counter


class SpellSuggester:

    """
    Clase que implementa el mÃ©todo suggest para la bÃºsqueda de tÃ©rminos.
    """

    def __init__(self, vocab_file_path, tam_vocab):
        """MÃ©todo constructor de la clase SpellSuggester

        Construye una lista de tÃ©rminos Ãºnicos (vocabulario),
        que ademÃ¡s se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tam_vocab (int): número de palabras que deseamos que tenga el vocabulario
        """

        self.vocabulary  = self.build_vocab(vocab_file_path, tam_vocab, tokenizer=re.compile("\W+"))

    def build_vocab(self, vocab_file_path, tam_vocab, tokenizer):
        """MÃ©todo para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se devuelven las primeras
        "tam_vocab" palabras por frecuencia de aparición ordenadas
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tam_vocab (int): número máximo de palabras que deseamos en el vocabulario
            tokenizer (re.Pattern): expresiÃ³n regular para la tokenizaciÃ³n.
        """
        with open(vocab_file_path, "r", encoding='utf-8') as fr:
            #Usamos un counter en vez de un set para poder contar el número de apariciones por palabra
            count = Counter(tokenizer.split(fr.read().lower()))
            if '' in count:
                del count[''] #Por si acaso
            reversed_count = [(freq, word) for (word,freq) in count.items()]
            sorted_reversed = sorted(reversed_count, reverse=True)
            sorted_vocab = [word for (freq,word) in sorted_reversed]
            return sorted(sorted_vocab[0:tam_vocab])

    
    def cota(self, x, y):
        """
            Metodo que devuelve un threshold en base a la comparacion de vectores de ocurrencias.
            Args
            x (str): primer termino a comparar
            y (str): segundo termino a comparar
        """
        # Crear vectores de ocurrencias
        letters = list(set(x).union(set(y)))    
        vx = [x.count(l) for l in letters]
        vy = [y.count(l) for l in letters]

        v_dif = [x - y for x, y in zip(vx, vy)]

        return max(sum(np.array([x for x in v_dif if x > 0 ])), sum(np.array([-x for x in v_dif if x < 0])))

    def suggest(self, term, distance="levenshtein", threshold=None):

        """MÃ©todo para sugerir palabras similares siguiendo la tarea 3.

        A completar.

        Args:
            term (str): tÃ©rmino de bÃºsqueda.
            distance (str): algoritmo de bÃºsqueda a utilizar
                {"levenshtein", "restricted", "intermediate"}.
            threshold (int): threshold para limitar la bÃºsqueda
                puede utilizarse con los algoritmos de distancia mejorada de la tarea 2
                o filtrando la salida de las distancias de la tarea 2
        """
        assert distance in ["levenshtein", "restricted", "intermediate"]
    
        results = {} # diccionario termino:distancia
        if threshold==None: threshold = float("inf")

        for term_voc in self.vocabulary:
            if abs(len(term) - len(term_voc)) > threshold:  # Si la diferencia de tamaño es mayor al treshold, el termino no se tiene en cuenta
                dist = threshold + 8
            if distance == 'levenshtein':
                dist = tarea2.dp_levenshtein_threshold(term, term_voc, threshold)
            elif distance == 'restricted':
                dist = tarea2.dp_restricted_damerau_threshold(term, term_voc, threshold)
            else:
                dist = tarea2.dp_intermediate_damerau_threshold(term, term_voc, threshold)
            
            if dist <= threshold:
                results[term_voc] = dist

        return results

class TrieSpellSuggester(SpellSuggester):
    """
    Clase que implementa el mÃ©todo suggest para la bÃºsqueda de tÃ©rminos y aÃ±ade el trie
    """
    def __init__(self, vocab_file_path,tam_vocab):
        super().__init__(vocab_file_path,tam_vocab)
        self.trie = Trie(self.vocabulary)

    def suggest(self, term, distance="levenshtein", th=None):
        if th == None: th = float("inf")
        results = {}
        states = self.trie.get_num_states()
        tam_x = len(term)
        current = np.zeros(states)
        pre = np.zeros(states)

        #Recorremos todos los nodos del trie y asignamos un coste a cada prefijo
        for i in range(1, states): 
            current[i]= current[self.trie.get_parent(i)] + 1

        #Vamos recorriendo las letras de la palabra x
        for i in range(1, tam_x + 1):
            pre[0] = i
            #Para cada letra cogemos la operación de coste mínimo
            for j in range(1,states) :
                pre[j] = min(current[j] + 1,
                            pre[self.trie.get_parent(j)] + 1,
                            current[self.trie.get_parent(j)] if term[i-1] == self.trie.get_label(j) else current[self.trie.get_parent(j)] + 1
                )

            if min(pre) > th: return {} #Si supera el threshold salimos
            current, pre = pre, current

        #Recorremos todos los estados, si son finales y menores que el threshold añadimos a result
        for i in range(states):
            if self.trie.is_final(i):
                if current[i] <= th: results[self.trie.get_output(i)] = current[i]

        return results

if __name__ == "__main__":

    tams_vocab = [1000,5000,10000,25000] #En total tiene 22942 palabras distintas el vocabulario
    thresholds = [1,2,5,20]
    terminos = ["alábese","diferencias","conquistar","ancho","senor"]

    for size in tams_vocab:
        spellsuggester = SpellSuggester("./corpora/quijote.txt", size)
        for palabra in terminos:
            for threshold in thresholds:
                for distance in ['levenshtein','restricted','intermediate']:    
                    tstart = process_time()
                    spellsuggester.suggest(palabra,distance=distance,threshold=threshold)
                    tend = process_time() - tstart
                    print('TIME: ' + str(tend) + ' usando ' + distance + ', tamaño: ' + str(size) + ' Threshold: ' + str(threshold) + ' Palabra:' + palabra)       

    distance = "levenshtein"
    for size in tams_vocab:
        spellsuggester = TrieSpellSuggester("./corpora/quijote.txt",size)
        for palabra in terminos:
            for threshold in thresholds:
                tstart = process_time()
                spellsuggester.suggest(palabra,distance,threshold)
                tend = process_time() - tstart
                print('TIME: ' + str(tend) + ' usando Trie, tamaño: ' + str(size) + ' Threshold: ' + str(threshold) + ' Palabra:' + palabra)       

    #spellsuggester = TrieSpellSuggester("./corpora/quijote.txt")
    #print(spellsuggester.suggest("alábese"))
    # cuidado, la salida es enorme print(suggester.trie)

    
