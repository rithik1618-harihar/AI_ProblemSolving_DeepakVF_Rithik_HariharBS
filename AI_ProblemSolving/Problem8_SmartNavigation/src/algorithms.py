"""
Smart Navigation System - BFS and DFS Algorithms
Problem 8: AI Problem Solving Assignment
"""

from collections import deque


class Graph:
    """Undirected graph represented as an adjacency list."""

    def __init__(self):
        self.adjacency_list = {}

    def add_node(self, node: str):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, node1: str, node2: str):
        self.add_node(node1)
        self.add_node(node2)
        if node2 not in self.adjacency_list[node1]:
            self.adjacency_list[node1].append(node2)
        if node1 not in self.adjacency_list[node2]:
            self.adjacency_list[node2].append(node1)

    def get_neighbors(self, node: str):
        return sorted(self.adjacency_list.get(node, []))

    def get_nodes(self):
        return list(self.adjacency_list.keys())

    def get_edges(self):
        edges = []
        seen = set()
        for node, neighbors in self.adjacency_list.items():
            for nb in neighbors:
                key = tuple(sorted([node, nb]))
                if key not in seen:
                    edges.append(list(key))
                    seen.add(key)
        return edges


# ─────────────────────────────────────────────
#  BFS  (Breadth-First Search)
# ─────────────────────────────────────────────

def bfs(graph: Graph, start: str, goal: str) -> dict:
    """
    Breadth-First Search — explores level by level.
    Guarantees the shortest path (fewest hops).

    Returns a dict with:
        path        : list of nodes from start → goal (or None)
        explored    : order in which nodes were visited
        nodes_count : total nodes explored
        is_shortest : always True for BFS
    """
    if start not in graph.adjacency_list or goal not in graph.adjacency_list:
        return {"path": None, "explored": [], "nodes_count": 0, "is_shortest": True}

    visited = {start}
    queue = deque([(start, [start])])
    explored_order = []

    while queue:
        current, path = queue.popleft()
        explored_order.append(current)

        if current == goal:
            return {
                "path": path,
                "explored": explored_order,
                "nodes_count": len(explored_order),
                "is_shortest": True,
            }

        for neighbor in graph.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return {"path": None, "explored": explored_order, "nodes_count": len(explored_order), "is_shortest": True}


# ─────────────────────────────────────────────
#  DFS  (Depth-First Search)
# ─────────────────────────────────────────────

def dfs(graph: Graph, start: str, goal: str) -> dict:
    """
    Depth-First Search — goes as deep as possible first.
    Finds *a* path but does NOT guarantee shortest.

    Returns a dict with:
        path        : list of nodes from start → goal (or None)
        explored    : order in which nodes were visited
        nodes_count : total nodes explored
        is_shortest : False (DFS does not guarantee this)
    """
    if start not in graph.adjacency_list or goal not in graph.adjacency_list:
        return {"path": None, "explored": [], "nodes_count": 0, "is_shortest": False}

    explored_order = []

    def _dfs_recursive(node: str, path: list, visited: set):
        visited.add(node)
        explored_order.append(node)

        if node == goal:
            return path

        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                result = _dfs_recursive(neighbor, path + [neighbor], visited)
                if result is not None:
                    return result
        return None

    path = _dfs_recursive(start, [start], set())

    return {
        "path": path,
        "explored": explored_order,
        "nodes_count": len(explored_order),
        "is_shortest": False,
    }


# ─────────────────────────────────────────────
#  Comparison helper
# ─────────────────────────────────────────────

def compare_algorithms(graph: Graph, start: str, goal: str) -> dict:
    """Run both algorithms and return a side-by-side comparison."""
    bfs_result = bfs(graph, start, goal)
    dfs_result = dfs(graph, start, goal)

    bfs_len = len(bfs_result["path"]) - 1 if bfs_result["path"] else None
    dfs_len = len(dfs_result["path"]) - 1 if dfs_result["path"] else None

    return {
        "bfs": bfs_result,
        "dfs": dfs_result,
        "comparison": {
            "bfs_path_length": bfs_len,
            "dfs_path_length": dfs_len,
            "bfs_nodes_explored": bfs_result["nodes_count"],
            "dfs_nodes_explored": dfs_result["nodes_count"],
            "bfs_is_optimal": True,
            "shorter_path_by": (
                dfs_len - bfs_len
                if bfs_len is not None and dfs_len is not None
                else None
            ),
        },
    }
