class FSM:
    """
    A class representing a Finite State Machine (can be used for both DFA and NFA)
    """
    def __init__(self, states, alphabet, transitions, start_state, accept_states, is_deterministic=True):
        """
        Initialize the FSM with its components
        
        Args:
            states (set): Set of all states in the FSM
            alphabet (set): Set of all input symbols
            transitions (dict): Dictionary mapping (state, symbol) to a set of next states
            start_state: The initial state
            accept_states (set): Set of accepting states
            is_deterministic (bool): Whether this FSM is deterministic
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.is_deterministic = is_deterministic
        self.current_states = {start_state} if not is_deterministic else start_state
        self.input_sequence = []
        
    def reset(self):
        """Reset the FSM to its initial state"""
        self.current_states = {self.start_state} if not self.is_deterministic else self.start_state
        self.input_sequence = []
    
    def transition(self, symbol):
        """
        Process an input symbol and update the current state(s)
        
        Args:
            symbol: The input symbol to process
            
        Returns:
            bool: True if valid transition, False otherwise
        """
        self.input_sequence.append(symbol)
        
        if self.is_deterministic:
            # DFA transition
            if (self.current_states, symbol) in self.transitions:
                self.current_states = self.transitions[(self.current_states, symbol)]
                return True
            return False
        else:
            # NFA transition
            next_states = set()
            for state in self.current_states:
                if (state, symbol) in self.transitions:
                    next_states.update(self.transitions[(state, symbol)])
                    
            self.current_states = next_states
            return len(next_states) > 0
    
    def process_string(self, input_string):
        """
        Process a complete input string
        
        Args:
            input_string (str): The input string to process
            
        Returns:
            bool: True if the string is accepted, False otherwise
        """
        self.reset()
        
        # Process each symbol in the input string
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            if not self.transition(symbol):
                return False
        
        # Check if we ended in an accept state
        if self.is_deterministic:
            return self.current_states in self.accept_states
        else:
            return any(state in self.accept_states for state in self.current_states)
    
    def get_transition_history(self):
        """
        Get the history of transitions made during the last string processing
        
        Returns:
            list: List of (state, symbol, next_state) tuples
        """
        history = []
        state = self.start_state
        
        for symbol in self.input_sequence:
            if self.is_deterministic:
                next_state = self.transitions.get((state, symbol))
                if next_state:
                    history.append((state, symbol, next_state))
                    state = next_state
            else:
                # For NFA, simplify by just showing one possible path
                next_states = self.transitions.get((state, symbol), set())
                if next_states:
                    next_state = next(iter(next_states))
                    history.append((state, symbol, next_state))
                    state = next_state
        
        return history

# Create DFA for the language (a+b)c*
def create_dfa_a_plus_b_c_star():
    """Create a DFA for the language (a+b)c*"""
    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b', 'c'}
    transitions = {
        ('q0', 'a'): 'q1',
        ('q0', 'b'): 'q1',
        ('q1', 'c'): 'q1',
    }
    start_state = 'q0'
    accept_states = {'q1'}
    
    return FSM(states, alphabet, transitions, start_state, accept_states, is_deterministic=True)

# Create NFA for the language (a|b)*abb
def create_nfa_a_or_b_star_abb():
    """Create an NFA for the language (a|b)*abb"""
    states = {'q0', 'q1', 'q2', 'q3'}
    alphabet = {'a', 'b'}
    transitions = {
        ('q0', 'a'): {'q0', 'q1'},
        ('q0', 'b'): {'q0'},
        ('q1', 'b'): {'q2'},
        ('q2', 'b'): {'q3'},
    }
    start_state = 'q0'
    accept_states = {'q3'}
    
    return FSM(states, alphabet, transitions, start_state, accept_states, is_deterministic=False)

# Example usage:
if __name__ == "__main__":
    # DFA example
    dfa = create_dfa_a_plus_b_c_star()
    test_strings_dfa = ['a', 'b', 'ac', 'bc', 'acc', 'bcc', 'c', 'ab', 'ba']
    
    print("DFA for language (a+b)c*:")
    for s in test_strings_dfa:
        result = dfa.process_string(s)
        print(f"String '{s}': {'Accepted' if result else 'Rejected'}")
    
    # NFA example
    nfa = create_nfa_a_or_b_star_abb()
    test_strings_nfa = ['abb', 'aabb', 'babb', 'aaabb', 'bbabb', 'ababb', 'ab', 'bb', 'bba']
    
    print("\nNFA for language (a|b)*abb:")
    for s in test_strings_nfa:
        result = nfa.process_string(s)
        print(f"String '{s}': {'Accepted' if result else 'Rejected'}")
# """
# FSM Visualizer - Creates graphical representations of finite state machines
# """

