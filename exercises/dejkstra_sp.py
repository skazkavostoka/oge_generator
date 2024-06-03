from indexed_pq import IndexedMinPQ
from random import shuffle, randint


def dijkstra_sp(G, src):
  N = G.number_of_nodes()
  inf = float('inf')
  dist_to = {v:inf for v in G.nodes()}
  dist_to[src] = 0

  impq = IndexedMinPQ(N)
  impq.enqueue(src, dist_to[src])
  for v in G.nodes():
    if v != src:
      impq.enqueue(v, inf)

  def relax(e):
    u, v, weight = e[0], e[1], e[2]['weight']
    if dist_to[u] + weight < dist_to[v]:
      dist_to[v] = dist_to[u] + weight
      edge_to[v] = e
      impq.decrease_priority(v, dist_to[v])

  edge_to = {}
  while not impq.is_empty():
    n = impq.dequeue()
    for e in G.edges(n, data=True):
      relax(e)

  return (dist_to, edge_to)

def edges_path_to(edge_to, src, target):
  if not target in edge_to:
    raise ValueError('{} is unreachable from {}'.format(target, src))

  path = []
  v = target
  while v != src:
    path.append(v)
    v = edge_to[v][0]

  # last one to push is the source, which makes it
  # the first one to be retrieved
  path.append(src)
  path.reverse()
  return path


def edges_generator():
  i = 1
  nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
  edges = []
  while i < 11:
    shuffle(nodes)
    if nodes[:2] not in edges:
      edges.append(nodes[:2] + [str(randint(1, 14))])
      i += 1
  return edges

def try_recursion(f):
  def wrapper(*args, **kwargs):
    steps = 10
    while steps:
      try:
        return f(*args, **kwargs)
      except Exception:
        steps -= 1
  return wrapper()
