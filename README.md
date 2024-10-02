# Núcleo y quasi-núcleo
Un núcleo es un subconjunto de nodos de una gráfica dirigida, tal que es independiente y absorbente, esto es en orden que los nodos del núcleo no son adyacentes entre sí, y que todo para todo nodo $v$ que no esta en el núcleo, existe un nodo $u$ en el núcleo tal que la distancia de $v$ a $u$ es 1.

Un quasi-núcleo relaja la condición de ser absorbente a ser 2-absorbente, que es pedir que la distancia de $v$ a $u$ sea menor igual a 2.

Algunos teoremas para tener a consideración es que

  $\bullet$ Toda gráfica dirigida tiene quasi-núcleo, pero no necesariamente es único.

  $\bullet$ Encontrar un núcleo en una gráfica dirigida es un problema NP.

  $\bullet$ Los núcleos siempre existen y son únicos en gráficas dirigidas aciclicas.

  $\bullet$ En general si existen dos núcleos en una gráfica dirigida entonces existe un tercer núcleo diferente de los otros dos.

El concepto de núcleo muy simplificadamente, nacío de querer encontrar estrategias ganadoras en juegos.

# Codigo para encontrar el conjunto quasi-núcleo (y cuando exista núcleo) de una gráfica dirigida.

Básicamente el codigo se divide en cuatro partes, la primera es para leer un archivo json, extraer el texto y guardarlo en una lista con nombre de variable A; en segundo la creación de la digráfica en cuestión; en tercero son las funciones para encontrar un quasi-núcleo o núcleo y por último la generación de la representación visual de la digráfica.

Y se usa python y principalmente las librerías de networkx, matplotlib entre otras.
  
Aquí nada mas me enfocare en describir rapidamente la parte de calcular el quasi-núcleo (o núcleo si existe).

Entonces, el proceso para encontrar el quasí-núcleo (o núcleo) es ir agarrando conjuntos independientes de vértices y checar si tienen la propiedad de ser 2-absorbente (o absorbente), tecnicamente un while loop, que se detiene cuando encuentra el quasi-núcleo.

La función en el codigo que se encarga de encontrar un conjunto independiente es 

    def Independent_set(graph):
        mis = set()
        nodes = list(graph.nodes())
    
        Po = [node for node in nodes if G.out_degree(node)==0]
    
        mis.update(Po)
    
        while nodes:
            node = nodes.pop()
            mis.add(node)
            nodes = [n for n in nodes if not (n in graph[node] or node in graph[n])]
    
        return mis

El cual empieza encontrando los nodos que son pozos (que no tienen flechas hacia alguien) y los agrega al conjunto "mis" pues por la condición de 2-absorbencia (y absorbencia) estos deben formar parte del núcleo necesariamente, luego de esto se selecciona un nodo al azar tal que no domina ni es dominado por un nodo en "mis", esto hasta que ya no haya nodos en la gráfica dirigida que satisfagan lo anterior.

Luego se define la función que checa si un conjunto tiene la propiedad de 2 absorbencia (o absorbencia) mediante la función
    
    def dist_2(G, S):
        for node in set(G.nodes) - S:
            if all(nx.shortest_path_length(G, node, s) > 2 for s in S if nx.has_path(G, node, s)):
                return False
        return True

Que checa si existe una trayectoria dirigida de un nodo a un nodo del quasi núcleo (o núcleo), y luego si la tryectoria dirigida de longitud minima es de longitud mayor a 2 (o 1), es decir esta función ve que si un nodo no es 2-absorbido (absorbido) regresa falso, y si todos los nodos son 2 absorbidos (o absorbidos) regresa verdadero.

Y este proceso si acaba pues es conocido que toda gráfica dirigida tiene quasi-núcleo pero:

OJO: Como una gráfica dirigida no necesariamente tiene núcleo puede que si se pide la absorbencia en vez de la 2 absorbencia en el código, el while loop nunca acabe.

# Extracción del texto

La extracción del texto consiste en una función, que extrae las palabras de una lista de texto

    def split_sentence(sentence):
      return [word for word in re.findall(r'\b\w+\b', sentence)]
    
    Aa = [split_sentence(A[i]) for i in range(len(A))]

Ya con esto se genera una digráfica de co-ocurrencia, donde los vértices son palabras y hay flechas de una palabra a otra si estas co-ocurren en un texto. Donde la palabra $x$ co-ocurre a la palabra $y$, si $x$ es la palabra anterior a $y$ en algun texto.
