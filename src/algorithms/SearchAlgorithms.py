import numpy as np
import heapq
from src.graph.GraphMatrix import GraphMatrix
from src.graph.elements.Node import Node
from collections import defaultdict


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

   
    def get_layers_from_bfs_output(self, bfs_output, starting_vertex: int):
        layers = defaultdict(list)
        layers[0] = [starting_vertex]
        visited = set([starting_vertex])
        queue: list[tuple[int, int]] = [(starting_vertex, 0)] 

        while queue:
            vertex, layer = queue.pop(0)
            adjacent_vertices = bfs_output[vertex]
            for adjacent_vertex in adjacent_vertices:
                if adjacent_vertex not in visited:
                    visited.add(adjacent_vertex)
                    queue.append((adjacent_vertex, layer + 1))
                    layers[layer + 1].append(adjacent_vertex)

        return sorted(layers.items())

    def dfs(self, matrix: dict[int, list[int]], start: Node) -> dict[int, list[int]]:
        node_id = int(start.index) - 1 
        visited = {node_id: []}  

        def dfs_visit(node, parent):
            visited[node].append(parent)
            for neighbor in matrix[node]:
                if neighbor not in visited:
                    visited[neighbor] = []
                    dfs_visit(neighbor, node) 

        dfs_visit(node_id, None)
        return visited
    
    def count_cycles(self, matrix: dict[int, list[int]]) -> int:
        cycle_count = 0

        def dfs(node, visited, parent):
            nonlocal cycle_count

            visited[node] = True

            for neighbor in matrix[node]:
                if not visited[neighbor]:
                    dfs(neighbor, visited, node)
                elif neighbor != parent:
                    cycle_count += 1

        visited = {node: False for node in matrix}
        
        for node in matrix:
            if not visited[node]:
                dfs(node, visited, None)

        return cycle_count

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
