from collections import defaultdict
from src.graph.elements.Edge import Edge
from src.graph.elements.Intersection import Intersection
from src.utils.Vector import Vector
from src.Theme import theme


class FindIntersection:

    def get_edge_node_positions(self, edge: Edge) -> tuple[float, float, float, float]:
        return edge.start_point.x, edge.start_point.y, edge.end_point.x, edge.end_point.y

    def intersection(self, edge1: Edge, edge2: Edge) -> Intersection:
        x1, y1, x2, y2 = self.get_edge_node_positions(edge1)
        x3, y3, x4, y4 = self.get_edge_node_positions(edge2)

        x = ((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
        y = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))

        return Intersection(Vector(x, y), theme.get("warning"))

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

        x = x1 + ua*dx1
        y = y1 + ua*dy1

        if (ua <= threshold or ua >= 1-threshold) and \
                ((x-x1)**2 + (y-y1)**2 <= threshold**2 or (x-x2)**2 + (y-y2)**2 <= threshold**2):
            return False
        if (ub <= threshold or ub >= 1-threshold) and \
                ((x-x3)**2 + (y-y3)**2 <= threshold**2 or (x-x4)**2 + (y-y4)**2 <= threshold**2):
            return False

        return True

    def find_intersections(self, edges: list[Edge], threshold: float = 25) -> list[Intersection]:
            intersections: list[Intersection] = []
            intersection_groups = defaultdict(list)

            for i in range(len(edges)):
                for j in range(i + 1, len(edges)):
                    if self.intersect(edges[i], edges[j], threshold):
                        intersection = self.intersection(edges[i], edges[j])
                        intersections.append(intersection)

                        # Check if the intersection is close to any existing group
                        for group_center, group_intersections in intersection_groups.items():
                            if self.is_close_to_group(intersection.position, group_center, threshold):
                                group_intersections.append(intersection)
                                break
                        else:
                            # If not close to any existing group, create a new group
                            intersection_groups[intersection.position].append(intersection)

            # Create a single intersection for each group
            grouped_intersections = []
            for group_intersections in intersection_groups.values():
                group_center = group_intersections[0].position
                group_size = len(group_intersections)
                radius = 12 + group_size
                if radius > 36:
                    radius = 36
                grouped_intersection = Intersection(group_center, theme.get("warning"), radius, group_size)
                grouped_intersections.append(grouped_intersection)

            return grouped_intersections

    def is_close_to_group(self, position: Vector, group_center: Vector, threshold: float) -> bool:
        squared_distance = (position.x - group_center.x) ** 2 + (position.y - group_center.y) ** 2
        return squared_distance <= threshold ** 2
