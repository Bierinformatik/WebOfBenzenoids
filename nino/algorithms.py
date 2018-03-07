__author__ = 'Nino Bašić <nino.basic@fmf.uni-lj.si>'
__version__ = '0.1'


import collections  # Used by the BFS and DFS algorithms.


def bfs(start, neighbors):
    """
    General breadth first search algorithm.
    """
    component = []
    seen = {start}
    queue = collections.deque([start])
    while len(queue) > 0:
        node = queue.popleft()
        component.append(node)
        for w in neighbors(node):
            if w in seen:
                continue  # Skip nodes which we already encountered.
            seen.add(w)
            queue.append(w)
    return component


def dfs(start, neighbors):
    """
    General depth first search algorithm.
    """
    component = []
    seen = {start}
    queue = collections.deque([start])
    while len(queue) > 0:
        node = queue.pop()
        component.append(node)
        for w in neighbors(node):
            if w in seen:
                continue  # Skip nodes which we already encountered.
            seen.add(w)
            queue.append(w)
    return component
