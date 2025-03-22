"""
Finite State Machine Main Program

My program provides a user interface to test both DFA and NFA implementations,
visualize state machines, run tests, and work with configuration files.
"""

import os
import sys
import unittest
import nfa_config.txt, dfa_config.txt
from fsm_visualizer import (
    generate_ascii_diagram, visualize_path, save_fsm_visualization
)
from fsm_tests import TestDFA, TestNFA


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_header(text):
    """Display a formatted header"""
    print("\n" + "=" * 60)
    print(f" {text} ".center(60))
    print("=" * 60 + "\n")


def get_user_choice(prompt, options):
    """Get a user choice from a list of options"""
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = int(input("\nEnter your choice: "))
            if 1 <= choice <= len(options):
                return choice
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")


def test_fsm(fsm):
    """Test a finite state machine interactively"""
    clear_screen()
    display_header(f"Testing {fsm.name}")
    
    print(generate_ascii_diagram(fsm))
    print("\nEnter strings to test against the FSM (or 'q' to quit)")
    
    while True:
        input_str = input("\nInput string: ")
        if input_str.lower() == 'q':
            break
        
        print(visualize_path(fsm, input_str))


def run_all_tests():
    """Run all unit tests"""
    clear_screen()
    display_header("Running Unit Tests")
    
    # Create test suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDFA))
    suite.addTest
