# Finite State Machine Implementation

This project implements both Deterministic and Non-deterministic Finite State Machines (DFA & NFA) to recognize specific languages. The implementation includes a visualization component to help understand how these machines work This project doesn't fully work but oh well

## Languages Implemented

### DFA
The DFA implements the language: `(a+b)c*`

This language accepts strings that:
- Start with exactly one 'a' or 'b'
- Followed by zero or more 'c's

Examples of acceptable strings:
- `a`
- `b`
- `ac`
- `bc`
- `acc`
- `bcc`
- `accc`
- `bccc`

### NFA
The NFA implements the language: `(a|b)*abb`

This language accepts strings that:
- End with the substring 'abb'
- Can have any number of 'a's and 'b's (including zero) before that substring

Examples of acceptable strings:
- `abb`
- `aabb`
- `babb`
- `aaabb`
- `bbabb`
- `ababb`

## Project Structure

```
├── fsm.py                 # Core FSM implementation
├── fsm_visualizer.py      # Graphviz-based FSM visualization
├── fsm_tests.py           # Unit tests for DFA and NFA
├── fsm_app.py             # Interactive GUI application
├── transition_tables.json # JSON definitions for FSMs
└── web_visualizer/        # Web-based visualization using React
```

## Features

1. **FSM Implementation**
   - Base FSM class supporting both DFA and NFA
   - String processing methods
   - Transition history tracking

2. **Visualizations**
   - Static FSM diagrams
   - Step-by-step processing visualization
   - Animation of string processing
   - Interactive web visualization

3. **Testing**
   - Unit tests for both DFA and NFA
   - Multiple test cases for valid and invalid strings

4. **User Interface**
   - GUI application with Tkinter
   - Web interface with React
   - Custom FSM definition support

## Requirements

### Python Implementation
- Python 3.6+
- Graphviz library for visualization
- PIL/Pillow for image handling in the application
- tkinter for the GUI

Install dependencies with:
```bash
pip install graphviz pillow
```

### Web Implementation
- Node.js environment
- React

## Running the Application

### Python GUI
```bash
python fsm_app.py
```

### Running Tests
```bash
python fsm_tests.py
```

### Web Visualizer
```bash
cd web_visualizer
npm install
npm start
```

## Custom FSM Definition

You can define your own FSM by creating a JSON file with the following structure:

```json
{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["a", "b", "c"],
  "transitions": {
    "q0": {
      "a": "q1",
      "b": "q1"
    },
    "q1": {
      "c": "q1"
    }
  },
  "start_state": "q0",
  "accept_states": ["q1"],
  "is_deterministic": true
}
```

For NFAs, transitions can point to multiple states:

```json
"transitions": {
  "q0": {
    "a": ["q0", "q1"],
    "b": ["q0"]
  }
}
```

## Extension Ideas

1. **Parser for Regular Expressions**
   - Automatically convert regular expressions to NFAs
   - Implement Thompson's construction algorithm

2. **NFA to DFA Conversion**
   - Implement the powerset construction algorithm
   - Visualize the conversion process

3. **Minimizing DFAs**
   - Implement Hopcroft's algorithm for DFA minimization
   - Compare before and after minimization

4. **Support for ε-transitions**
   - Extend the NFA implementation to handle epsilon transitions
   - Show epsilon-closure computation

5. **Multiple Input Methods**
   - Support for reading input from files
   - Batch processing of multiple strings

## Educational Value

This project demonstrates core concepts in computational theory:

1. **Language Recognition**
   - How finite automata recognize formal languages
   - Differences between DFAs and NFAs in expressive power

2. **State Transitions**
   - How machines change state based on input
   - Processing strings character by character

3. **Determinism vs. Non-determinism**
   - How NFAs can have multiple active states
   - How NFAs can transition to multiple states on the same input

So Hanna this implementation is valuable for computer science students studying theoretical foundations, showing practical applications of automata theory concepts.