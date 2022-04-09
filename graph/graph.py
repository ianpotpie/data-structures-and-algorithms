from typing import TypeVar

GraphType = TypeVar("GraphType", bound="Graph")  # TODO: remove in future update


class Graph:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.nodes: set[GraphType.Node] = set()
        self.edges: set[GraphType.Edge] = set()

    def __str__(self):
        """
        The graph is represented with a dot format.

        :return: a string representation of the graph
        """
        s = "graph {\n"
        for node in self.get_nodes():
            s += f"\t{node}\n"
        for edge in self.get_edges():
            s += f"\t{edge}\n"
        s += "}"
        return s

    def __len__(self):
        """
        Counts the number of nodes in the graph

        :return: the number of nodes in the graph
        """
        return len(self.nodes)

    def __contains__(self, item):
        """
        Checks whether the graph contains a node or edge.

        :param item: a node or edge
        :return: a bool indicating whether the item is in the graph
        """
        if isinstance(item, GraphType.Node):
            return item in self.nodes
        if isinstance(item, GraphType.Edge):
            return item in self.edges
        raise TypeError("Item must be node or edge.")

    def __iter__(self):
        """
        Creates an iterator over the nodes of the graph.

        :return: a node iterator
        """
        return iter(self.nodes)

    def get_nodes(self) -> set[GraphType.Node]:
        """
        Creates a set of all nodes in the graph.

        :return: a set of graph nodes
        """
        return self.nodes.copy()

    def get_edges(self) -> set[GraphType.Edge]:
        """
        Creates a set of all edges in the graph.

        :return: a set of graph edges
        """
        return self.edges.copy()

    def new_node(self, **kwargs) -> GraphType.Node:
        """
        Creates a new node in the graph.

        :param kwargs: keyword attributes of the node
        :return: the new node
        """
        new_node = GraphType.Node(**kwargs)
        self.nodes.add(new_node)
        return new_node

    def new_edge(self, tail: GraphType.Node, head: GraphType.Node, **kwargs) -> GraphType.Edge:
        """
        Creates a new edge in the graph between two existing nodes.

        :param tail: the starting/tail node
        :param head: the ending/head node
        :param kwargs: keyword attributes of the new edge
        :return: the new edge
        """
        assert tail in self.nodes
        assert head in self.nodes
        new_edge = Graph.Edge(tail, head, **kwargs)
        self.edges.add(new_edge)
        return new_edge

    def remove_node(self, node: GraphType.Node) -> None:
        """
        Removes the node and all connected edges from the graph.

        :param node: the node to remove
        :return: None
        """
        assert node in self.nodes
        for edge in self.edges:
            self.remove_edge(edge)
        self.nodes.remove(node)

    def remove_edge(self, edge: GraphType.Edge) -> None:
        """
        Removes the edge from its nodes and the graph.

        :param edge: the edge to be removed
        :return: None
        """
        assert edge in self.edges
        edge.tail.edges.remove(edge)
        if edge.head is not edge.tail:
            edge.head.edges.remove(edge)
        self.edges.remove(edge)

    def adjacent(self, x: GraphType.Node, y: GraphType.Node) -> bool:
        """
        Checks whether two nodes in the graph are adjacent.

        :param x: a node in the graph
        :param y: a node in the graph
        :return: a boolean indicating whether the two nodes are adjacent.
        """
        assert x in self.nodes
        assert y in self.nodes
        is_adjacent = y in x.get_neighbors()
        return is_adjacent

    class Node:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
            self.edges: set[GraphType.Edge] = set()

        def __str__(self):
            """
            The node is represented with dot file format.

            :return: a string representation of the node
            """
            s = f"{id(self)}"
            if hasattr(self, "label"):
                s += f" [label={self.label}]"
            return s

        def get_neighbors(self) -> set[GraphType.Node]:
            """
            Creates a set of neighbors by iterating over the edges of the node.

            :return: a set of the node's neighbors
            """
            neighbors = set()
            for edge in self.edges:
                if edge.tail is self:
                    neighbors.add(edge.head)
                else:
                    neighbors.add(edge.tail)
            return neighbors

        def get_edges(self) -> set[GraphType.Edge]:
            """
            Creates a shallow copy of the set of edges.

            :return: the edges connected to the node
            """
            return self.edges.copy()

    class Edge:
        def __init__(self, tail: GraphType.Node, head: GraphType.Node, **kwargs):
            self.__dict__.update(kwargs)
            self.tail: GraphType.Node = tail
            self.head: GraphType.Node = head

        def __str__(self):
            """
            The edge is represented in the dot file format.

            :return: a string representation of the edge
            """
            s = f"{self.tail} -- {self.head}"
            if hasattr(self, "label"):
                s += f" [label={self.label}]"
            return s
