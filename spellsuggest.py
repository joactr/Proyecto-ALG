# -*- coding: utf-8 -*-
from os import error
import re
import tarea2
from trie import Trie
import json
import numpy as np

class SpellSuggester:

    """
    Clase que implementa el mÃ©todo suggest para la bÃºsqueda de tÃ©rminos.
    """

    def __init__(self, vocab_file_path=None,vocab=None):
        """MÃ©todo constructor de la clase SpellSuggester

        Construye una lista de tÃ©rminos Ãºnicos (vocabulario),
        que ademÃ¡s se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
        """
        if vocab_file_path is None and vocab is not None: #Usamos lista para constructor
            self.vocabulary  = self.build_vocab_list(vocab)
        elif vocab is None and vocab_file_path is not None: #Usamos fichero como constructor
            self.vocabulary  = self.build_vocab_file(vocab_file_path, tokenizer=re.compile("\W+"))
        else:
            raise Exception("Error")

    def build_vocab_file(self, vocab_file_path, tokenizer):
        """MÃ©todo para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresiÃ³n regular para la tokenizaciÃ³n.
        """
        with open(vocab_file_path, "r", encoding='utf-8') as fr:
            vocab = set(tokenizer.split(fr.read().lower()))
            vocab.discard('') # por si acaso
            return sorted(vocab)

    def build_vocab_list(self, vocab):
        """MÃ©todo para crear el vocabulario.

        Coge una lista dada de vocabulario y crea el spellsugester

        Args:
            vocab (lista): lista de palabras ya tokenizadas
        """
        vocab = set(vocab)
        vocab.discard('') # por si acaso
        return sorted(vocab)
    
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

        """Metodo para sugerir palabras similares siguiendo la tarea 3.

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
            # Si la diferencia de tamaño es mayor al treshold, el termino no se tiene en cuenta o si la cota optimista es mayor
            if abs(len(term) - len(term_voc)) > threshold or cota(term,term_voc) > threshold:
                dist = float("inf")
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
    Clase que implementa el metodo suggest para la busqueda de terminos y añade el trie
    """
    def __init__(self, vocab_file_path=None, vocab=None):
        super().__init__(vocab_file_path, vocab)
        self.trie = Trie(self.vocabulary)

    def suggest(self, term, distance="levenshtein", threshold=None):
        if distance == "levenshtein":
            if threshold == None: threshold = float("inf")
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

                if min(pre) > threshold: return {} #Si supera el threshold salimos
                current, pre = pre, current

            #Recorremos todos los estados, si son finales y menores que el threshold añadimos a result
            for i in range(states):
                if self.trie.is_final(i):
                    if current[i] <= threshold: results[self.trie.get_output(i)] = current[i]

            return results

        elif distance == "restricted":
            x = term
            d = np.zeros((self.trie.get_num_states() + 1, len(x) + 1))
            results = {}


            for i in range(1, self.trie.get_num_states() + 1):
                d[i, 0] = d[self.trie.get_parent(i), 0] + 1

            for j in range(1, len(x) + 1):
                d[0, j] = d[0, j - 1] + 1

                for i in range(1, self.trie.get_num_states() + 1):
                    d[i, j] = min(
                        d[self.trie.get_parent(i), j] + 1,
                        d[i, j - 1] + 1,
                        d[self.trie.get_parent(i), j - 1] + (self.trie.get_label(i) != x[j - 1])
                    )

                    if i > 1 and j > 1 and x[j - 2] == self.trie.get_label(i) and x[j - 1] == self.trie.get_label(
                            self.trie.get_parent(i)):
                        d[i, j] = min(
                            d[i, j],
                            d[self.trie.get_parent(self.trie.get_parent(i)), j - 2] + 1
                        )

                if (min(d[:, j]) > threshold):
                    return threshold + 1

            for i in range(self.trie.get_num_states()):
                if self.trie.is_final(i):
                    if d[i, len(x)] <= threshold: results[self.trie.get_output(i)] = d[i, len(x)]
            return results
        else:
            print("Distancia Damerau-Levenshtein intermedia no implementada con trie")
            return {}

if __name__ == "__main__":

    spellsuggester = SpellSuggester("./corpora/quijote.txt")
    #for distance in ['levenshtein','restricted','intermediate']:
    """for distance in ['intermediate']:  
        destiny =  f'result_{distance}_quijote.txt'
        with open(destiny, "w", encoding='utf-8') as fw:
            for palabra in ("casa", "senor", "jabón", "constitución", "ancho",
                            "savaedra", "vicios", "quixot", "s3afg4ew"):
                for threshold in range(1, 6):
                    resul = spellsuggester.suggest(palabra,distance=distance,threshold=threshold)
                    numresul = len(resul)
                    resul = " ".join(sorted(f'{v}:{k}' for k,v in resul.items()))
                    fw.write(f'{palabra}\t{threshold}\t{numresul}\t{resul}\n')"""
                    
    spellsuggester = TrieSpellSuggester("./corpora/quijote.txt")
    print(spellsuggester.suggest("alábese"))
    # cuidado, la salida es enorme print(suggester.trie)

    