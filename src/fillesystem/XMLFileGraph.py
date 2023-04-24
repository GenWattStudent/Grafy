from src.GraphFile import FileManager
from src.graph.GraphModel import GraphModel, Graph
from xml.etree.ElementTree import Element, SubElement, ElementTree, parse
from src.graph.elements.Node import Node
from src.graph.elements.Edge import Edge
from src.graph.GraphConfig import GraphConfig
from src.utils.Vector import Vector
from src.Theme import Theme
import uuid

class XMLFileGraph(FileManager):
    def save(self, graph: GraphModel, path: str):
        # sue xml tree to save graph
        root = Element('graph')
        for node in graph.nodes:
            # create node element
            node_element = SubElement(root, 'node')
            node_element.set('id', str(node.id))
            node_element.set('x', str(node.position.x))
            node_element.set('y', str(node.position.y))
            node_element.set('index', str(node.index))

        for edge in graph.edges:
            # create edge element
            edge_element = SubElement(root, 'edge')
            edge_element.set('id', str(edge.id))
            edge_element.set('from', str(edge.node1.id))
            edge_element.set('to', str(edge.node2.id))
        
        tree = ElementTree(root)
        tree.write(path)

    def load(self, path: str) -> GraphModel:
        # use xml tree to load graph
        tree = parse(path)
        root = tree.getroot()
        config = GraphConfig()
        config.number_of_nodes = 0
    
        graph = Graph(config)
        for node in root.findall('node'):
            if node is None:
                continue
            vector = Vector(float(node.get('x')), float(node.get('y')))
            node_el = Node(vector, int(node.get('index')), 15, Theme.get("node_color"), Theme.get("node_selected_color"))
            node_el.id = uuid.UUID(node.get('id'))
            graph.add_node(node_el)
        for edge in root.findall('edge'):
            if edge is None:
                continue
            
            node1 = next(node for node in graph.nodes if node.id == uuid.UUID(edge.get('from')))
            node2 = next(node for node in graph.nodes if node.id == uuid.UUID(edge.get('to')))
            edge_el = Edge(node1, node2)
            edge_el.id = str(edge.get('id'))
            graph.add_edge(edge_el)

        return graph
