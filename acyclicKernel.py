import networkx as nx
import matplotlib.pyplot as plt
import mplcursors
import itertools
import json
import numpy as np
import random
import spacy

text = []

A = ['La oración de ejemplo', 'La mesa esta chueca', 'La sociedad esta rara', ]

# Para no lematizar descomentar la siguiente línea
Aa = [sentence.split(' ') for sentence in A]

# Seleccionar modelo de spacy para lematizar
#nlp = spacy.load('es_dep_news_trf') #spacy.load('en_core_web_sm') #spacy.load('es_dep_news_trf')

# Lematización de las oraciones de la lista A
#Aa = [[token.lemma_ for token in nlp(text)] for text in A]

#Creación de la digráfica

G = nx.DiGraph()

for i in range(len(A)):
    for j in range(len(Aa[i])-1):
        G.add_edge(Aa[i][j],Aa[i][j+1])

# Información básica de la digráfica
print(f'Palabras:{Aa}\n Cantidad de palabras: {len(G.nodes)}\n Cantidad de oraciones: {len(A)}\n  Grado de entrada: {G.in_degree}\n Grado de salida: {G.out_degree}\n Grado: {G.degree}\n Diametro de la gráfica subyacente: {nx.diameter(G.to_undirected())}\n Excentricidad: {dict(nx.eccentricity(G.to_undirected()))}\n Centralidad de los vertices: {nx.degree_centrality(G)}')

# Función para encontrar el núcleo de una digráfica

def AcyclicKernel(G):
    D = G.copy()
    Pozos = set()

    while D:
        Po = [node for node in D if D.out_degree(node)==0] 

        for v in Po:
            prePo = G.predecessors(v)
            D.remove_nodes_from(prePo)
        
            Pozos.update(Po)

            D.remove_nodes_from(Po)
    return Pozos

quasi_kernel_G = AcyclicKernel(G)

# Dibujar la gráfica con matplotlib
node_colors = ["skyblue" if node in quasi_kernel_G else "red" for node in G.nodes]
pos = nx.spring_layout(G)
nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=80)
nx.draw_networkx_edges(G, pos, arrowsize=20)
#nx.draw_networkx_labels(G, pos)
plt.axis("off")

crs = mplcursors.cursor(hover=True)

#Para que no cambien el color de los vértices descomentar la siguiente línea

crs.connect("add", lambda sel: sel.annotation.set_text(f'{list(G.nodes)[sel.target.index]} (in-grado: {G.in_degree(list(G.nodes)[sel.target.index])})'))

#Para que cambien el color de los vértices descomentar las siguientes líneas

#node_colors = list(itertools.chain(*node_colors))

#nodes.set_array(np.array(node_colors))

#def update(sel):
#    node_idx = sel.target.index
#    node = list(G.nodes)[node_idx]
#    successors = list(G.successors(node))

#    color_map = {"black": 1, "green": 2, "blue": 3}
#    node_colors = [color_map["green"] if node in successors else color_map["blue"] for node in G.nodes]
#    nodes.set_array(np.array(node_colors))

#    sel.annotation.set_text(f'{node} (in-degree: {G.in_degree(node)})')
#    plt.draw()

#crs.connect("add", update)

plt.show()
