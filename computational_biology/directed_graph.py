from typing import TypeVar

DiGraphType = TypeVar("DiGraphType", bound="DiGraph")  # TODO: remove in future update
DiGraphType.Node = TypeVar("Node", bound="DiGraph.Node")  # TODO: remove in future update
DiGraphType.Edge = TypeVar("Edge", bound="DiGraph.Edge")  # TODO: remove in future update


class DiGraph:
    """
    This is a simple implementation of the digraph data structure using only the python standard library.
    The string representations are based on the DOT file format.

    Note that "name" and "label" are reserved attributes for the string representation of the graph.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.nodes: set[DiGraphType.Node] = set()
        self.edges: set[DiGraphType.Edge] = set()

    def __str__(self) -> str:
        """
        The digraph is represented with a dot format.

        :return: a string representation of the digraph
        """
        s = "digraph {\n"
        for node in self.nodes:
            s += f"\t{node};\n"
        for edge in self.edges:
            s += f"\t{edge};\n"
        s += "}"
        return s

    def get_nodes(self) -> list[DiGraphType.Node]:
        """
        Creates a list of all nodes in the digraph.

        :return: a list of the node in the digraph
        """
        return list(self.nodes)

    def get_edges(self) -> list[DiGraphType.Edge]:
        """
        Creates a list of all edges in the digraph.

        :return: a list of the edges in the digraph
        """
        return list(self.edges)

    def new_node(self, **kwargs) -> DiGraphType.Node:
        """
        Creates a new node in the digraph.

        :param kwargs: keyword attributes of the node
        :return: the new node
        """
        new_node = DiGraph.Node(**kwargs)
        self.nodes.add(new_node)
        return new_node

    def new_edge(self, tail: DiGraphType.Node, head: DiGraphType.Node, **kwargs) -> DiGraphType.Edge:
        """
        Creates a new edge in the digraph between two existing nodes.

        :param tail: the start/tail node
        :param head: the end/head node
        :param kwargs: keyword attributes of the new edge
        :return: the new edge
        """
        if tail not in self.nodes:
            raise ValueError("tail is not in the current graph")
        if head not in self.nodes:
            raise ValueError("head is not in the current graph")
        new_edge = DiGraph.Edge(tail, head, **kwargs)
        tail.outgoing_edges.add(new_edge)
        head.incoming_edges.add(new_edge)
        self.edges.add(new_edge)
        return new_edge

    def remove_node(self, node: DiGraphType.Node) -> None:
        """
        Removes an existing node and all connected edges from the digraph.

        :param node: the node to remove
        :return: None
        """
        if node not in self.nodes:
            raise ValueError("node is not in the current graph")
        for edge in node.get_edges():
            self.remove_edge(edge)
        self.nodes.remove(node)

    def remove_edge(self, edge: DiGraphType.Edge) -> None:
        """
        Removes the edge from its nodes and the digraph.

        :param edge: the edge to be removed
        :return: None
        """
        if edge not in self.edges:
            raise ValueError("edge is not in the current graph")
        edge.tail.outgoing_edges.remove(edge)
        edge.head.incoming_edges.remove(edge)
        self.edges.remove(edge)

    class Node:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
            self.incoming_edges: set[DiGraphType.Edge] = set()
            self.outgoing_edges: set[DiGraphType.Edge] = set()

        def __str__(self):
            """
            The node is represented with dot file format.

            :return: a string representation of the node
            """
            s = self.name if hasattr(self, "name") else str(id(self))
            if hasattr(self, "label"):
                s += f" [label={self.label}]"
            return s

        def get_incoming_edges(self) -> list[DiGraphType.Edge]:
            """
            Creates a list of all incoming edges in from the node.

            :return: a list of incoming edges
            """
            return list(self.incoming_edges)

        def get_outgoing_edges(self) -> list[DiGraphType.Edge]:
            """
            Creates a list of all outgoing edges in from the node.

            :return: a list of outgoing edges
            """
            return list(self.outgoing_edges)

        def get_edges(self) -> list[DiGraphType.Edge]:
            """
            Creates a list of all edge connect (incoming or outgoing) to the node.

            :return: the list of edges connected to the node
            """
            return list(self.incoming_edges | self.outgoing_edges)

        def get_children(self) -> list[DiGraphType.Node]:
            """
            Creates a list of all nodes connected to the current node via outgoing edges.

            :return: a list of the node's children/destinations
            """
            children = set()
            for edge in self.outgoing_edges:
                children.add(edge.head)
            return list(children)

        def get_parents(self) -> list[DiGraphType.Node]:
            """
            Creates a list of all nodes connected to the current node via incoming edges.

            :return: a list of the node's parents/sources
            """
            parents = set()
            for edge in self.incoming_edges:
                parents.add(edge.tail)
            return list(parents)

        def get_neighbors(self) -> list[DiGraphType.Node]:
            """
            Creates a list of all nodes connected to the current node via incoming or outgoing edges.

            :return: a list of the node's neighbors
            """
            neighbors = set()
            for edge in self.incoming_edges:
                neighbors.add(edge.tail)
            for edge in self.outgoing_edges:
                neighbors.add(edge.head)
            return list(neighbors)

    class Edge:
        def __init__(self, tail: DiGraphType.Node, head: DiGraphType.Node, **kwargs):
            self.__dict__.update(kwargs)
            self.tail: DiGraphType.Node = tail
            self.head: DiGraphType.Node = head

        def __str__(self):
            """
            The edge is represented in the dot file format.

            :return: a string representation of the edge
            """
            tail_name = self.tail.name if hasattr(self.tail, "name") else str(id(self.tail))
            head_name = self.head.name if hasattr(self.head, "name") else str(id(self.head))
            s = f"{tail_name} -> {head_name}"
            if hasattr(self, "label"):
                s += f" [label={self.label}]"
            return s
