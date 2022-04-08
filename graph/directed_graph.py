from typing import TypeVar, Optional

DiGraphType = TypeVar("DiGraphType", bound="DiGraph")


class DiGraph:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.nodes_by_name: dict[str, DiGraph.Node] = dict()
        self.edges_by_tail: dict[str, set[DiGraph.Edge]] = dict()
        self.edges_by_head: dict[str, set[DiGraph.Edge]] = dict()

    def __str__(self):
        s = "digraph {\n"
        for node in self.get_nodes():
            s += f"\t{node}\n"
        for edge in self.get_edges():
            s += f"\t{edge}\n"
        s += "}"
        return s

    def get_names(self) -> set[str]:
        """
        Creates a set of all node name in the graph.

        :return: a set of names
        """
        return set(self.nodes_by_name.keys())

    def get_nodes(self) -> set[DiGraphType.Node]:
        """
        Creates a set of all nodes in the graph.

        :return: a set of graph nodes
        """
        return set(self.nodes_by_name.values())

    def get_edges(self) -> set[DiGraphType.Edge]:
        """
        Creates a set of all edges in the graph.

        :return: a set of graph edges
        """
        edges = set()
        for name in self.nodes_by_name:
            edges.update(self.edges_by_tail[name])
        return edges

    def new_node(self, name: str, label: Optional[str] = None, **kwargs):
        """
        Creates a new node in the graph.

        :param name: the name of the new node
        :param label: the optional label of the node
        :param kwargs: keyword attributes of the node
        :return: None
        """
        assert name not in self.nodes_by_name
        new_node = DiGraph.Node(name, label, **kwargs)
        self.nodes_by_name[name] = new_node
        self.edges_by_tail[name] = set()
        self.edges_by_head[name] = set()

    def new_edge(self, tail_name: str, head_name: str, label: Optional[str] = None, **kwargs):
        """
        Creates a new edge in the graph.

        :param tail_name: the starting/tail node
        :param head_name: the ending/head node
        :param label: the optional label of the edge
        :param kwargs: keyword attributes of the new edge
        :return: None
        """
        assert tail_name in self.nodes_by_name
        assert head_name in self.nodes_by_name
        new_edge = DiGraph.Edge(tail_name, head_name, label, **kwargs)
        self.edges_by_tail[tail_name].add(new_edge)
        self.edges_by_head[head_name].add(new_edge)

    def remove_name(self, name: str):
        """
        Removes the node with the given name and all connected edges from the graph.

        :param name: the name of a node
        :return: None
        """
        assert name in self.nodes_by_name
        for edge in self.edges_by_tail[name]:
            self.remove_edge(edge)
        for edge in self.edges_by_head[name]:
            self.remove_edge(edge)
        del self.edges_by_tail[name]
        del self.edges_by_head[name]
        del self.nodes_by_name[name]

    def remove_node(self, node: DiGraphType.Node):
        """
        Removes the node and all connected edges from the graph.

        :param node: the node to remove
        :return: None
        """
        assert node.name in self.nodes_by_name
        assert self.nodes_by_name[node.name] is node
        for edge in self.edges_by_tail[node.name]:
            self.remove_edge(edge)
        for edge in self.edges_by_head[node.name]:
            self.remove_edge(edge)
        del self.edges_by_tail[node.name]
        del self.edges_by_head[node.name]
        del self.nodes_by_name[node.name]

    def remove_edge(self, edge: DiGraphType.Edge):
        """
        Removes the edge from its nodes and the graph.

        :param edge: the edge to be removed
        :return: None
        """
        assert edge in self.edges_by_tail[edge.tail_name]
        assert edge in self.edges_by_head[edge.head_name]
        self.edges_by_tail[edge.tail_name].remove(edge)
        self.edges_by_head[edge.head_name].remove(edge)

    def get_node(self, name):
        """
        Gets the node with the given name.

        :param name: the name of the node
        :return: a graph node
        """
        return self.nodes_by_name[name]

    def get_outgoing_edges(self, name):
        """
        Finds all the outgoing edges connected to a node.

        :param name: the name of the node
        :return: a set of edges
        """
        return self.edges_by_tail[name].copy()

    def get_incoming_edges(self, name):
        """
        Finds all the incoming edges connected to a node.

        :param name: the name of the node
        :return: a set of edges
        """
        return self.edges_by_head[name].copy()

    class Node:
        def __init__(self, name, label=None, **kwargs):
            self.__dict__.update(kwargs)
            self.name: str = name
            self.label: str = label

        def __str__(self):
            s = f"{self.name}"
            if self.label is not None:
                s += f" [label={self.label}]"
            return s

    class Edge:
        def __init__(self, tail_name, head_name, label=None, **kwargs):
            self.__dict__.update(kwargs)
            self.tail_name: str = tail_name
            self.head_name: str = head_name
            self.label: str = label

        def __str__(self):
            s = f"{self.tail_name} -> {self.head_name}"
            if self.label is not None:
                s += f" [label={self.label}]"
            return s
