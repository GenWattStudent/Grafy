import numpy as np
import heapq
from src.graph.GraphMatrix import GraphMatrix
from src.graph.Node import Node


class SearchAlgorithms:
    def bfs(self, matrix: GraphMatrix, start: Node, end: Node) -> tuple[float, list[int]]:
        n = len(matrix)
        visited = np.zeros(n, dtype=bool)
        previous = np.full(n, None)

        queue = [int(start.index) - 1]
        visited[int(start.index) - 1] = True
        distances = np.full(n, np.inf)
        distances[int(start.index) - 1] = 0

        heap = [(0, int(start.index) - 1)]

        while queue:
            current_node = queue.pop(0)

            if current_node == int(end.index) - 1:
                (current_distance, d) = heapq.heappop(heap)
                total_distance = current_distance
                path = []

                while previous[current_node] is not None:
                    path.insert(0, current_node)
                    current_node = previous[current_node]

                path.insert(0, int(start.index) - 1)
                return total_distance, path

            for neighbor in range(n):
                if matrix[current_node][neighbor] != 0 and not visited[neighbor]:
                    visited[neighbor] = True
                    previous[neighbor] = current_node
                    queue.append(neighbor)

        return np.inf, []

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
