import sys
from directed_graph import DiGraph
from debruijn_graph import build_debruijn_graph


def merge_subsequences(start_subsequences: set[tuple[int, int, int]],
                       end_subsequences: set[tuple[int, int, int]]) -> set[tuple[int, int, int]]:
    """
    Takes two sets of tuples, where the first element of each tuple represents an origin sequence and the next
    two elements represent the start and end points of a subsequence. The function generates a new set of tuples
    with any overlapping subsequences combined.

    :param start_subsequences: the initial subsequences
    :param end_subsequences: the terminal subsequences
    :return: a new set of subsequence tuples
    """
    merged_sources: set[tuple[int, int, int]] = set()
    unmerged_sources: set[tuple[int, int, int]] = start_subsequences | end_subsequences

    # check for source intervals that can be combined (they overlap)
    for p1 in start_subsequences:
        for p2 in end_subsequences:
            read1, start1, end1 = p1
            read2, start2, end2 = p2
            if read1 == read2 and start1 <= start2 <= end1 <= end2:
                merged_sources.add((read1, start1, end2))
                unmerged_sources.remove(p1)
                unmerged_sources.remove(p2)

    return merged_sources | unmerged_sources


def reduce_singletons(graph: DiGraph) -> bool:
    """
    Reduces a singleton in a DeBruijn graph.

    :param graph: a directed graph (DeBruijn Graph)
    :return: a boolean indicating if a reduction occurred
    """
    was_reduced = False
    for name in graph.get_names():
        incoming_edges = graph.get_incoming_edges(name)
        outgoing_edges = graph.get_outgoing_edges(name)
        if len(incoming_edges) == 1 and len(outgoing_edges) == 1 and len(incoming_edges - outgoing_edges) > 0:
            graph.remove_name(name)
            was_reduced = True

            incoming_edge = incoming_edges.pop()
            outgoing_edge = outgoing_edges.pop()
            prefix = incoming_edge.name[:-len(name)]
            suffix = outgoing_edge.name[len(name):]
            new_name = prefix + name + suffix

            merged_sources = merge_subsequences(incoming_edge.sources, outgoing_edge.sources)
            graph.new_edge(incoming_edge.tail_name, outgoing_edge.head_name,
                           name=new_name, label=new_name, sources=merged_sources)
    return was_reduced


def reduce_forks(graph: DiGraph) -> bool:
    """
    Reduces the forks in a DeBruijn Graph.

    :param graph: a directed graph (DeBruijn Graph)
    :return: a boolean indicating if a reduction occurred
    """
    was_reduced = False
    for name in graph.get_names():
        incoming_edges = graph.get_incoming_edges(name)
        outgoing_edges = graph.get_outgoing_edges(name)
        if len(outgoing_edges) > 1 and len(incoming_edges) == 1:
            incoming_edge = incoming_edges.pop()

            good_edges = set()
            max_merges = 0
            for outgoing_edge in outgoing_edges:
                merged_sources = merge_subsequences(incoming_edge.sources, outgoing_edge.sources)
                n_merges = len(incoming_edge.sources) + len(outgoing_edge.sources) - len(merged_sources)
                if n_merges > max_merges:
                    good_edges.clear()
                    max_merges = n_merges
                if n_merges == max_merges:
                    good_edges.add(outgoing_edge)

            for edge in outgoing_edges:
                if edge not in good_edges:
                    graph.remove_edge(edge)
                    was_reduced = True

        if len(outgoing_edges) == 1 and len(incoming_edges) > 1:
            outgoing_edge = outgoing_edges.pop()

            good_edges = set()
            max_merges = 0
            for incoming_edge in incoming_edges:
                merged_sources = merge_subsequences(incoming_edge.sources, outgoing_edge.sources)
                n_merges = len(incoming_edge.sources) + len(outgoing_edge.sources) - len(merged_sources)
                if n_merges > max_merges:
                    good_edges.clear()
                    max_merges = n_merges
                if n_merges == max_merges:
                    good_edges.add(outgoing_edge)

            for edge in outgoing_edges:
                if edge not in good_edges:
                    graph.remove_edge(edge)
                    was_reduced = True

    return was_reduced


def reduce_crosses(graph: DiGraph):
    """
    Reduces the crosses in the DeBruijn Graph.

    :param graph: a directed graph (DeBruijn graph)
    :return: a graph
    """
    return False


def simplify_debruijn(graph):
    """
    Simplifies the DeBruijn graph

    :param graph:
    :return: None
    """

    is_reducing = True
    while is_reducing:
        is_reducing = False
        is_reducing = is_reducing | reduce_singletons(graph)
        is_reducing = is_reducing | reduce_forks(graph)
        # is_reducing = is_reducing | reduce_crosses(graph)


def main():
    # reads from the read file
    reads = []
    read_file = sys.argv[1]
    with open(read_file) as f:
        for line in f:
            reads.append(line.strip())

    # size of the kmers
    k = int(sys.argv[2])

    debruijn_graph = build_debruijn_graph(reads, k)

    # output graph file
    graph_file = sys.argv[3]
    with open(graph_file, mode="w") as f:
        f.write(str(debruijn_graph))


if __name__ == "__main__":
    main()
