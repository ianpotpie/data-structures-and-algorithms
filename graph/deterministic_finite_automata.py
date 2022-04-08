from directed_graph import DirectedGraph


class DFA(DirectedGraph):
    def __init__(self):
        super().__init__()
        self.states = self.nodes
        self.transitions = self.edges
        self.start_state = None
        self.accept_states = set()
        self.alphabet = set()
        self.sink_state = None

    def insert_state(self, state):
        self.states.add(state)

    def insert_transition(self, transition):
        assert transition.symbol in self.alphabet
        assert transition.start in self.states
        assert transition.end in self.states
        for outgoing_transition in transition.start.outgoing_transitions:
            if outgoing_transition.symbol == transition.symbol:
                self.del_transition(outgoing_transition)  # outgoing symbol transitions are unique (injective)
        self.transitions.add(transition)
        transition.start.outgoing_transitions.add(transition)
        transition.start.symbol_map[transition.symbol] = transition.end
        transition.end.incoming_transitions.add(transition)

    def insert_accept_state(self, state):
        assert state in self.states
        self.accept_states.add(state)

    def insert_symbol(self, symbol):
        self.alphabet.add(symbol)

    def del_state(self, state):
        assert state in self.states
        for transition in state.outgoing_transitions:
            self.del_transition(transition)
        for transition in state.incoming_transitions:
            self.del_transition(transition)
        self.states.remove(state)

    def del_transition(self, transition):
        assert transition in self.transitions
        transition.start.outgoing_transitions.remove(transition)
        del transition.start.symbol_map[transition.symbol]
        if transition.end is not transition.start:
            transition.end.incoming_transitions.remove(transition)
        self.transitions.remove(transition)

    def del_accept_state(self, state):
        assert state in self.accept_states
        self.accept_states.remove(state)

    def del_symbol(self, symbol):
        assert symbol in self.alphabet
        self.alphabet.remove(symbol)
        for transition in self.transitions:
            if transition.symbol == symbol:
                self.del_transition(transition)

    def set_start_state(self, state):
        assert state in self.states
        self.start_state = state

    def set_sink_state(self, state):
        assert state in self.states
        self.sink_state = state

    def evaluate_string(self, string):
        iterator = DFA.Iterator(self)
        for symbol in string:
            iterator.consume_symbol(symbol)
        return iterator.is_accepting()

    class Iterator:
        def __init__(self, dfa):
            assert dfa.start_state is not None
            self.curr_state = dfa.start_state
            self.dfa = dfa
            self.steps = 0

        def consume_symbol(self, symbol):
            assert symbol in self.dfa.alphabet
            self.steps += 1
            if symbol in self.curr_state.symbol_map:
                self.curr_state = self.curr_state.symbol_map[symbol]
            else:
                assert self.dfa.sink_state is not None
                self.curr_state = self.dfa.sink_state

        def is_accepting(self):
            return self.curr_state in self.dfa.accept_states

    class State(DirectedGraph.Node):
        def __init__(self, label):
            super().__init__(label)
            self.label = self.value
            self.transitions = self.edges
            self.incoming_transitions = self.incoming_edges
            self.outgoing_transitions = self.outgoing_edges
            self.symbol_map = dict()

    class Transition(DirectedGraph.Edge):
        def __init__(self, symbol, start, end):
            super().__init__(symbol, start, end)
            self.symbol = self.value
