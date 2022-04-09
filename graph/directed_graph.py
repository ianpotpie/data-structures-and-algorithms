from typing import TypeVar, Union, Iterator

DiGraphType = TypeVar("DiGraphType", bound="DiGraph")  # TODO: remove in future update


class DiGraph:
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
            s += f"\t{node}\n"
        for edge in self.get_edges():
            s += f"\t{edge}\n"
        s += "}"
        return s

    def __len__(self) -> len:
        """
        Counts the number of nodes in the digraph

        :return: the number of nodes in the digraph
        """
        return len(self.nodes)

    def __contains__(self, item: Union[DiGraphType.Node, DiGraphType.Edge]) -> bool:
        """
        Checks whether the digraph contains a node or edge.

        :param item: a node or edge
        :return: a bool indicating whether the item is in the digraph
        """
        if isinstance(item, DiGraphType.Node):
            return item in self.nodes
        if isinstance(item, DiGraphType.Edge):
            return item in self.edges
        raise TypeError("Item must be node or edge.")

    def __iter__(self) -> Iterator[DiGraphType.Node]:
        """
        Creates an iterator over the nodes of the digraph.

        :return: a node iterator
        """
        return iter(self.nodes)

    def get_nodes(self) -> set[DiGraphType.Node]:
        """
        Creates a set of all nodes in the digraph.

        :return: a set of digraph nodes
        """
        return self.nodes.copy()

    def get_edges(self) -> set[DiGraphType.Edge]:
        """
        Creates a set of all edges in the digraph.

        :return: a set of digraph edges
        """
        return self.edges.copy()

    def new_node(self, **kwargs) -> DiGraphType.Node:
        """
        Creates a new node in the digraph.

        :param kwargs: keyword attributes of the node
        :return: the new node
        """
        new_node = DiGraphType.Node(**kwargs)
        self.nodes.add(new_node)
        return new_node

    def new_edge(self, tail: DiGraphType.Node, head: DiGraphType.Node, **kwargs) -> DiGraphType.Edge:
        """
        Creates a new edge in the digraph between two existing nodes.

        :param tail: the starting/tail node
        :param head: the ending/head node
        :param kwargs: keyword attributes of the new edge
        :return: the new edge
        """
        assert tail in self.nodes
        assert head in self.nodes
        new_edge = DiGraph.Edge(tail, head, **kwargs)
        tail.outgoing_edges.add(new_edge)
        head.incoming_edges.add(new_edge)
        self.edges.add(new_edge)
        return new_edge

    def remove_node(self, node: DiGraphType.Node) -> None:
        """
        Removes the node and all connected edges from the digraph.

        :param node: the node to remove
        :return: None
        """
        assert node in self.nodes
        for edge in node.get_edges():
            self.remove_edge(edge)
        self.nodes.remove(node)

    def remove_edge(self, edge: DiGraphType.Edge) -> None:
        """
        Removes the edge from its nodes and the digraph.

        :param edge: the edge to be removed
        :return: None
        """
        assert edge in self.edges
        edge.tail.outgoing_edges.remove(edge)
        edge.head.incoming_edges.remove(edge)
        self.edges.remove(edge)

    def adjacent(self, x: DiGraphType.Node, y: DiGraphType.Node) -> bool:
        """
        Checks whether two nodes in the digraph are adjacent.

        :param x: a node in the digraph
        :param y: a node in the digraph
        :return: a boolean indicating whether the two nodes are adjacent.
        """
        assert x in self.nodes
        assert y in self.nodes
        is_adjacent = y in x.get_neighbors()
        return is_adjacent

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
            s = f"{id(self)}"
            if hasattr(self, "label"):
                s += f" [label={self.label}]"
            return s

        def get_neighbors(self) -> set[DiGraphType.Node]:
            """
            Creates a set of neighbors by iterating over the edges of the node.

            :return: a set of the node's neighbors
            """
            neighbors = set()
            for edge in self.outgoing_edges:
                neighbors.add(edge.head)
            return neighbors

        def get_edges(self) -> set[DiGraphType.Edge]:
            """
            Creates a shallow copy of the set of edges.

            :return: the edges connected to the node
            """
            return self.incoming_edges | self.outgoing_edges

        def get_incoming_edges(self) -> set[DiGraphType.Edge]:
            """
            Creates a shallow copy of the incoming set of edges.

            :return: the incoming edges of the node
            """
            return self.incoming_edges.copy()

        def get_outgoing_edges(self) -> set[DiGraphType.Edge]:
            """
            Creates a shallow copy of the outgoing set of edges.

            :return: the outgoing edges of the node
            """
            return self.outgoing_edges.copy()

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
            s = f"{self.tail} -> {self.head}"
            if hasattr(self, "label"):
                s += f" [label={self.label}]"
            return s
