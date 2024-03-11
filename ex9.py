import copy
import string
import random
import networkx as nx
import matplotlib.pyplot as plt


# В этой функции зададим шаблоны графа, определим удаляющуюся переменную, определим внутреннюю функцию,
# которая будет ссылаться на переменные функции старшего порядка.
# Так же реализуем поиск в глубину для нахождения всех путей графа
def generate_graph():
    graphs = [{'A': ['B', 'C', 'D'], 'D': ['E', 'F', 'G'], 'G': ['H', 'I'], 'B': ['D', 'E'], 'C': ['D', 'F'],
               'E': ['G', 'H'], 'F': ['G', 'I'], 'H': 'I'},
              {'A': ['B', 'C', 'D'], 'B': ['F', 'E'], 'E': ['F', 'G', 'H'], 'F': ['H', 'G', 'I'], 'G': ['I', 'H'],
               'H': ['I'], 'D': ['E', 'G'], 'C': 'E'},
              {'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['E', 'F'], 'D': ['E', 'G'], 'E': ['G', 'H'], 'F': ['E', 'I'],
               'G': ['H', 'J'], 'H': 'J', 'I': ['H', 'J']},
              {'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['E', 'F'], 'D': 'G', 'E': 'G', 'F': 'G', 'G': ['I', 'H'],
               'H': 'J', 'I': 'J'}]
    # выберем случайный граф, случайно удалим одну из его вершин, сохраним в новой переменной
    # новый граф с удаленной вершиной и удалим все ребра идущие в нее
    graph_data = random.choice(graphs)
    del_node = random.choice([string.ascii_uppercase[i] for i in range(len(graph_data))][1:-1])
    new_graph_data = copy.deepcopy(graph_data)
    del new_graph_data[del_node]
    for key, value in list(new_graph_data.items()):
        if value == del_node:
            del new_graph_data[key]
        elif del_node in list(value):
            value.pop(value.index(del_node))
    final_node = string.ascii_uppercase[len(graph_data)]
    print(del_node)

    # depth first search, DFS. default argument is mutable, но мы к этому готовы :)
    def find_paths(start='A', path=[]):
        path = path + [start]
        if start == final_node:
            return [path]
        if start not in new_graph_data:
            return []
        all_paths = []
        for vertex in new_graph_data[start]:
            if vertex in path:
                continue
            paths = find_paths(start=vertex, path=path)
            all_paths.extend(paths)
        return all_paths

    #сохраним пути в res, распечатаем количество путей(для сравнения с ответом тестирующегося) и сами пути
    #исключительно для проверки работоспособности
    res = find_paths()
    print(len(res))
    print('пути: ', res)
    return graph_data, new_graph_data, res

# сохраним возврат функции, создадим исходный граф, преобразуем словарь графа в список
# на основе списка отрисуем исходный граф
graph, new_graph, number_of_tracks  = generate_graph()
G, list_edges = nx.DiGraph(), []
#
for node in graph:
    for elem in graph[node]:
        list_edges.append([node, elem])
G.add_edges_from(list_edges)
# #Здесь определим внешний вид графа
options = {
    'edge_color': 'black',
    'node_color': 'black',
    'font_color': 'white',
    'node_size': 350,
    'width': 1
}
nx.draw_planar(G, **options, with_labels=True)
plt.show()