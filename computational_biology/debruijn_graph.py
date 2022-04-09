import sys
from directed_graph import DiGraph


def build_kmer_spectrum(reads: list[str], k: int) -> dict[str, list[tuple[int, int, int]]]:
    """
    Generates the spectrum of kmers in the reads.

    :param reads: a list of read sequences
    :param k: the size of the kmers
    :return: a dictionary of kmers to their source locations
    """
    kmer_spectrum: dict[str, list[tuple[int, int, int]]] = {}
    for i, read in enumerate(reads):
        n_kmers = len(read) + 1 - k
        for j in range(n_kmers):
            kmer = read[j:j + k]
            if kmer not in kmer_spectrum:
                kmer_spectrum[kmer] = []
            kmer_spectrum[kmer].append((i, j, j + k))

    return kmer_spectrum


def build_debruijn_graph(reads: list[str], k: int) -> DiGraph:
    """
    Builds a directed graph that is the DeBruijn graph of the kmers in the reads.

    :param reads: a list of read sequences
    :param k: the length of the kmers
    :return: a directed graph of kmers
    """
    debruijn_graph = DiGraph()
    for kmer, sources in build_kmer_spectrum(reads, k).items():
        start = kmer[:-1]
        end = kmer[1:]
        if start not in debruijn_graph:
            debruijn_graph.new_node(name=start, label=start)
        if end not in debruijn_graph:
            debruijn_graph.new_node(name=end, label=end)
        debruijn_graph.new_edge(tail_name=start, head_name=end, name=kmer, label=kmer, sources=sources)

    return debruijn_graph


def main():
    # the reads from the read file
    reads = []
    read_file = sys.argv[1]
    with open(read_file) as f:
        for line in f:
            reads.append(line.strip())

    # the size of the kmers
    k = int(sys.argv[2])

    debruijn_graph = build_debruijn_graph(reads, k)

    # the output graph file
    graph_file = sys.argv[3]
    with open(graph_file, mode="w") as f:
        f.write(str(debruijn_graph))


if __name__ == "__main__":
    main()
