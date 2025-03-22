import unittest
import nfa_config.txt, dfa_config.txt

class TestDFA(unittest.TestCase):
    def setUp(self):
        self.dfa = create_dfa_a_plus_b_c_star()
    
    def test_acceptable_strings(self):
        # Test all the provided acceptable examples and more
        acceptable_strings = [
            'a',        # Single 'a'
            'b',        # Single 'b'
            'ac',       # 'a' followed by one 'c'
            'bc',       # 'b' followed by one 'c'
            'acc',      # 'a' followed by two 'c's
            'bcc',      # 'b' followed by two 'c's
            'accc',     # 'a' followed by three 'c's
            'bccc',     # 'b' followed by three 'c's
            'acccc',    # 'a' followed by four 'c's
            'bcccc'     # 'b' followed by four 'c's
        ]
        
        for s in acceptable_strings:
            with self.subTest(string=s):
                self.assertTrue(self.dfa.process_string(s), f"String '{s}' should be accepted")
    
    def test_unacceptable_strings(self):
        # Test unacceptable strings
        unacceptable_strings = [
            '',         # Empty string
            'c',        # Only 'c'
            'ab',       # 'a' followed by 'b'
            'ba',       # 'b' followed by 'a'
            'aca',      # 'a', 'c', then 'a'
            'bca',      # 'b', 'c', then 'a'
            'abc',      # 'a', 'b', then 'c'
            'cab',      # 'c', 'a', then 'b'
            'aaa',      # Multiple 'a's
            'bbb'       # Multiple 'b's
        ]
        
        for s in unacceptable_strings:
            with self.subTest(string=s):
                self.assertFalse(self.dfa.process_string(s), f"String '{s}' should be rejected")

class TestNFA(unittest.TestCase):
    def setUp(self):
        self.nfa = create_nfa_a_or_b_star_abb()
    
    def test_acceptable_strings(self):
        # Test all the provided acceptable examples and more
        acceptable_strings = [
            'abb',      # Basic pattern
            'aabb',     # Prefixed with 'a'
            'babb',     # Prefixed with 'b'
            'aaabb',    # Prefixed with 'aa'
            'bbabb',    # Prefixed with 'bb'
            'ababb',    # Prefixed with 'ab'
            'baabb',    # Prefixed with 'ba'
            'abababb',  # More complex prefix
            'bbaabb'    # Another complex prefix
        ]
        
        for s in acceptable_strings:
            with self.subTest(string=s):
                self.assertTrue(self.nfa.process_string(s), f"String '{s}' should be accepted")
    
    def test_unacceptable_strings(self):
        # Test unacceptable strings
        unacceptable_strings = [
            '',         # Empty string
            'a',        # Only 'a'
            'b',        # Only 'b'
            'ab',       # 'a' then 'b'
            'ba',       # 'b' then 'a'
            'bba',      # 'b', 'b', then 'a'
            'aba',      # 'a', 'b', then 'a'
            'abab',     # Alternating 'a' and 'b'
            'abba',     # 'a', 'b', 'b', then 'a'
            'aab'       # 'a', 'a', then 'b'
        ]
        
        for s in unacceptable_strings:
            with self.subTest(string=s):
                self.assertFalse(self.nfa.process_string(s), f"String '{s}' should be rejected")

if __name__ == '__main__':
    unittest.main()
# """
# Unit Tests for Finite State Machine Implementations
# """

# import unittest
# from fsm_implementation import create_dfa_for_ab_c_star, create_nfa_for_ab_star_abb

# class TestDFA(unittest.TestCase):
#     """Tests for the DFA implementation of language (a+b)c*"""
    
#     def setUp(self):
#         """Set up the DFA for testing"""
#         self.dfa = create_dfa_for_ab_c_star()
    
