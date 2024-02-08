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
with open("C:/Users/Miguel/Desktop/Manim/conversations.json") as file:
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

# Información básica de la digráfica
print(f'Palabras:{Aa}\nMaximo in-grado de la digráfica:{max_of_G(G)}\n Cantidad de palabras: {len(G.nodes)}\n Cantidad de oraciones: {len(A)}\n  Grado de entrada: {G.in_degree}\n Grado de salida: {G.out_degree}\n Grado: {G.degree}\n Diametro de la gráfica subyacente: {nx.diameter(G.to_undirected())}\n Excentricidad: {dict(nx.eccentricity(G.to_undirected()))}\n Centralidad de los vertices: {nx.degree_centrality(G)}')

# Función para checar que un conjunto S tiene la propiedad de ser 2 absorbente, para que cambiar a 1 absorbente cambiar el 2 por 1
def dist_2(G, S):
    for node in set(G.nodes) - S:
        if all(nx.shortest_path_length(G, node, s) > 2 for s in S if nx.has_path(G, node, s)):
            return False
    return True

# Función para encontrar conjunto independiente    
def Independent_set(G):
    ind = set()
    Nodes = set(G.nodes)

    while Nodes:
        v = random.choice(list(Nodes))
        if v in Nodes:
            Nodes.remove(v)

        predecessors = set(G.predecessors(v))
        Nodes -= predecessors

        for u in predecessors:
            Nodes -= set(G.predecessors(u))

        if all(G.has_edge(v, u) == False for u in ind):
            ind.add(v)
        if not all(G.has_edge(u, v) == False for u in ind):
            ind.remove(v)
    
    # Para ver el proceso de encontrar el conjunto independiente descomentar la siguiente línea
    #print(f'Nodos: {Nodes}\nQuasi-kernel: {ind}')

    return ind

# Función para checar que el conjunto dado por la función anterior satisface 
# ser 2-absorbente
def refine_set(G):
    S = Independent_set(G)
    while not dist_2(G, S):
        S = Independent_set(G)
    return S

quasi_kernel_G = refine_set(G)

print("Quasi-núcleo:", refine_set(G))

# Dibujar la gráfica con matplotlib
node_colors = ["skyblue" if node in quasi_kernel_G else "red" for node in G.nodes]
pos = nx.spring_layout(G)
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
