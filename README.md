# Núcleo y quasi-núcleo
Un núcleo es un subconjunto de nodos de una gráfica dirigida, tal que es independiente y absorbente, esto es en orden que los nodos del núcleo no son adyacentes entre sí, y que todo para todo nodo $v$ que no esta en el núcleo, existe un nodo $u$ en el núcleo tal que la distancia de $v$ a $u$ es 1.

Un quasi-núcleo relaja la condición de ser absorbente a ser 2-absorbente, que es pedir que la distancia de $v$ a $u$ sea menor igual a 2.

Algunos teoremas para tener a consideración es que

  $\bullet$ Toda gráfica dirigida tiene quasi-núcleo, pero no necesariamente es único.

  $\bullet$ Encontrar un núcleo en una gráfica dirigida es un problema NP.

  $\bullet$ Los núcleos siempre existen y son únicos en gráficas dirigidas aciclicas.

  $\bullet$ En general si existen dos núcleos en una gráfica dirigida entonces existe un tercer núcleo diferente de los otros dos.

El concepto de núcleo muy simplificadamente, nacío de querer encontrar estrategias ganadoras en juegos.

#Codigo para encontrar el conjunto quasi-núcleo (y cuando exista núcleo) de una digráfica.

Básicamente el codigo se divide en cuatro partes, la primera es para leer un archivo json, extraer el texto y guardarlo en una lista con nombre de variable A; en segundo la creación de la digráfica en cuestión; en tercero son las funciones para encontrar un quasi-núcleo o núcleo y por último la generación de la representación visual de la digráfica.
  
Aquí nada mas me enfocare en describir un poco la parte de calcular el quasi-núcleo (o núcleo si existe)

Entonces, el proceso para encontrar el quasí-núcleo (o núcleo) es ir agarrando conjuntos independientes de vértices y checar si tienen la propiedad de ser 2-absorbente (o absorbente), tecnicamente un while loop, que se detiene cuando encuentra el quasi-núcleo.

\textbf{OJO}: Como una gráfica dirigida no necesariamente tiene núcleo puede que si se pide la absorbencia en vez de la 2 absorbencia en el código, el while loop nunca acabe.

# Extracción de texto

