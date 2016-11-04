import pickle
from collections import deque
import heapq
import time

with open("map1.pkl", 'rb') as f:
    map1 = pickle.load(f)


def breadth_search_distance(start, finish):
    """Calculate graph distance between two points.


    Args:
        start (Tuple(int, int)): start point
        finish (Tuple(int, int)): end point

    Returns:
        int: graph distance
    """
    nodes = deque()
    nodes.append((start, 0))
    visited = set()

    while nodes:
        n = nodes.popleft()
        cell = n[0]
        level = n[1]
        visited.add(cell)
        neighbors = map1[cell]
        for neigh in neighbors:
            if neigh == finish:
                return level + 1
            elif neigh not in visited:
                nodes.append((neigh, level + 1))


def manh_dist(p1, p2):
    """Compute manhatan distance between two points.

    Args:
        p1 (Tuple(int, int)): point 1
        p2 (Tuple(int, int)): point 2

    Returns:
        int: distance
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def dijkstra_search_distance(start, finish):
    """Calculate graph distance between two points.

    Args:
        start (Tuple(int, int)): start point
        finish (Tuple(int, int)): end point

    Returns:
        TYPE: graph distance
    """
    nodes = []
    heapq.heappush(nodes, (manh_dist(start, finish), (start, 0, 0)))
    visited = set()
    cost_so_far = {}

    while nodes:
        n = heapq.heappop(nodes)[1]
        cell = n[0]
        level = n[1]
        cost = n[2]
        visited.add(cell)
        neighbors = map1[cell]
        for neigh in neighbors:
            if neigh == finish:
                return level + 1
            elif neigh not in visited:
                priority = cost + 1 + manh_dist(neigh, finish)
                node = (neigh, level + 1, cost + 1)
                heapq.heappush(nodes, (priority, node))


if __name__ == "__main__":
    t = time.time()
    print(breadth_search_distance((18, 2), (158, 158)))
    print(time.time() - t)
    t = time.time()
    print(dijkstra_search_distance((18, 2), (158, 158)))
    print(time.time() - t)
