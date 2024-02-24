import networkx as nx #Para generar la digráfica
import matplotlib.pyplot as plt #Opcional. Para una representación de la digráfica
import mplcursors 
import itertools
import json
import numpy as np
import random
import spacy

##### Parte generada por Github-copilot
# Load the JSON data
with open("---") as file:
    data = json.load(file)

# Initialize an empty list to store the text
text = []

# Iterate over all elements in the data
for element in data:
    # Iterate over the messages in the element
    for key in element['mapping']:
        # Check if the message field is not None
        if element['mapping'][key]['message'] is not None:
            # Extract the text from the message and add it to the list
            text.append(element['mapping'][key]['message']['content']['parts'][0])
##### Fin

# Lista de oraciones o texto de ejemplo
A = ['La oración de ejemplo', 'La mesa esta chueca', 'La sociedad esta rara', 'La palabra es muy corta', 'La palabra es muy larga', 'La vida tiene un origen bastante especial', 'La condena es condenar al condenado', 'La lematización de este ejemplo sera rara'] #['Esta es una oración, para un ejemplo', 'Aquí hay otra oración de ejemplo', 'Una tercera oración para el ejemplo', 'Una cuarta oración para el ejemplo', 'Una vaca come oraciones', 'Una', 'Las oraciones se ven como líneas']

# Para no lematizar descomentar la siguiente línea
Aa = [sentence.split(' ') for sentence in A]

# Seleccionar modelo de spacy para lematizar
#nlp = spacy.load('es_dep_news_trf') #spacy.load('en_core_web_sm') #spacy.load('es_dep_news_trf')

# Lematización de las oraciones de la lista A, comentar linea 32 en este caso
#Aa = [[token.lemma_ for token in nlp(text)] for text in A]

#Creación de la digráfica

G = nx.DiGraph()

for i in range(len(A)):
    #for j in Aa[i]:
    #    G.add_edge(A[i],j)
    for j in range(len(Aa[i])-1):
        G.add_edge(Aa[i][j],Aa[i][j+1])

# Maximo ingrado de la digrafica
def max_of_G(G):
    m = {G.in_degree(v) for v in G.nodes}
    return (max(m),m)

# Función para checar que un conjunto S tiene la propiedad de ser 2 absorbente, para que cambiar a 1 absorbente cambiar el 2 por 1
# OJO: Si se selecciona que sea 1 aborbente, el programa puede estancarse en un while loop
def dist_2(G, S):
    for node in set(G.nodes) - S:
        if all(nx.shortest_path_length(G, node, s) > 2 for s in S if nx.has_path(G, node, s)):
            return False
    return True

# Función para encontrar conjunto independiente    
def find_independent_set(graph):
    fis = set()
    nodes = list(graph.nodes())

    Po = [node for node in nodes if G.out_degree(node)==0]

    fis.update(Po)

    for v in Po:
        prePo = G.predecessors(v)
        nodes -= list(prePo)

    while nodes:
        node = nodes.pop()
        fis.add(node)
        nodes = [n for n in nodes if not (n in graph[node] or node in graph[n])]

    # Para ver el proceso de encontrar el conjunto independiente descomentar la siguiente línea
    #print(f'Nodos: {Nodes}\nQuasi-kernel: {ind}')
    
    return fis

# Función para checar que el conjunto dado por la función anterior satisface 
# ser 2-absorbente
def refine_set(G):
    S = find_independent_set(G)
    while not dist_2(G, S):
        S = find_independent_set(G)
    return S

quasi_kernel_G = refine_set(G)

# Info de la digráfica
print(f'Palabras:{Aa}\n Cantidad de palabras: {len(G.nodes)}\n Cantidad de oraciones: {len(A)}\n Grado de entrada: {G.in_degree}\n Grado de salida: {G.out_degree}\n Grado: {G.degree}\n Diametro de la gráfica subyacente: {nx.diameter(G.to_undirected())}\n Excentricidad: {dict(nx.eccentricity(G.to_undirected()))}\n Centralidad de los vertices: {nx.degree_centrality(G)}\n (Quasi) Núcleo: {Narb}\n Cardinalidad del (quasi) núcleo: {len(Narb)}\n No (quasi) núcleo: {set(G.nodes - Narb)}\n Nodos1: {N1}\n Nodos2: {N2}')

# Conjuntos auxiliares para una mejor re´resentación de la digráfica
N2 = set(v for v in set(G.nodes) if any(nx.shortest_path_length(G, v, s) == 2 for s in Narb if nx.has_path(G, v, s)))

N1 = set(v for v in set(G.nodes) if any(nx.shortest_path_length(G, v, s) == 1 for s in Narb if nx.has_path(G, v, s)))

# Función para acomodar los nodos en círculos
def calculate_positions(G, Narb, N1, N2):
    positions = {}
    num_nodes = len(G.nodes)
    narb_nodes = len(Narb)
    n1_nodes = len(N1)
    n2_nodes = len(N2)
    for i, node in enumerate(G.nodes):
        if node in Narb:
            theta = (num_nodes / (2 * math.pi)) + (i / (2 * math.pi))
            positions[node] = (3 * math.cos(theta), 3 * math.sin(theta))
        elif node in N1:
            theta = (num_nodes / (2 * math.pi)) + (i / (2 * math.pi))
            positions[node] = (2 * math.cos(theta), 2 * math.sin(theta))
        elif node in N2:
            theta = (num_nodes / (2 * math.pi)) + (i / (2 * math.pi))
            positions[node] = (math.cos(theta), math.sin(theta))
    return positions

# Posición de los nodos segun la función anterior
pos = calculate_positions(G, quasi_kernel_G, N1, N2)

# Dibujar la gráfica con matplotlib
node_colors = ["skyblue" if node in quasi_kernel_G else "red" for node in G.nodes]
nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=80)
nx.draw_networkx_edges(G, pos, arrowsize=20)
#nx.draw_networkx_labels(G, pos)
plt.axis("off")

crs = mplcursors.cursor(hover=True)

###Para que no cambien el color de los vértices descomentar la siguiente línea

crs.connect("add", lambda sel: sel.annotation.set_text(f'{list(G.nodes)[sel.target.index]} (in-grado: {G.in_degree(list(G.nodes)[sel.target.index])})'))

###Para que cambien el color de los vértices descomentar las siguientes líneas

#node_colors = list(itertools.chain(*node_colors))

#nodes.set_array(np.array(node_colors))

def update(sel):
    node_idx = sel.target.index
    node = list(G.nodes)[node_idx]
    successors = list(G.successors(node))

    color_map = {"black": 1, "green": 2, "blue": 3}
    node_colors = [color_map["green"] if node in successors else color_map["blue"] for node in G.nodes]
    nodes.set_array(np.array(node_colors))

    sel.annotation.set_text(f'{node} (in-degree: {G.in_degree(node)})')
    plt.draw()

crs.connect("add", update)

plt.show()
