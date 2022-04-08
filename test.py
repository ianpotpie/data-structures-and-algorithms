import graphviz

graph = graphviz.Graph()

graph.node("A")
graph.node("B")
graph.edge("A", "B")
graph.edge("A", "B")
graph.edge("A", "B")
graph.edge("A", "B")
graph.edge("A", "B")
graph.view()