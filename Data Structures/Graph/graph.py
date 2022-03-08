class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def insert_node(self, node):
        self.nodes.add(node)

    def insert_edge(self, edge):
        assert edge.start in self.nodes
        assert edge.end in self.nodes
        self.edges.add(edge)
        edge.node1.edges.add(edge)
        edge.node2.edges.add(edge)

    def remove_node(self, node):
        assert node in self.nodes
        for edge in node.edges:
            self.remove_edge(edge)
        self.nodes.remove(node)

    def remove_edge(self, edge):
        assert edge in self.edges
        edge.node1.edges.remove(edge)
        edge.node2.edges.remove(edge)
        self.edges.remove(edge)

    class Node:
        def __init__(self, value):
            self.value = value
            self.edges = set()

    class Edge:
        def __init__(self, value, node1, node2):
            self.value = value
            self.node1 = node1
            self.node2 = node2
