#coding: utf-8
import json
from pickle import FALSE
from nltk.stem.snowball import SnowballStemmer
import os
import re

#Algoritmica
from spellsuggest import SpellSuggester 
from spellsuggest import TrieSpellSuggester


class SAR_Project:
    """
    Prototipo de la clase para realizar la indexacion y la recuperacion de noticias
        
        Preparada para todas las ampliaciones:
          parentesis + multiples indices + posicionales + stemming + permuterm + ranking de resultado

    Se deben completar los metodos que se indica.
    Se pueden añadir nuevas variables y nuevos metodos
    Los metodos que se añadan se deberan documentar en el codigo y explicar en la memoria
    """

    # lista de campos, el booleano indica si se debe tokenizar el campo
    # NECESARIO PARA LA AMPLIACION MULTIFIELD
    fields = [("title", True), ("date", False),
              ("keywords", True), ("article", True),
              ("summary", True)]
    
    
    # numero maximo de documento a mostrar cuando self.show_all es False
    SHOW_MAX = 100


    def __init__(self):
        """
        Constructor de la classe SAR_Indexer.
        NECESARIO PARA LA VERSION MINIMA

        Incluye todas las variables necesaria para todas las ampliaciones.
        Puedes añadir más variables si las necesitas 

        """
        self.index = {} # hash para el indice invertido de terminos --> clave: termino, valor: posting list.
                        # Si se hace la implementacion multifield, se pude hacer un segundo nivel de hashing de tal forma que:
                        # self.index['title'] seria el indice invertido del campo 'title'.
        self.stemmindex = {} # hash para el índice invertido de stems --> clave: stem, valor: posting list.
        self.sindex = {} # hash para el indice invertido de stems --> clave: stem, valor: lista con los terminos que tienen ese stem
        self.ptindex = {} # hash para el indice permuterm.
        self.docs = {} # diccionario de documentos --> clave: entero(docid),  valor: ruta del fichero.
        self.weight = {} # hash de terminos para el pesado, ranking de resultados. puede no utilizarse
        self.news = {} # hash de noticias --> clave entero (newid), valor: la info necesaria para diferenciar la noticia dentro de su fichero (doc_id y posición dentro del documento)
        self.tokenizer = re.compile("\W+") # expresion regular para hacer la tokenizacion
        self.stemmer = SnowballStemmer('spanish') # stemmer en castellano
        self.show_all = False # valor por defecto, se cambia con self.set_showall()
        self.show_snippet = False # valor por defecto, se cambia con self.set_snippet()
        self.use_stemming = False # valor por defecto, se cambia con self.set_stemming()
        self.use_ranking = False  # valor por defecto, se cambia con self.set_ranking()
        self.tam_not = {} # hash que indica el tamaño en tokens de cada noticia, clave: termino, noticia: num_tokens

        #Variable añadida en Algoritmica
        self.use_approximation = False # indica si se usará aproximación de terminos por distancias, se cambia con self.set_approximation()

        self.IdDoc = 0 # numero de documento (archivo .json)
        self.newid = 0 # numero de noticia
      
    ###############################
    ###                         ###
    ###      CONFIGURACION      ###
    ###                         ###
    ###############################


    def set_showall(self, v):
        """

        Cambia el modo de mostrar los resultados.
        
        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_all es True se mostraran todos los resultados el lugar de un maximo de self.SHOW_MAX, no aplicable a la opcion -C

        """
        self.show_all = v


    def set_snippet(self, v):
        """

        Cambia el modo de mostrar snippet.
        
        input: "v" booleano.

        UTIL PARA TODAS LAS VERSIONES

        si self.show_snippet es True se mostrara un snippet de cada noticia, no aplicable a la opcion -C

        """
        self.show_snippet = v


    def set_stemming(self, v):
        """

        Cambia el modo de stemming por defecto.
        
        input: "v" booleano.

        UTIL PARA LA VERSION CON STEMMING

        si self.use_stemming es True las consultas se resolveran aplicando stemming por defecto.

        """
        self.use_stemming = v


    def set_ranking(self, v):
        """

        Cambia el modo de ranking por defecto.
        
        input: "v" booleano.

        UTIL PARA LA VERSION CON RANKING DE NOTICIAS

        si self.use_ranking es True las consultas se mostraran ordenadas, no aplicable a la opcion -C

        """
        self.use_ranking = v

    #AGREGADO EN ALGORITMICA
    def set_approximation(self, v, distance, trie, threshold):
        """
        Activa o desactiva la aproximación de términos
        
        input: "v" booleano.
              "distance" algoritmo de distancia entre cadenas a usar (string)
              "trie" decide si se usa trie como estructura o no (booleano)
              "threshold" distancia máxima a considerar entre cadenas (int)

        si self.use_approximation es True los términos de las consultas podrán aproximarse a otros similares
        por algoritmos de distancia si no se encuentran resultados de esos términos

        """
        self.use_approximation = v
        self.approximation_distance = distance
        self.use_trie = trie
        self.approximation_threshold = threshold


    ###############################
    ###                         ###
    ###   PARTE 1: INDEXACION   ###
    ###                         ###
    ###############################


    def index_dir(self, root, **args):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        
        Recorre recursivamente el directorio "root" e indexa su contenido
        los argumentos adicionales "**args" solo son necesarios para las funcionalidades ampliadas

        """

        self.multifield = args['multifield']
        self.positional = args['positional']
        self.stemming = args['stem']
        self.permuterm = args['permuterm']
        self.approximation = args['approximation'] #Añadido en algoritmica
        self.use_trie = args['trie'] #Añadido en algoritmica

        for dir, subdirs, files in os.walk(root):
            for filename in files:
                if filename.endswith('.json'):
                    fullname = os.path.join(dir, filename)
                    self.index_file(fullname)
        
        if self.stemming is True:
          self.make_stemming()
          self.make_inverted_stems()
        
        #Algoritmica
        if self.approximation is True:
          if self.multifield is True:
            if self.use_trie:
              self.spellsuggester = TrieSpellSuggester(vocab=self.index['article'].keys())
            else:
              self.spellsuggester = SpellSuggester(vocab=self.index['article'].keys())
          else:
            if self.use_trie:
              self.spellsuggester = TrieSpellSuggester(vocab=self.index.keys())
            else:
              self.spellsuggester = SpellSuggester(vocab=self.index.keys())

        ##########################################
        ## COMPLETAR PARA FUNCIONALIDADES EXTRA ##
        ##########################################
        

    def index_file(self, filename):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Indexa el contenido de un fichero.

        Para tokenizar la noticia se debe llamar a "self.tokenize"

        Dependiendo del valor de "self.multifield" y "self.positional" se debe ampliar el indexado.
        En estos casos, se recomienda crear nuevos metodos para hacer mas sencilla la implementacion

        input: "filename" es el nombre de un fichero en formato JSON Arrays (https://www.w3schools.com/js/js_json_arrays.asp).
                Una vez parseado con json.load tendremos una lista de diccionarios, cada diccionario se corresponde a una noticia

        """
        IdNot = 0

        with open(filename) as fh:
            jlist = json.load(fh)
            self.docs[self.IdDoc]=filename
            

            for n in jlist: #Para cada noticia del documento
              if self.multifield is True: #Multifield está activado, coger resto de campos
                for tupla in self.fields:
                  (campo,tokenizar) = tupla

                  content = n[campo]
                  self.tam_not.setdefault(campo,{})
                  self.tam_not[campo].setdefault(self.newid,len(content))
                  

                  if tokenizar is True:
                    self.index.setdefault(campo,{})
                    tokens = self.tokenize(content) #Tokenizamos los términos
                    if self.positional is True:     #Creamos el indice posicional
                      self.make_positionals(tokens,campo)
                    else:
                      for tt in tokens:
                        self.index[campo].setdefault(tt,[])
                        #Comprobamos que el termino no se repite
                        if self.newid not in self.index[campo][tt]:
                          self.index[campo].setdefault(tt,[]).append(self.newid)
                  else:
                    self.index.setdefault(campo,{})
                    self.index[campo].setdefault(content,[])
                    if self.newid not in self.index[campo][content]:
                      self.index[campo][content].append(self.newid)

              else:
                content = n['article']

                self.tam_not.setdefault(self.newid,len(content))

                tokens = self.tokenize(content) #Tokenizamos los términos
                if self.positional is True:
                  self.make_positionals(tokens)
                else:
                  for tt in tokens:
                    self.index.setdefault(tt,[])
                    if self.newid not in self.index[tt]:
                      excluidos = {"title","date","keywords","summary"}
                      if tt not in excluidos:
                        self.index.setdefault(tt,[]).append(self.newid)



              self.news.setdefault(self.newid,[]).append((self.IdDoc,IdNot)) #Para cada noticia, indica el documento al que pertenece y su posición en el mismo
              self.newid += 1
              IdNot += 1
            self.IdDoc += 1    
            

        #################
        ### COMPLETAR ###
        #################



    def tokenize(self, text):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Tokeniza la cadena "texto" eliminando simbolos no alfanumericos y dividiendola por espacios.
        Puedes utilizar la expresion regular 'self.tokenizer'.

        params: 'text': texto a tokenizar

        return: lista de tokens

        """
        return self.tokenizer.sub(' ', text.lower()).split()



    def make_positionals(self, tokens, campo='article'):
      """
      Crea los posicionales de los tokens dentro de cada id de noticia

      """
      contador = 0
      
      if self.multifield is True:
        for tt in tokens:   
          self.index[campo].setdefault(tt,{}).setdefault(self.newid,[])
          if contador not in self.index[campo][tt][self.newid]:
            #Agregamos el id de noticia en el que aparece el token

            self.index[campo][tt][self.newid].append(contador)
            contador += 1       
      else:
        for tt in tokens:   
          self.index.setdefault(tt,{}).setdefault(self.newid,[])
          if contador not in self.index[tt][self.newid]:
            #Agregamos el id de noticia en el que aparece el token

            self.index[tt][self.newid].append(contador)
            contador += 1  

  


    def make_stemming(self):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING.

        Crea el indice de stemming (self.stemmindex) para los terminos de todos los indices.

        self.stemmer.stem(token) devuelve el stem del token

        """
        if self.multifield is True:
          for campo in self.index:
            if campo != "date":
              self.stemmindex.setdefault(campo,{})
              for token in self.index[campo]:
                stem = self.stemmer.stem(token)
                self.stemmindex[campo].setdefault(stem,[])
                for idnot in self.index[campo][token]: #Va copiando el reverse posting del token al stem
                  if idnot not in self.stemmindex[campo][stem]:
                    self.stemmindex[campo][stem].append(idnot)

                self.stemmindex[campo][stem].sort()

            else:
              self.stemmindex.setdefault(campo,{})
              self.stemmindex[campo] = self.index[campo]
        else:
            for token in self.index:
              stem = self.stemmer.stem(token)
              self.stemmindex.setdefault(stem,[])
              for idnot in self.index[token]: #Va copiando el reverse posting del token al stem
                if idnot not in self.stemmindex[stem]:
                  self.stemmindex[stem].append(idnot)

              self.stemmindex[stem].sort()




        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################



    def make_inverted_stems(self):
        """
        Crea un diccionario (self.sindex) para relacionar los stems son sus términos´

        """
        
        if self.multifield is True:
          for campo in self.index:
            if campo != 'date':
              for term in self.index[campo]:
                stem = self.stemmer.stem(term)
                self.sindex.setdefault(stem,[])
                if term not in self.sindex[stem]:
                  self.sindex[stem].append(term)
            else:
              for term in self.index[campo]:
                self.sindex.setdefault(term,term)
        else:
          for term in self.index:
            stem = self.stemmer.stem(term)
            self.sindex.setdefault(stem,[])
            if term not in self.sindex[stem]:
              self.sindex[stem].append(term)


    
    def make_permuterm(self):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM

        Crea el indice permuterm (self.ptindex) para los terminos de todos los indices.

        """
        pass
        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################




    def show_stats(self):
        """
        NECESARIO PARA TODAS LAS VERSIONES
        
        Muestra estadisticas de los indices
        
        """
        
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################
        print("========================")
        if self.multifield:
          print("Number of indexed days: %d" % len(self.index["date"]))
          print("-------------------------")
        print("Number of indexed news: %d" % len(self.news))
        print("-------------------------")
        print("TOKENS")

        for t in self.index:
          print("#of tokens in %s: %d" % (t, len(self.index[t])))
        print("-------------------------")
        print("PERMUTERMS")
        for p in self.ptindex:
          print("#of permuterms in %s: %d" % (p, len(self.ptindex[p])))
        print("-------------------------")
        print("STEMS")
        for s in self.stemmindex:
          print("#of stems in %s: %d" % (s, len(self.stemmindex[s])))
        print("-------------------------")
        post = " "
        if self.positional == []:
          post=" NOT "
        print("Positional queries are%sallowed" % (post))






    ###################################
    ###                             ###
    ###   PARTE 2.1: RECUPERACION   ###
    ###                             ###
    ###################################


    def solve_query(self, query, prev={}):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una query.
        Debe realizar el parsing de consulta que sera mas o menos complicado en funcion de la ampliacion que se implementen


        param:  "query": cadena con la query
                "prev": incluido por si se quiere hacer una version recursiva. No es necesario utilizarlo.


        return: posting list con el resultado de la query

        """
        posts = {}
        operadores = []
        if query is None or len(query) == 0:
            return []
        i = 0
        
        
        
        lista_query = re.split(" +(AND|OR) +",query)
        for term in lista_query:
          if term not in ['AND','OR']:
            
            
            if term.find('NOT ') == 0:  #Es un NOT
              string = term.split(' ')[1]
              aux = string.split(":")
              if len(aux) > 1:
                string = aux[1]
                campo = aux[0]
              else:
                campo = "article"
              if string.find('"') == 0:     #Positional
                string = string[1:len(string) - 1]
                posts[i] = self.reverse_posting(self.get_positionals(string, campo)) #Calculamos el "NOT posicional"
              else:
                posts[i] = self.reverse_posting(self.get_posting(string, campo)) #Calculamos el "NOT term"
              i+=1
            else:
              campo = "article"
              aux = term.split(":")
              if len(aux) > 1:
                term = aux[1]
                campo = aux[0]
              if term.find('"') == 0:     #Positional
                term = term[1:len(term) - 1]
                posts[i] = self.get_positionals(term, campo) #Calculamos el posting posicional
              else:
                posts[i] = self.get_posting(term,campo) #Calculamos la posting list del term
              i+=1
          else:
            operadores.append(term)
        i = 0
        for op in operadores:
          if op == 'AND':
            posts[i+1] = self.and_posting(posts[i],posts[i+1])
            i+=1
          else: #Es un OR
            posts[i+1] = self.or_posting(posts[i],posts[i+1])
            i+=1
        
        return posts[i]
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################

    

    def get_posting(self, term, field='article', positional=False):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Devuelve la posting list asociada a un termino. 
        Dependiendo de las ampliaciones implementadas "get_posting" puede llamar a:
            - self.get_positionals: para la ampliacion de posicionales
            - self.get_permuterm: para la ampliacion de permuterms
            - self.get_stemming: para la amplaicion de stemming


        param:  "term": termino del que se debe recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario si se hace la ampliacion de multiples indices

        return: posting list

        """
        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################
        res = []
        term = term.lower()
        if self.positional is True:
          if self.multifield is True:
            #Usamos positionals y multifield
            if self.use_stemming is True and positional is False:
              res = self.get_stemming(term, field)
            else:
              if field == 'date':
                if self.index[field].get(term) is not None:
                  res = self.index[field].get(term)
                else:
                  res = []
              else:
                if term in list(self.index[field].keys()):
                  if list(self.index[field][term].keys()) is not None:
                    res = list(self.index[field][term].keys())
                  else:
                    res = []
                else: res = []
          else: #No usamos multifield pero sí positionals
            if self.use_stemming is True:
              res = self.get_stemming(term)
            else:
              if self.index.get(term) is not None:
                res = list(self.index[term].keys())
              else:
                res = []

        else: #No usamos positionals
          if self.multifield is True:
            if self.use_stemming is True:
              res = self.get_stemming(term, field)
            else:
              if self.index[field].get(term) is not None:
                res = self.index[field].get(term)
              else:
                res = []
          else:
            if self.use_stemming is True:
              res = self.get_stemming(term)
            else:
              if self.index.get(term) is not None:
                res = self.index.get(term)
              else:
                res = []
        
        if self.use_approximation is True and res == []:
            if self.positional:
                if self.stemming is False:
                    if self.multifield is True:
                        lista = self.spellsuggester.suggest(term, self.approximation_distance,
                                                            threshold=self.approximation_threshold)
                        for palabra in lista:
                            res = self.or_posting(res, list(self.index[field][palabra].keys()))
                    else:
                        lista = self.spellsuggester.suggest(term, self.approximation_distance,
                                                            self.approximation_threshold)
                        for palabra in lista:
                            res = self.or_posting(res, list(self.index[palabra].keys()))
            else:
                if self.stemming is False:
                      if self.multifield is True:
                        lista = self.spellsuggester.suggest(term, self.approximation_distance, threshold=self.approximation_threshold)
                        for palabra in lista:
                          res = self.or_posting(res, self.index[field][palabra])
                      else:
                        lista = self.spellsuggester.suggest(term, self.approximation_distance , self.approximation_threshold)
                        for palabra in lista:
                          res = self.or_posting(res,self.index[palabra])
        
        return res


    def get_positionals(self, terms, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE POSICIONALES

        Devuelve la posting list asociada a una secuencia de terminos consecutivos.

        param:  "terms": lista con los terminos consecutivos para recuperar la posting list.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """
        res = []
        postings = [] #Contendrá las noticias en las que aparecen todos los términos
        lista_terms = terms.split(' ')
        
        for term in lista_terms:
          postings.append(self.get_posting(term,field,True))

        i=0
        while i < len(lista_terms)-1:
          postings[i+1] = self.and_posting(postings[i],postings[i+1])
          i+=1


        """
        Para cada noticia:
          Coger las posiciones de cada termino i y poner en pos[i]
          Hacer un AND entre pos[0] y pos[i] restando i a cada elemento (por la diferencia en posicion por palabras)


        """

        if postings[i] is not None and not self.use_approximation:
          for noticia in postings[i]:
            pos = []
            for term in lista_terms:
              if self.multifield is True:
                pos.append(list(self.index[field][term][noticia]))
              else:
                pos.append(self.index[term][noticia])
            j=0
            while j < len(pos):
              pos[j] = [x-j for x in pos[j]]
              j+=1
            j=0
            while j < len(pos)-1:
              pos[j+1] = self.and_posting(pos[j],pos[j+1])
              j+=1
            if len(pos[j]) != 0:
              res.append(noticia)
        elif postings[i] is not None:
            res.extend(postings[i])

        if res is None:
            return []
        else:
            return res
        ########################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE POSICIONALES ##
        ########################################################


    def get_stemming(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE STEMMING

        Devuelve la posting list asociada al stem de un termino.

        param:  "term": termino para recuperar la posting list de su stem.
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """
        if self.stemming is False:
          print("Stemming Desactivado")
          exit()

        if self.multifield is True:
          stem = self.stemmer.stem(term)
          if field == "date":
            return self.stemmindex[field].get(stem)
          else:
            if self.stemmindex[field].get(stem) is not None:
                return self.stemmindex[field].get(stem)
            else:
                res = []
        else:
          stem = self.stemmer.stem(term)
          if self.stemmindex.get(stem) is not None:
              return self.stemmindex.get(stem)
          else:
              res = []

        ####################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE STEMMING ##
        ####################################################


    def get_permuterm(self, term, field='article'):
        """
        NECESARIO PARA LA AMPLIACION DE PERMUTERM

        Devuelve la posting list asociada a un termino utilizando el indice permuterm.

        param:  "term": termino para recuperar la posting list, "term" incluye un comodin (* o ?).
                "field": campo sobre el que se debe recuperar la posting list, solo necesario se se hace la ampliacion de multiples indices

        return: posting list

        """

        ##################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA PERMUTERM ##
        ##################################################




    def reverse_posting(self, p):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Devuelve una posting list con todas las noticias excepto las contenidas en p.
        Util para resolver las queries con NOT.


        param:  "p": posting list


        return: posting list con todos los newid exceptos los contenidos en p

        """
        
        posting = []      
        i = 0
        while ((i < len(self.news))):
          if i not in p:
            posting.append(i)
          i +=1

        return posting


    def and_posting(self, p1, p2):
      """
      NECESARIO PARA TODAS LAS VERSIONES

      Calcula el AND de dos posting list de forma EFICIENTE

      param:  "p1", "p2": posting lists sobre las que calcular


      return: posting list con los newid incluidos en p1 y p2

      """
      
      posting = []
      i = 0 
      j = 0
      if p1 is None and p2 is None: res = []
      while ((i < len(p1)) & (j < len(p2))):
        if p1[i] == p2[j]:
          posting.append(p2[j])
          i += 1 
          j += 1
        elif p1[i] < p2[j]:
            i += 1
        else: j += 1

      return posting


    def or_posting(self, p1, p2):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Calcula el OR de dos posting list de forma EFICIENTE

        param:  "p1", "p2": posting lists sobre las que calcular


        return: posting list con los newid incluidos de p1 o p2

        """
        
        posting = []
        i = 0 
        j = 0



        while ((i < len(p1)) & (j < len(p2))):
          if p1[i] == p2[j]:
            posting.append(p1[i])
            i = i+1
            j = j+1
          elif p1[i] < p2[j]:
            posting.append(p1[i])
            i = i+1
          else:
            posting.append(p2[j])
            j = j+1

        while (i < len(p1)):
          posting.append(p1[i])
          i += 1
        while (j < len(p2)):
          posting.append(p2[j])
          j += 1

        return posting



    #####################################
    ###                               ###
    ### PARTE 2.2: MOSTRAR RESULTADOS ###
    ###                               ###
    #####################################


    def solve_and_count(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una consulta y la muestra junto al numero de resultados 

        param:  "query": query que se debe resolver.

        return: el numero de noticias recuperadas, para la opcion -T

        """
        result = self.solve_query(query)
        print("%s\t%d" % (query, len(result)))
        return len(result)  # para verificar los resultados (op: -T)


    def solve_and_show(self, query):
        """
        NECESARIO PARA TODAS LAS VERSIONES

        Resuelve una consulta y la muestra informacion de las noticias recuperadas.
        Consideraciones:

        - En funcion del valor de "self.show_snippet" se mostrara una informacion u otra.
        - Si se implementa la opcion de ranking y en funcion del valor de self.use_ranking debera llamar a self.rank_result

        param:  "query": query que se debe resolver.

        return: el numero de noticias recuperadas, para la opcion -T
        
        """
        result = self.solve_query(query)

        
        if self.show_snippet is True or self.use_ranking is True: #Generamos snippets en orden de result
          terms = []
          lista_query = re.split(" +(AND|OR) +",query)
          for term in lista_query:
            if term not in ['AND','OR']:
              if term.find('NOT ') != 0: #Si no hay un not en el término
                terms.append(term)
        
          if self.show_snippet is True and len(result)>0:
            snippets = self.create_snippet(result,terms)
          if self.use_ranking is True and len(result)>0:
            result = self.rank_result(result,terms)
            
          
        print("========================")
        print("Query: '%s'" % query)
        print("Number of results: %d" % len(result))
        i=1


        

        for id in result:
          

          (doc,position) = self.news[id][0]
          filename = self.docs[doc]
          with open(filename) as fh:
            jlist = json.load(fh)
            jlist = jlist[position]
            fecha = jlist['date']
            title = jlist['title']
            keywords = jlist['keywords']


          if self.use_ranking is True and len(result)>0:
            print("#%d \t (%d)\t (%d)\t (%s) %s \t (%s) " % (i, doc, self.weight[id], fecha, title, keywords))
          else:
            print("#%d \t (%d)\t (0)\t (%s) %s \t (%s) " % (i, doc, fecha, title, keywords))

          if self.show_snippet is True:
              for snippet in snippets[id]:
                print("\t\t %s" % snippet)

          i+=1
          if i > self.SHOW_MAX and self.show_all == False:
            break

          

        print("========================")
        return len(result)



        ########################################
        ## COMPLETAR PARA TODAS LAS VERSIONES ##
        ########################################
    def func_sort(self,noticia):
      """
      Devuelve las puntuaciones

      param: "noticia": número de noticia

      """
      
      
      return self.weight[noticia]




    def create_snippet(self, posts, terms):
      """
      Crea un snippet de los términos que aparecen en la query y en el documento

      param:  "posts": posting list de los documentos que coinciden con la query
              "terms": términos que aparecen en la query

      """
      lista_snippets = {}
      positional = False

      for noticia in posts:
        (doc_id, posicion) = self.news[noticia][0]
        f = self.docs[doc_id]
        lista_snippets.setdefault(noticia,[])
        with open(f) as fh:
          jlist = json.load(fh)
          news = jlist[posicion]

          for term in terms:
            field = 'article' #Valor por defecto
            if term.find('"')==0:
              #Es posicional
              positional = True
              term = term[1:len(term)-1]
            else:
              #No es posici
              positional = False
            aux = term.split(":")
            if len(aux) > 1:
              #Tiene keywords
              term = aux[1]
              field = aux[0]


            if self.use_stemming is True and positional is False:
              stem = self.stemmer.stem(term)
              if len(stem) == len(term):
                pattern = re.compile(r'\b({0})\b'.format(term), flags=re.IGNORECASE) #La longitud del stem es la misma, puede que solo quite acentos
              else:
                pattern = re.compile(r'\b({0})'.format(stem), flags=re.IGNORECASE) #Puede no haber espacio al final al ser stem
            else:
              pattern = re.compile(r'\b({0})\b'.format(term), flags=re.IGNORECASE)

            #Separamos la palabra del resto del texto
            if self.use_stemming:              
              words = re.split(pattern, self.normalize(news[field]))
            else:
              words = re.split(pattern, news[field])

            if len(words) > 1:
              precedente = ' '.join(words[0].split()[-3:])
              consecuente = ' '.join(words[2].split()[:3])

              if self.use_stemming is True and positional is False:
                result = "..." + precedente + " " + stem + "" + consecuente + "..."
              else:
                result = "..." + precedente + " " + term + " " + consecuente + "..."
                
              lista_snippets[noticia].append(result)
            
          
      return lista_snippets
    

    def normalize(self, s):
      """
      Elimina las tildes de un texto

      :param
        s: texto a normalizar
        
      :return: texto s sin tildes
      """
      replacements = (
          ("á", "a"),
          ("é", "e"),
          ("í", "i"),
          ("ó", "o"),
          ("ú", "u"),
      )
      for a, b in replacements:
          s = s.replace(a, b).replace(a.upper(), b.upper())
      return s

    def rank_result(self, result, query):
        """
        NECESARIO PARA LA AMPLIACION DE RANKING

        Ordena los resultados de una query.

        param:  "result": lista de resultados sin ordenar
                "query": query, puede ser la query original, la query procesada o una lista de terminos


        return: la lista de resultados ordenada

        """
        self.weight #Aquí almacenaremos la Score de cada documento
        fields = []
        terms = []

        for term in query:
          aux = term.split(':')
          field = 'article'
          if len(aux) > 1:
            #Tiene keyword
            field = aux[0]
            term = aux[1]
            if term.find('"')==0: 
              #Es posicional
              term = term[1:len(term)-1]
              for subterm in term.split(' '):
                terms.append(subterm)
                fields.append(field)
            else:
              #No es posicional
              terms.append(term)
              fields.append(field)
          else:
            #No tiene keyword
            if term.find('"')==0: 
              #Es posicional
              term = term[1:len(term)-1]  #Quitamos las comillas
              for subterm in term.split(' '):
                terms.append(subterm)
                fields.append(field)
            else:
              #No es posicional
              terms.append(term)
              fields.append(field)       


        rareza_termino = []
        i=0
        if self.multifield is True:
          if self.use_stemming is True: 
            #Multifield y Stemming
            while i < len(terms):
              stem = self.stemmer.stem(terms[i])
              if stem in self.sindex:
                term_stem = self.sindex[stem]
                rareza_termino.append(0)
                for t in term_stem:
                  if t in list(self.index[fields[i]]):
                    rareza_termino[i] += len(self.index[fields[i]][t])
              if rareza_termino[i] == 0:
                rareza_termino[i] = 100000 #Ponemos un valor alto ya que queremos usar la inversa
              i+=1
          else:   
            #Multifield y No Stemming
            while i < len(terms):
              if terms[i] in self.index[fields[i]]:
                rareza_termino.append(len(self.index[fields[i]][terms[i]]))
              else:
                rareza_termino.append(100000) #Ponemos un valor alto ya que queremos usar la inversa
              
              i+=1
        else:
          if self.use_stemming is True: 
            #No Multifield y Stemming
            while i < len(terms):
              stem = self.stemmer.stem(terms[i])
              if stem in self.sindex:
                term_stem = self.sindex[stem]
                rareza_termino.append(0)
                for t in term_stem:
                  if t in list(self.index.keys()):
                    rareza_termino[i] += len(self.index[t])
              if rareza_termino[i] == 0:
                rareza_termino[i] = 100000 #Ponemos un valor alto ya que queremos usar la inversa

              i+=1
            
          else:   
            #No Multifield y no Stemming
            while i<len(terms):
              rareza_termino.append(len(self.index[terms[i]]))
              if rareza_termino[i] == 0:
                rareza_termino[i] = 100000
              i+=1
          



        weights = []
        for noticia in result:
          i=0
          if self.multifield is True:
            if self.use_stemming is True: #Usamos stemming y multifield
              res = 0
              while i<len(terms):
                sum = 0
                stem = self.stemmer.stem(terms[i])
                if stem in self.sindex:
                  term_stem = self.sindex[stem]
                  for t in term_stem:
                    if t in list(self.index[fields[i]]):
                      if noticia in list(self.index[fields[i]][t]):
                        if self.positional is True:
                          sum += len(self.index[fields[i]][t][noticia])
                        else:
                          sum += 1
                #Formula refachera para los pesos de cada noticia
                res+= sum*(1/rareza_termino[i])*10000000/self.tam_not[fields[i]][noticia]
                i+=1 
              self.weight.setdefault(noticia,res)
            else: #Usamos multifield sin stemming
              res = 0
              while i<len(terms):
                sum = 0
                if terms[i] in list(self.index[fields[i]]):
                  if noticia in list(self.index[fields[i]][terms[i]]):
                    if self.positional is True:
                      sum += len(self.index[fields[i]][terms[i]][noticia])
                    else:
                      sum += 1

                res+= sum*(1/rareza_termino[i])*10000000/self.tam_not[fields[i]][noticia]
                i+=1
              self.weight.setdefault(noticia,res)
          else:
            if self.use_stemming is True: #Usamos stemming sin multifield
              res = 0
              while i<len(terms):
                sum = 0
                stem = self.stemmer.stem(terms[i])
                if stem in self.sindex:
                  term_stem = self.sindex[stem]
                  for t in term_stem:
                    if t in list(self.index):
                      if noticia in list(self.index[t]):
                        if self.positional is True:
                          sum += len(self.index[t][noticia])
                        else:
                          sum += 1
                res+= sum*(1/rareza_termino[i])*10000000/self.tam_not[noticia]
                i+=1 
              self.weight.setdefault(noticia,res)
            else: #No usamos otras ampliaciones
              res=0
              while i<len(terms):
                sum = 0
                if terms[i] in list(self.index):
                  if noticia in list(self.index[terms[i]]):
                    if self.positional is True:
                      sum += len(self.index[terms[i]][noticia])
                    else:
                      sum += 1
                res+= sum*(1/rareza_termino[i])*10000000/self.tam_not[noticia]
                i+=1
              self.weight.setdefault(noticia,res)
          weights.append(self.weight[noticia])

        Z = [x for _,x in sorted(zip(weights,result),reverse=True)]
        return Z

        #self.weight[i] es un pesado de la inversa de apariciones totales del termino entre el numero de veces que aparece en la noticia

        
        
        ###################################################
        ## COMPLETAR PARA FUNCIONALIDAD EXTRA DE RANKING ##
        ###################################################
