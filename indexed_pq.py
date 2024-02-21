class IndexedMinPQ:
  def __init__(self, size):
    self.N = 0
    self.size = size
    self.values = [None] * (size+1)
    self.priorities = [None] * (size+1)   # binary heap using 1-based indexing
    self.location = {}                    # For each value, remember its location in storage

  def is_empty(self):
    return self.N == 0

  def swim(self, child):
    while child > 1 and self.less(child//2, child):
      self.swap(child, child//2)
      child = child//2

  def sink(self, parent):
    while 2*parent <= self.N:
      child = 2*parent
      if child < self.N and self.less(child, child+1):
        child += 1
      if not self.less(parent, child):
        break
      self.swap(child, parent)

      parent = child

  def enqueue(self, v, p):
    self.N += 1
    self.values[self.N], self.priorities[self.N] = v, p
    self.location[v] = self.N             # record where it is being stored
    self.swim(self.N)

  def decrease_priority(self, v, lower_priority):
    if not v in self.location:
      raise ValueError('{} not in the indexed min priority queue.'.format(v))
    idx = self.location[v]
    if lower_priority >= self.priorities[idx]:
      raise RuntimeError('Value {} has existing priority of {} which is already lower'
                         ' than {}'.format(v, self.priorities[idx], lower_priority))

    self.priorities[idx] = lower_priority
    self.swim(idx)

  def less(self, i, j):
    return self.priorities[i] > self.priorities[j]

  def swap(self, i, j):
    self.values[i], self.values[j] = self.values[j], self.values[i]
    self.priorities[i], self.priorities[j] = self.priorities[j], self.priorities[i]

    self.location[self.values[i]] = i
    self.location[self.values[j]] = j

  def dequeue(self):
    min_value = self.values[1]
    self.values[1] = self.values[self.N]
    self.priorities[1] = self.priorities[self.N]
    self.location[self.values[1]] = 1

    self.values[self.N] = self.priorities[self.N] = None
    self.location.pop(min_value)   # remove from dictionary

    self.N -= 1
    self.sink(1)
    return min_value
