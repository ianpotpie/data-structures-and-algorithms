from directed_graph import DirectedGraph


class NFA(DirectedGraph):
    def __init__(self):
        super().__init__()
        self.states = self.nodes
        self.transitions = self.edges
        self.start_state = None
        self.accept_states = set()
        self.empty_symbol = ""
        self.alphabet = set()
        self.sink_state = None

    def insert_state(self, state):
        self.states.add(state)

    def insert_transition(self, transition):
        assert (transition.symbol in self.alphabet) or (transition.symbol == self.empty_symbol)
        assert transition.start in self.states
        assert transition.end in self.states
        if transition.symbol == self.empty_symbol:
            if transition.end in transition.start.empty_map:
                for outgoing_transition in transition.start.outgoing_transitions:
                    if (outgoing_transition.symbol == self.empty_symbol) \
                            and (outgoing_transition.end == transition.end):
                        self.del_transition(outgoing_transition)
            transition.start.empty_map.add(transition.end)
        else:
            if transition.symbol in transition.start.symbol_map:
                for outgoing_transition in transition.start.outgoing_transitions:
                    if outgoing_transition.symbol == transition.symbol:
                        # outgoing symbol transitions are unique (injective) if they are not the empty string
                        self.del_transition(outgoing_transition)
            transition.start.symbol_map[transition.symbol] = transition.end
        self.transitions.add(transition)
        transition.start.outgoing_transitions.add(transition)
        transition.end.incoming_transitions.add(transition)

    def insert_accept_state(self, state):
        assert state in self.states
        self.accept_states.add(state)

    def insert_symbol(self, symbol):
        assert symbol != self.empty_symbol
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
        if transition.symbol == self.empty_symbol:
            transition.start.empty_map.remove(transition.end)
        else:
            del transition.start.symbol_map[transition.symbol]
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
                self.transitions.remove(symbol)

    def set_start_state(self, state):
        assert state in self.states
        self.start_state = state

    def set_sink_state(self, state):
        assert state in self.states
        self.sink_state = state

    def evaluate_string(self, string):
        iterator = NFA.Iterator(self)
        for symbol in string:
            iterator.consume_symbol(symbol)
        return iterator.is_accepting()

    class Iterator:
        def __init__(self, nfa):
            assert nfa.start_state is not None
            self.curr_states = {nfa.start_state}
            self.nfa = nfa
            self.steps = 0
            self.consume_empty_symbol()

        def consume_empty_symbol(self):
            assert self.nfa.empty_symbol is not None
            next_states = set()
            frontier = set(self.curr_states)
            while len(frontier) > 0:
                state = frontier.pop()
                next_states.add(state)
                frontier.add(state.empty_map - next_states)
            self.curr_states = next_states

        def consume_symbol(self, symbol):
            assert symbol in self.nfa.alphabet
            self.steps += 1
            next_states = set()
            for state in self.curr_states:
                if symbol in state.symbol_map:
                    next_states.add(state.symbol_map[symbol])
                else:
                    assert self.nfa.sink_state is not None
                    next_states.add(self.nfa.sink_state)
            self.curr_states = next_states
            self.consume_empty_symbol()

        def is_accepting(self):
            for state in self.curr_states:
                if state in self.nfa.accept_states:
                    return True
            return False

    class State(DirectedGraph.Node):
        def __init__(self, label):
            super().__init__(label)
            self.label = self.value
            self.transitions = self.edges
            self.incoming_transitions = self.incoming_edges
            self.outgoing_transitions = self.outgoing_edges
            self.symbol_map = dict()
            self.empty_map = set()

    class Transition(DirectedGraph.Edge):
        def __init__(self, symbol, start, end):
            super().__init__(symbol, start, end)
            self.symbol = self.value
