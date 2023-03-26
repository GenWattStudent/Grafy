from .layout import Layout
import random
import math


class TarjanSCC(Layout):
    def __init__(self, graph, width, height, k=1.0, iterations=50):
        self.graph = graph
        self.width = width
        self.height = height
        self.k = k
        self.iterations = iterations
        self.nodes = {}
        self.edges = []

    def run(self):
        # Initialize positions of nodes randomly
        for node in self.graph.nodes:
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            self.nodes[node] = (x, y)

        # Compute optimal node positions
        for i in range(self.iterations):
            dx = [0.0] * len(self.graph.nodes)
            dy = [0.0] * len(self.graph.nodes)

            # Compute repulsive forces between nodes
            for n1, (x1, y1) in self.nodes.items():
                for n2, (x2, y2) in self.nodes.items():
                    if n1 != n2:
                        d = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                        f = self.k ** 2 / d
                        dx[n1] += f * (x1 - x2) / d
                        dy[n1] += f * (y1 - y2) / d

            # Compute spring forces between connected nodes
            for edge in self.graph.edges:
                n1 = edge[0]
                n2 = edge[1]
                x1, y1 = self.nodes[n1]
                x2, y2 = self.nodes[n2]
                d = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                f = self.k * d
                dx[n1] -= f * (x1 - x2) / d
                dy[n1] -= f * (y1 - y2) / d
                dx[n2] += f * (x1 - x2) / d
                dy[n2] += f * (y1 - y2) / d

            # Limit maximum displacement
            for n in self.nodes:
                d = math.sqrt(dx[n] ** 2 + dy[n] ** 2)
                if d > self.k:
                    dx[n] *= self.k / d
                    dy[n] *= self.k / d

            # Update node positions
            for n, (x, y) in self.nodes.items():
                self.nodes[n] = (x + dx[n], y + dy[n])