#     def test_dfa_accepts_valid_inputs(self):
#         """Test that the DFA accepts valid inputs"""
#         valid_inputs = [
#             "a",        # Just 'a'
#             "b",        # Just 'b'
#             "ac",       # 'a' followed by one 'c'
#             "bc",       # 'b' followed by one 'c'
#             "acc",      # 'a' followed by two 'c's
#             "bccc",     # 'b' followed by three 'c's
#             "acccccc",  # 'a' followed by six 'c's
#         ]
        
#         for input_str in valid_inputs:
#             with self.subTest(input=input_str):
#                 is_accepted, _ = self.dfa.process_input(input_str)
#                 self.assertTrue(is_accepted, f"DFA should accept '{input_str}'")
    
#     def test_dfa_rejects_invalid_inputs(self):
#         """Test that the DFA rejects invalid inputs"""
#         invalid_inputs = [
#             "",         # Empty string
#             "c",        # Just 'c'
#             "aa",       # Two 'a's
#             "bb",       # Two 'b's
#             "aca",      # 'a' followed by 'c' then 'a'
#             "ab",       # 'a' followed by 'b'
#             "acb",      # 'a' followed by 'c' then 'b'
#         ]
        
#         for input_str in invalid_inputs:
#             with self.subTest(input=input_str):
#                 is_accepted, _ = self.dfa.process_input(input_str)
#                 self.assertFalse(is_accepted, f"DFA should reject '{input_str}'")
    
#     def test_dfa_transition_path(self):
#         """Test that the DFA returns correct transition paths"""
#         # Test for the input "acc"
#         is_accepted, path = self.dfa.process_input("acc")
#         self.assertTrue(is_accepted)
        
#         # Check that the path follows the expected transitions
#         expected_path = [
#             ("start", None),           # Initial state
#             ("read_a_or_b", "a"),      # After reading 'a'
#             ("read_c", "c"),           # After reading 'c'
#             ("read_c", "c"),           # After reading 'c'
#         ]
        
#         self.assertEqual(path, expected_path, "Path should match expected transitions")


# class TestNFA(unittest.TestCase):
#     """Tests for the NFA implementation of language (a|b)*abb"""
    
#     def setUp(self):
#         """Set up the NFA for testing"""
#         self.nfa = create_nfa_for_ab_star_abb()
    
#     def test_nfa_accepts_valid_inputs(self):
#         """Test that the NFA accepts valid inputs"""
#         valid_inputs = [
#             "abb",      # Minimal pattern
#             "aabb",     # With prefix 'a'
#             "babb",     # With prefix 'b'
#             "ababb",    # With prefix 'ab'
#             "bababb",   # With prefix 'bab'
#             "aaabb",    # With prefix 'aa'
#             "abbabb",   # Two occurrences of 'abb'
#         ]
        
#         for input_str in valid_inputs:
#             with self.subTest(input=input_str):
#                 is_accepted, _ = self.nfa.process_input(input_str)
#                 self.assertTrue(is_accepted, f"NFA should accept '{input_str}'")
    
#     def test_nfa_rejects_invalid_inputs(self):
#         """Test that the NFA rejects invalid inputs"""
#         invalid_inputs = [
#             "",         # Empty string
#             "a",        # Just 'a'
#             "ab",       # 'a' followed by 'b' (missing final 'b')
#             "abba",     # Different pattern
#             "ababc",    # Invalid character
#             "bab",      # 'b' followed by 'a' then 'b' (not full pattern)
#             "abbb",     # 'a' followed by three 'b's
#         ]
        
#         for input_str in invalid_inputs:
#             with self.subTest(input=input_str):
#                 is_accepted, _ = self.nfa.process_input(input_str)
#                 self.assertFalse(is_accepted, f"NFA should reject '{input_str}'")
    
#     def test_nfa_path_finding(self):
#         """Test that the NFA can find a valid path for accepted strings"""
#         # Test for the input "abb"
#         is_accepted, path = self.nfa.process_input("abb")
#         self.assertTrue(is_accepted)
        
#         # The path should end at the accepting state
#         self.assertEqual(path[-1][0], "read_abb", 
#                          "Path should end at the accepting state")


# if __name__ == "__main__":
#     unittest.main()
