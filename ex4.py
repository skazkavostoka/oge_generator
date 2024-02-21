from dejkstra_sp import *
import networkx as nx
import prettytable


@try_recursion
def exercise_generator():
    G = nx.Graph()
    nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    shuffle(nodes)
    point_1, point_2, point_3 = nodes[:3]
    edges = edges_generator()
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=int(edge[2]))
    (dist_to, edge_to) = dijkstra_sp(G, point_1)
    sums = dist_to[point_2]
    (dist_to, edge_to) = dijkstra_sp(G, point_2)
    sums += dist_to[point_3]
    print(sums, point_1, point_2, point_3)
    return sums, edges, point_1, point_2, point_3


nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
k, edges, point_1, point_2, point_3 = exercise_generator
matrix = [['-' for i in range(8)]for j in range(8)]
for i in range(8):
    for j in range(8):
        if i == 0 and j > 0:
            matrix[i][j] = nodes[j-1]
        elif j == 0 and i > 0:
            matrix[i][j] = nodes[i-1]
        for elem in edges:
            n, m = '', ''
            for k in nodes:
                if k == elem[0]:
                    n = elem[0]
                elif k == elem[1]:
                    m = elem[1]
            if n and m:
                matrix[nodes.index(n)+1][nodes.index(m)+1] = elem[2]
                matrix[nodes.index(m)+1][nodes.index(n)+1] = elem[2]
table = prettytable.PrettyTable(matrix[0])
for i in range(1, 8):
    table.add_row(matrix[i])
hello_4 = f'Между населенными пунктами {*nodes,} построены дороги,' \
          f'протяженность которых (в километрах) приведена в таблице ниже. ' \
          f'Определите длину кратчайшего пути между пунктами {point_1} и {point_3},' \
          f'проходящего через пункт {point_2}.\n' \
          f'Передвигаться можно только по дорогам, протяженность ' \
          f'которых указана в таблице.\n' \
          f'{table}'
print(hello_4)
