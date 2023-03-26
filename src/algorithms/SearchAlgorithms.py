import numpy as np
import heapq
from src.graph.GraphMatrix import GraphMatrix
from src.graph.Node import Node


class SearchAlgorithms:
    def bfs(self, matrix: dict[int, list[int]], start: Node) -> dict[int, list[int]]:
        node_id = int(start.index) - 1

        visited = set()
        queue = [node_id]
        tree = {node_id: []}

        while queue:
            node = queue.pop(0)
            visited.add(node)

            for neighbor in matrix[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    if neighbor not in tree:
                        tree[neighbor] = []
                    tree[node].append(neighbor)
                    tree[neighbor].append(node)

        return tree

    def dfs(self, matrix: dict[int, list[int]], start: Node) -> dict[int, list[int]]:
        node_id = int(start.index) - 1  # indeks wierzchołka startowego
        visited = {node_id: []}  # słownik przechowujący informację o odwiedzonych wierzchołkach i ich przodkach

        def dfs_visit(node, parent):
            visited[node].append(parent)
            for neighbor in matrix[node]:
                if neighbor not in visited:
                    visited[neighbor] = []
                    dfs_visit(neighbor, node)  # rekurencyjnie wywołaj dfs_visit dla nieodwiedzonego sąsiada

        dfs_visit(node_id, None)  # wywołaj dfs_visit dla startowego wierzchołka
        return visited

    def dijkstra(self, matrix: GraphMatrix, start: Node, end: Node) -> tuple[float, list[int]]:
        n = len(matrix)
        distances = np.full(n, np.inf)
        visited = np.zeros(n, dtype=bool)
        previous = np.full(n, None)

        distances[int(start.index) - 1] = 0

        heap = [(0, int(start.index) - 1)]

        while heap:
            (current_distance, current_node) = heapq.heappop(heap)
            visited[current_node] = True

            if current_node == int(end.index) - 1:
                path = []
                total_distance = current_distance

                while previous[current_node] is not None:
                    path.insert(0, current_node)
                    current_node = previous[current_node]

                path.insert(0, int(start.index) - 1)
                return total_distance, path

            for neighbor in range(n):
                if matrix[current_node][neighbor] != 0 and not visited[neighbor]:
                    tentative_distance = distances[current_node] + matrix[current_node][neighbor]
                    if tentative_distance < distances[neighbor]:
                        distances[neighbor] = tentative_distance
                        previous[neighbor] = current_node
                        heapq.heappush(heap, (tentative_distance, neighbor))

        return np.inf, []
