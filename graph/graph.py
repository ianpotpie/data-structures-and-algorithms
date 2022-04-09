import argparse
from typing import TypeVar

GraphType = TypeVar("GraphType", bound="Graph")  # TODO: remove in future update
GraphType.Node = TypeVar("Node", bound="Graph.Node")  # TODO: remove in future update
GraphType.Edge = TypeVar("Edge", bound="Graph.Edge")  # TODO: remove in future update


class Graph:
    """
    This is a simple implementation of the graph data structure using only the python standard library.
    The string representations are based on the DOT file format.

    Note that "name" and "label" are reserved attributes for the string representation of the graph.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.nodes: set[GraphType.Node] = set()
        self.edges: set[GraphType.Edge] = set()

    def __str__(self) -> str:
        """
        The graph is represented with a dot format.

        :return: a string representation of the graph
        """
        s = "graph {\n"
        for node in self.nodes:
            s += f"\t{node};\n"
        for edge in self.edges:
            s += f"\t{edge};\n"
        s += "}"
        return s

    def get_nodes(self) -> list[GraphType.Node]:
        """
        Creates a list of all nodes in the graph.

        :return: a set of graph nodes
        """
        return list(self.nodes)

    def get_edges(self) -> list[GraphType.Edge]:
        """
        Creates a list of all edges in the graph.

        :return: a set of graph edges
        """
        return list(self.edges)

    def new_node(self, **kwargs) -> GraphType.Node:
        """
        Creates a new node in the graph.

        :param kwargs: keyword attributes of the node
        :return: the new node
        """
        new_node = Graph.Node(**kwargs)
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
        if tail not in self.nodes:
            raise ValueError("tail is not in the current graph")
        if head not in self.nodes:
            raise ValueError("head is not in the current graph")
        new_edge = Graph.Edge(tail, head, **kwargs)
        tail.edges.add(new_edge)
        head.edges.add(new_edge)
        self.edges.add(new_edge)
        return new_edge

    def remove_node(self, node: GraphType.Node) -> None:
        """
        Removes the node and all connected edges from the graph.

        :param node: the node to remove
        :return: None
        """
        if node not in self.nodes:
            raise ValueError("node is not in the current graph")
        for edge in node.get_edges():
            self.remove_edge(edge)
        self.nodes.remove(node)

    def remove_edge(self, edge: GraphType.Edge) -> None:
        """
        Removes the edge from its nodes and the graph.

        :param edge: the edge to be removed
        :return: None
        """
        if edge not in self.edges:
            raise ValueError("edge is not in the current graph")
        edge.tail.edges.remove(edge)
        if edge.head is not edge.tail:
            edge.head.edges.remove(edge)
        self.edges.remove(edge)

    class Node:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
            self.edges: set[GraphType.Edge] = set()

        def __str__(self):
            """
            The node is represented with dot file format.

            :return: a string representation of the node
            """
            s = self.name if hasattr(self, "name") else str(id(self))
            if hasattr(self, "label"):
                s += f" [label={self.label}]"
            return s

        def get_edges(self) -> list[GraphType.Edge]:
            """
            Creates a shallow copy of the set of edges.

            :return: the edges connected to the node
            """
            return list(self.edges)

        def get_neighbors(self) -> list[GraphType.Node]:
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
            return list(neighbors)

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
            tail_name = self.tail.name if hasattr(self.tail, "name") else str(id(self.tail))
            head_name = self.head.name if hasattr(self.head, "name") else str(id(self.head))
            s = f"{tail_name} -- {head_name}"
            if hasattr(self, "label"):
                s += f" [label={self.label}]"
            return s


def main():
    graph = Graph()
    nodes_by_name = {}
    edges_by_name = {}

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-l", "--label")
    parser.add_argument("-n", "--name")

    print("~Graph Builder REPL~")
    print("-------------------")
    print("Commands:")
    print("1. add-node [-n, --name] [-l, --label]")
    print("2. add-edge [-n, --name] [-l, --label]")
    print("3. del-node [name]")
    print("4. del-edge [name]")
    print("5. node-dict")
    print("6. edge-dict")
    print("7. reset-graph")
    print("8. print-graph")
    print("9. load [filepath]")
    print("10. save [filepath]")
    print("11. exit")
    print("-------------------")

    while True:
        argv = input("> ").split()
        if argv[0] == "add-node":
            namespace, argv = parser.parse_known_args(argv[1:])
            if namespace.name in nodes_by_name:
                print(f"a node with the name \"{namespace.name}\" already exists")
            else:
                print(argv)
                new_node = graph.new_node()
                name = argv.pop(0) if (namespace.name is None and len(argv) > 0) else namespace.name
                new_node.name = str(id(new_node)) if name is None else name
                label = argv.pop(0) if (namespace.label is None and len(argv) > 0) else namespace.label
                if label is not None:
                    new_node.label = label
                nodes_by_name[new_node.name] = new_node

        elif argv[0] == "del-node":
            if len(argv) < 2:
                print("must provide the name of the node to remove")
            else:
                node = nodes_by_name[argv[1]]
                del nodes_by_name[argv[1]]
                for edge in node.get_edges():
                    if hasattr(edge, "name"):
                        if edge.name in edges_by_name:
                            del edges_by_name[edge.name]
                graph.remove_node(node)

        elif argv[0] == "add-edge":
            namespace, argv = parser.parse_known_args(argv[1:])
            if len(argv) < 2:
                print("must provide two nodes, a tail and a head")
            elif argv[1] not in nodes_by_name:
                print(f"{argv[1]} is not a node in the graph")
            elif argv[2] not in nodes_by_name:
                print(f"{argv[2]} is not a node in the graph")
            elif namespace.name in edges_by_name:
                print(f"an edge with the name \"{namespace.name}\" already exists")
            else:
                tail = nodes_by_name[argv[1]]
                head = nodes_by_name[argv[2]]
                new_edge = graph.new_edge(tail, head)
                new_edge.name = str(id(new_edge)) if namespace.name is None else namespace.name
                if namespace.label is not None:
                    new_edge.label = namespace.label
                edges_by_name[new_edge.name] = new_edge

        elif argv[0] == "del-edge":
            if len(argv) < 2:
                print("must provide the name of the edge to remove")
            else:
                edge = edges_by_name[argv[1]]
                graph.remove_edge(edge)

        elif argv[0] == "node-dict":
            for name, node in nodes_by_name.items():
                print(f"{name} : {node}")

        elif argv[0] == "edge-dict":
            for name, edge in edges_by_name.items():
                print(f"{name} : {edge}")

        elif argv[0] == "reset":
            graph = Graph()
            nodes_by_name = {}
            edges_by_name = {}

        elif argv[0] == "print":
            print(graph)

        # TODO: this needs to be implemented
        elif argv[0] == "load":
            if len(argv) < 2:
                print("must provide file containing graph")
            else:
                graph = Graph()
                nodes_by_name = {}
                edges_by_name = {}

        elif argv[0] == "save":
            file = argv[1]
            with open(file, "w") as f:
                f.write(str(graph))
                f.close()

        elif argv[0] == "exit":
            break

        else:
            print(f"unknown command \"{argv[0]}\"")


if __name__ == "__main__":
    main()
