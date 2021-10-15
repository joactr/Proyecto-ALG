# -*- coding: utf-8 -*-
import re
import tarea2 
from trie import Trie
import json
import numpy as np

class SpellSuggester:

    """
    Clase que implementa el mÃ©todo suggest para la bÃºsqueda de tÃ©rminos.
    """

    def __init__(self, vocab_file_path):
        """MÃ©todo constructor de la clase SpellSuggester

        Construye una lista de tÃ©rminos Ãºnicos (vocabulario),
        que ademÃ¡s se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.

        """

        self.vocabulary  = self.build_vocab(vocab_file_path, tokenizer=re.compile("\W+"))

    def build_vocab(self, vocab_file_path, tokenizer):
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
    def __init__(self, vocab_file_path):
        super().__init__(vocab_file_path)
        self.trie = Trie(self.vocabulary)

    def suggest(self, term):


if __name__ == "__main__":

    spellsuggester = SpellSuggester("./corpora/quijote.txt")
    #for distance in ['levenshtein','restricted','intermediate']:
    for distance in ['intermediate']:  
        destiny =  f'result_{distance}_quijote.txt'
        with open(destiny, "w", encoding='utf-8') as fw:
            for palabra in ("casa", "senor", "jabón", "constitución", "ancho",
                            "savaedra", "vicios", "quixot", "s3afg4ew"):
                for threshold in range(1, 6):
                    resul = spellsuggester.suggest(palabra,distance=distance,threshold=threshold)
                    numresul = len(resul)
                    resul = " ".join(sorted(f'{v}:{k}' for k,v in resul.items()))
                    fw.write(f'{palabra}\t{threshold}\t{numresul}\t{resul}\n')
                    
    # spellsuggester = TrieSpellSuggester("./corpora/quijote.txt")
    # print(spellsuggester.suggest("alábese"))
    # cuidado, la salida es enorme print(suggester.trie)

    