# def generate_dot_representation(fsm):
#     """Generate a DOT language representation of the FSM for graphviz"""
#     dot = [
#         'digraph fsm {',
#         '    rankdir=LR;',
#         '    size="8,5";',
#         '    node [shape = doublecircle];'
#     ]
    
#     # Add accepting states as double circles
#     accepting_states = [state.name for state in fsm.states.values() if state.is_accepting]
#     if accepting_states:
#         dot.append('    ' + ' '.join(f'"{state}"' for state in accepting_states) + ';')
    
#     dot.append('    node [shape = circle];')
    
#     # Add invisible initial node with transition to initial state
#     dot.append('    "" [shape=none];')
#     if fsm.initial_state:
#         dot.append(f'    "" -> "{fsm.initial_state.name}";')
    
#     # Add all transitions
#     for state_name, state in fsm.states.items():
#         for symbol, target_states in state.transitions.items():
#             for target in target_states:
#                 dot.append(f'    "{state_name}" -> "{target.name}" [label="{symbol}"];')
    
#     dot.append('}')
#     return '\n'.join(dot)


# def generate_ascii_diagram(fsm):
#     """Generate a simple ASCII representation of the FSM"""
#     result = [f"FSM: {fsm.name}"]
#     result.append("=" * len(result[0]))
#     result.append("")
    
#     # States
#     result.append("States:")
#     for state_name, state in sorted(fsm.states.items()):
#         initial_marker = "→ " if fsm.initial_state and state_name == fsm.initial_state.name else "  "
#         accepting_marker = " (accepting)" if state.is_accepting else ""
#         result.append(f"{initial_marker}{state_name}{accepting_marker}")
    
#     result.append("")
    
#     # Transitions
#     result.append("Transitions:")
#     for state_name, state in sorted(fsm.states.items()):
#         for symbol, target_states in sorted(state.transitions.items()):
#             targets = ", ".join(sorted(target.name for target in target_states))
#             result.append(f"  {state_name} --({symbol})--> {targets}")
    
#     return "\n".join(result)


# def visualize_path(fsm, input_string):
#     """
#     Visualize the path taken through the FSM for a given input string
#     Returns a formatted string representation
#     """
#     is_accepted, path = fsm.process_input(input_string)
    
#     # Create a string representation of the path
#     result = [f"Input: {input_string}"]
#     result.append("=" * len(result[0]))
#     result.append(f"Result: {'ACCEPTED' if is_accepted else 'REJECTED'}")
#     result.append("")
#     result.append("Path:")
    
#     for i, (state, symbol) in enumerate(path):
#         if i == 0:
#             result.append(f"  Start at state: {state}")
#         else:
#             result.append(f"  Read '{symbol}' → Go to state: {state}")
    
#     return "\n".join(result)


# def save_fsm_visualization(fsm, filename):
#     """Save a graphviz visualization of the FSM to a file"""
#     try:
#         import graphviz
#         dot = graphviz.Source(generate_dot_representation(fsm))
#         dot.render(filename, format='png', cleanup=True)
#         return True
#     except ImportError:
#         print("Graphviz not installed. Using text-based visualization instead.")
#         with open(f"{filename}.txt", 'w') as f:
#             f.write(generate_ascii_diagram(fsm))
#         return False


# if __name__ == "__main__":
#     # Simple test
#     from fsm_implementation import create_dfa_for_ab_c_star, create_nfa_for_ab_star_abb
    
#     dfa = create_dfa_for_ab_c_star()
#     nfa = create_nfa_for_ab_star_abb()
    
#     print(generate_ascii_diagram(dfa))
#     print("\n\n")
#     print(generate_ascii_diagram(nfa))
    
#     # Test path visualization
#     print("\n\n")
#     print(visualize_path(dfa, "acc"))
#     print("\n\n")
#     print(visualize_path(nfa, "aabb"))