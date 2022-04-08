from directed_graph import DirectedGraph
from graph import Graph

def depth_first_search(graph, root, end_condition):

def depth_first_find_paths(graph, start, end):

    # each path should start at "start" and end at "end"
    paths: list[list[DirectedGraph.Edge]] = []

    stack: list[tuple[DirectedGraph.Node, list[DirectedGraph.Edge], set[DirectedGraph.Edge]]] = [(start, [], set())]

    while stack
