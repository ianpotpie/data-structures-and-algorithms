def build_eulerian_path(graph, start_node=None, end_node=None):
    """
    This algorithm finds an eularean path on an undirected graph. The path may not be unique.
    :param graph: an undirected graph
    :param start_node: a starting node for the path
    :param end_node: an ending node for the path
    :return: a list of all edges in the graph such that any consecutive edges share at least one node
    """

    # if there are odd-degree nodes, then they are the ends of the eulerian path
    odd_degree_nodes = []
    for node in graph.nodes:
        if len(node.edges) % 2 == 1:
            odd_degree_nodes.append(node)

    # there are only two possible ways a eulerian path can exist
    assert (len(odd_degree_nodes) == 0) or (len(odd_degree_nodes) == 2)

    # check that the start and end nodes have valid values, and set the start node if it is none
    # (given a start node, the end node is unique, so we only need to keep one of the two)
    if (len(odd_degree_nodes) > 0) and (start_node is None) and (end_node is None):
        start_node, end_node = odd_degree_nodes
    elif (len(odd_degree_nodes) > 0) and (start_node is None) and (end_node is not None):
        assert end_node in odd_degree_nodes
        start_node = odd_degree_nodes[0] if odd_degree_nodes[1] is end_node else odd_degree_nodes[1]
    elif (len(odd_degree_nodes) > 0) and (start_node is not None) and (end_node is None):
        assert start_node in odd_degree_nodes
    elif (len(odd_degree_nodes) > 0) and (start_node is not None) and (end_node is not None):
        assert start_node is not end_node
        assert start_node in odd_degree_nodes
        assert end_node in odd_degree_nodes
    elif (len(odd_degree_nodes) == 0) and (start_node is None) and (end_node is None):
        start_node = next(iter(graph.nodes))
    elif (len(odd_degree_nodes) == 0) and (start_node is None) and (end_node is not None):
        start_node = end_node
    elif (len(odd_degree_nodes) == 0) and (start_node is not None) and (end_node is None):
        pass
    elif (len(odd_degree_nodes) == 0) and (start_node is not None) and (end_node is not None):
        assert start_node is end_node

    path = []
    remaining_edges: set = graph.edges.copy()

    curr_node = start_node
    path_index = 0
    while len(remaining_edges) > 0:
        assert path_index >= 0
        next_edges = remaining_edges & curr_node.edges
        if len(next_edges) == 0:  # we backtrack if we encounter a dead-end
            path_index -= 1
            edge = path[path_index]
            curr_node = edge.node1 if edge.node1 is not curr_node else edge.node2
        else:
            edge = next_edges.pop()
            remaining_edges.remove(edge)
            path.insert(path_index, edge)
            path_index += 1
            curr_node = edge.node1 if edge.node1 is not curr_node else edge.node2

    return path


def build_directed_eulerian_path(graph, start_node=None, end_node=None):
    """
    This algorithm finds an eularean path on a directed graph. The path may not be unique.
    :param graph: an undirected graph
    :param start_node: a starting node for the path
    :param end_node: an ending node for the path
    :return: a list of all edges in the graph such that any consecutive edges share at least one node
    """

    # check the validity of the start and end nodes, and sets them if they have null values
    # given a start node, the end node is unique, so we only need to keep one of the two
    is_circuit = True
    for node in graph.nodes:
        n_in = len(node.in_edges)
        n_out = len(node.out_edges)
        assert abs(n_in - n_out) <= 1
        if n_in - n_out == -1:
            is_circuit = False
            if start_node is not None:
                assert node is start_node
            else:
                start_node = node
        if n_in - n_out == 1:
            is_circuit = False
            if end_node is not None:
                assert node is end_node
            else:
                end_node = node
    if is_circuit:
        assert start_node is end_node

    path = []
    remaining_edges: set = graph.edges.copy()

    curr_node = start_node
    path_index = 0
    while len(remaining_edges) > 0:
        assert path_index >= 0
        next_edges = remaining_edges & curr_node.out_edges
        if len(next_edges) == 0:
            path_index -= 1
            edge = path[path_index]
            curr_node = edge.start
        else:
            edge = next_edges.pop()
            remaining_edges.remove(edge)
            path.insert(path_index, edge)
            path_index += 1
            curr_node = edge.end

    return path


def main():
    pass


if __name__ == "__main__":
    main()
