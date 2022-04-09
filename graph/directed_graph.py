import argparse
from typing import TypeVar
import graphviz
import pydot

DiGraphType = TypeVar("DiGraphType", bound="DiGraph")  # TODO: remove in future update
DiGraphType.Node = TypeVar("Node", bound="DiGraph.Node")  # TODO: remove in future update
DiGraphType.Edge = TypeVar("Edge", bound="DiGraph.Edge")  # TODO: remove in future update


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
            s += f"\t{node};\n"
        for edge in self.edges:
            s += f"\t{edge};\n"
        s += "}"
        return s

    def get_nodes(self) -> list[DiGraphType.Node]:
        """
        Creates a list of all nodes in the digraph.

        :return: a set of digraph nodes
        """
        return list(self.nodes)

    def get_edges(self) -> list[DiGraphType.Edge]:
        """
        Creates a list of all edges in the digraph.

        :return: a set of digraph edges
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

        :param tail: the starting/tail node
        :param head: the ending/head node
        :param kwargs: keyword attributes of the new edge
        :return: the new edge
        """
        assert tail in self.nodes
        assert head in self.nodes
        new_edge = DiGraph.Edge(tail, head, **kwargs)
        tail.edges.add(new_edge)
        head.edges.add(new_edge)
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
            s = f"{str(id(self))}"
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

        def get_edges(self) -> list[DiGraphType.Edge]:
            """
            Creates a shallow copy of the set of edges.

            :return: the edges connected to the node
            """
            return list(self.incoming_edges | self.outgoing_edges)

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
            s = f"{str(id(self.tail))} -> {str(id(self.head))}"
            if hasattr(self, "label"):
                s += f" [label={self.label}]"
            return s


def visualize_digraph(graph: DiGraphType) -> None:
    """
    Render and view the current digraph with graphviz.

    :return: None
    """
    vis_digraph = graphviz.Digraph()
    for node in graph.nodes:
        label = node.label if hasattr(node, "label") else None
        vis_digraph.node(name=str(id(node)), label=label)
    for edge in graph.edges:
        label = edge.label if hasattr(edge, "label") else None
        vis_digraph.edge(tail_name=str(id(edge.tail)), head_name=str(id(edge.head)), label=label)
    vis_digraph.view()


def load_digraph_from_file(file: str) -> DiGraphType:
    """
    Builds a new digraph from the contents of a file (dot format).

    :param file: the path to the file
    :return: a digraph
    """
    new_digraph = DiGraph()
    graph = pydot.graph_from_dot_file(file)[0]

    node_dict = {}
    for node in graph.get_nodes():
        node_dict[node.get_name()] = new_digraph.new_node(name=node.get_name(), **node.get_attributes())

    for edge in graph.get_edges():
        tail_name = edge.get_source()
        head_name = edge.get_destination()
        new_digraph.new_edge(node_dict[tail_name], node_dict[head_name], **edge.get_attributes())

    return new_digraph


def main():
    digraph = DiGraph()
    nodes_by_name = {}
    edges_by_name = {}

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-l", "--label")
    parser.add_argument("-n", "--name")

    print("~DiGraph Builder REPL~")
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
    print("9. view")
    print("10. load [filepath]")
    print("11. save [filepath]")
    print("12. exit")
    print("-------------------")

    while True:
        argv = input("> ").split()
        if argv[0] == "add-node":
            namespace, argv = parser.parse_known_args(argv[1:])
            if namespace.name in nodes_by_name:
                print(f"a node with the name \"{namespace.name}\" already exists")
            else:
                print(argv)
                new_node = digraph.new_node()
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
                digraph.remove_node(node)

        elif argv[0] == "add-edge":
            namespace, argv = parser.parse_known_args(argv[1:])
            if len(argv) < 2:
                print("must provide two nodes, a tail and a head")
            elif argv[1] not in nodes_by_name:
                print(f"{argv[1]} is not a node in the digraph")
            elif argv[2] not in nodes_by_name:
                print(f"{argv[2]} is not a node in the digraph")
            elif namespace.name in edges_by_name:
                print(f"an edge with the name \"{namespace.name}\" already exists")
            else:
                tail = nodes_by_name[argv[1]]
                head = nodes_by_name[argv[2]]
                new_edge = digraph.new_edge(tail, head)
                new_edge.name = str(id(new_edge)) if namespace.name is None else namespace.name
                if namespace.label is not None:
                    new_edge.label = namespace.label
                edges_by_name[new_edge.name] = new_edge

        elif argv[0] == "del-edge":
            if len(argv) < 2:
                print("must provide the name of the edge to remove")
            else:
                edge = edges_by_name[argv[1]]
                digraph.remove_edge(edge)

        elif argv[0] == "node-dict":
            for name, node in nodes_by_name.items():
                print(f"{name} : {node}")

        elif argv[0] == "edge-dict":
            for name, edge in edges_by_name.items():
                print(f"{name} : {edge}")

        elif argv[0] == "reset":
            digraph = DiGraph()
            nodes_by_name = {}
            edges_by_name = {}

        elif argv[0] == "print":
            print(digraph)

        elif argv[0] == "view":
            visualize_digraph(digraph)

        elif argv[0] == "load":
            if len(argv) < 2:
                print("must provide file containing digraph")
            else:
                digraph = load_digraph_from_file(argv[1])
                nodes_by_name = {str(id(node)): node for node in digraph.get_nodes()}
                edges_by_name = {str(id(edge)): edge for edge in digraph.get_edges()}

        elif argv[0] == "save":
            file = argv[1]
            with open(file, "w") as f:
                f.write(str(digraph))
                f.close()

        elif argv[0] == "exit":
            break

        else:
            print(f"unknown command \"{argv[0]}\"")


if __name__ == "__main__":
    main()
