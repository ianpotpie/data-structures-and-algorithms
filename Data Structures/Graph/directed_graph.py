from graph import Graph


class DirectedGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def insert_node(self, node):
        self.nodes.add(node)

    def insert_edge(self, edge):
        assert edge.start in self.nodes
        assert edge.end in self.nodes
        self.edges.add(edge)
        edge.start.edges.add(edge)
        edge.start.out_edges.add(edge)
        edge.end.edges.add(edge)
        edge.end.in_edges.add(edge)

    def remove_node(self, node):
        assert node in self.nodes
        for edge in node.edges:
            self.remove_edge(edge)
        self.nodes.remove(node)

    def remove_edge(self, edge):
        assert edge in self.edges
        edge.start.out_edges.remove(edge)
        edge.start.edges.remove(edge)
        edge.end.in_edges.remove(edge)
        if edge.start is not edge.end:
            edge.end.edges.remove(edge)
        self.edges.remove(edge)

    class Node:
        def __init__(self, value):
            self.value = value
            self.in_edges = set()
            self.out_edges = set()

    class Edge:
        def __init__(self, value, start, end):
            self.value = value
            self.start = start
            self.end = end
