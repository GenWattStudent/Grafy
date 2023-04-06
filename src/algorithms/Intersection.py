from src.graph.elements.Edge import Edge
from src.graph.elements.Intersection import Intersection
from src.utils.Vector import Vector
from src.Theme import Theme


class FindIntersection:

    def get_edge_node_positions(self, edge: Edge) -> tuple[float, float, float, float]:
        return edge.node1.position.x, edge.node1.position.y, edge.node2.position.x, edge.node2.position.y

    def intersection(self, edge1: Edge, edge2: Edge) -> Intersection:
        x1, y1, x2, y2 = self.get_edge_node_positions(edge1)
        x3, y3, x4, y4 = self.get_edge_node_positions(edge2)

        x = ((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
        y = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))

        return Intersection(Vector(x, y), Theme.get("intersection_color"))

    def intersect(self, edge1: Edge, edge2: Edge, threshold: float = 1e-6) -> bool:
        x1, y1, x2, y2 = self.get_edge_node_positions(edge1)
        x3, y3, x4, y4 = self.get_edge_node_positions(edge2)

        dx1 = x2 - x1
        dy1 = y2 - y1
        dx2 = x4 - x3
        dy2 = y4 - y3
        denom = dy2*dx1 - dx2*dy1
        if denom == 0:
            return False
        ua = (dx2*(y1-y3) - dy2*(x1-x3)) / denom
        ub = (dx1*(y1-y3) - dy1*(x1-x3)) / denom
        if ua < 0 or ua > 1 or ub < 0 or ub > 1:
            return False

        # obliczenie pozycji punktu przecięcia
        x = x1 + ua*dx1
        y = y1 + ua*dy1

        # sprawdzenie, czy przecięcie jest blisko wierzchołka krawędzi
        if (ua <= threshold or ua >= 1-threshold) and \
                ((x-x1)**2 + (y-y1)**2 <= threshold**2 or (x-x2)**2 + (y-y2)**2 <= threshold**2):
            return False
        if (ub <= threshold or ub >= 1-threshold) and \
                ((x-x3)**2 + (y-y3)**2 <= threshold**2 or (x-x4)**2 + (y-y4)**2 <= threshold**2):
            return False

        return True

    def find_intersections(self, edges: list[Edge]) -> list[Intersection]:
        intersections: list[Intersection] = []

        for i in range(len(edges)):
            for j in range(i + 1, len(edges)):
                # if intersection is
                if self.intersect(edges[i], edges[j]):
                    intersections.append(self.intersection(edges[i], edges[j]))
        return intersections
