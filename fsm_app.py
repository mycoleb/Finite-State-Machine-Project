import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from PIL import Image, ImageTk
import import nfa_config.txt, dfa_config.txt
import visualize_fsm, visualize_string_processing, animate_string_processing

class FSMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Finite State Machine Visualizer")
        self.geometry("800x600")
        self.configure(padx=10, pady=10)
        
        # Create the DFA and NFA
        self.dfa = create_dfa_a_plus_b_c_star()
        self.nfa = create_nfa_a_or_b_star_abb()
        self.current_fsm = self.dfa
        
        # Create tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        
        # Create tab for DFA
        self.dfa_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dfa_tab, text="DFA (a+b)c*")
        
        # Create tab for NFA
        self.nfa_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.nfa_tab, text="NFA (a|b)*abb")
        
        # Create tab for custom FSM
        self.custom_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.custom_tab, text="Custom FSM")
        
        # Setup DFA tab
        self.setup_fsm_tab(self.dfa_tab, self.dfa, "(a+b)c*")
        
        # Setup NFA tab
        self.setup_fsm_tab(self.nfa_tab, self.nfa, "(a|b)*abb")
        
        # Setup custom FSM tab
        self.setup_custom_fsm_tab()
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def setup_fsm_tab(self, tab, fsm, language):
        # Create visualization
        viz_file = f"fsm_{id(fsm)}"
        visualize_fsm(fsm, viz_file)
        
        # Left frame for visualization
        left_frame = ttk.Frame(tab)
        left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        # Label for language
        language_label = ttk.Label(left_frame, text=f"Language: {language}")
        language_label.pack(pady=5)
        
        # Canvas for FSM visualization
        canvas = tk.Canvas(left_frame)
        canvas.pack(fill="both", expand=True)
        
        # Load and display the image
        image_path = f"{viz_file}.png"
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((400, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.image = photo  # Keep a reference to prevent garbage collection
        
        # Right frame for input and testing
        right_frame = ttk.Frame(tab)
        right_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=5, pady=5)
        
        # Label and entry for input string
        input_label = ttk.Label(right_frame, text="Enter a string to test:")
        input_label.pack(pady=5)
        
        input_entry = ttk.Entry(right_frame)
        input_entry.pack(fill="x", pady=5)
        
        # Button to test the string
        test_button = ttk.Button(
            right_frame, 
            text="Test String", 
            command=lambda: self.test_string(fsm, input_entry.get(), result_label)
        )
        test_button.pack(pady=5)
        
        # Label for the result
        result_label = ttk.Label(right_frame, text="")
        result_label.pack(pady=5)
        
        # Button to visualize the processing
        visualize_button = ttk.Button(
            right_frame,
            text="Visualize Processing",
            command=lambda: self.visualize_processing(fsm, input_entry.get())
        )
        visualize_button.pack(pady=5)
        
        # Button to animate the processing
        animate_button = ttk.Button(
            right_frame,
            text="Animate Processing",
            command=lambda: self.animate_processing(fsm, input_entry.get())
        )
        animate_button.pack(pady=5)
        
        # List of example strings
        example_frame = ttk.LabelFrame(right_frame, text="Example Strings")
        example_frame.pack(fill="x", pady=10)
        
        # Determine example strings based on FSM type
        if fsm.is_deterministic:
            acceptable = ["a", "b", "ac", "bc", "acc", "bcc"]
            unacceptable = ["", "c", "ab", "ba", "abc"]
        else:
            acceptable = ["abb", "aabb", "babb", "aaabb", "bbabb"]
            unacceptable = ["", "a", "b", "ab", "ba", "abba"]
        
        # Add acceptable examples
        ttk.Label(example_frame, text="Acceptable:").pack(anchor="w")
        for example in acceptable:
            example_button = ttk.Button(
                example_frame, 
                text=example,
                command=lambda ex=example: self.fill_input(input_entry, ex)
            )
            example_button.pack(side=tk.LEFT, padx=2)
        
        # Add unacceptable examples
        ttk.Label(example_frame, text="Unacceptable:").pack(anchor="w")
        for example in unacceptable:
            example_button = ttk.Button(
                example_frame, 
                text=example if example else "(empty)",
                command=lambda ex=example: self.fill_input(input_entry, ex)
            )
            example_button.pack(side=tk.LEFT, padx=2)
    
    def setup_custom_fsm_tab(self):
        # Frame for loading/creating custom FSM
        control_frame = ttk.Frame(self.custom_tab)
        control_frame.pack(fill="x", pady=5)
        
        # Button to load FSM from file
        load_button = ttk.Button(
            control_frame,
            text="Load FSM from JSON",
            command=self.load_fsm_from_file
        )
        load_button.pack(side=tk.LEFT, padx=5)
        
        # Button to save current FSM to file
        save_button = ttk.Button(
            control_frame,
            text="Save Current FSM to JSON",
            command=self.save_fsm_to_file
        )
        save_button.pack(side=tk.LEFT, padx=5)
        
        # Text widget for manual definition
        definition_frame = ttk.LabelFrame(self.custom_tab, text="FSM Definition (JSON)")
        definition_frame.pack(fill="both", expand=True, pady=5)
        
        self.definition_text = tk.Text(definition_frame)
        self.definition_text.pack(fill="both", expand=True)
        
        # Add a sample FSM definition
        sample_definition = {
            "states": ["q0", "q1", "q2"],
            "alphabet": ["a", "b", "c"],
            "transitions": {
                "q0": {"a": "q1", "b": "q1"},
                "q1": {"c": "q1"}
            },
            "start_state": "q0",
            "accept_states": ["q1"],
            "is_deterministic": True
        }
        self.definition_text.insert("1.0", json.dumps(sample_definition, indent=2))
        
        # Button to create FSM from definition
        create_button = ttk.Button(
            self.custom_tab,
            text="Create FSM from Definition",
            command=self.create_fsm_from_definition
        )
        create_button.pack(pady=5)
        
        # Frame for testing the custom FSM
        test_frame = ttk.Frame(self.custom_tab)
        test_frame.pack(fill="x", pady=5)
        
        self.custom_input_label = ttk.Label(test_frame, text="Enter a string to test:")
        self.custom_input_label.pack(side=tk.LEFT)
        
        self.custom_input_entry = ttk.Entry(test_frame)
        self.custom_input_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        self.custom_test_button = ttk.Button(
            test_frame,
            text="Test String",
            command=self.test_custom_string
        )
        self.custom_test_button.pack(side=tk.LEFT, padx=5)
        
        self.custom_result_label = ttk.Label(self.custom_tab, text="")
        self.custom_result_label.pack(pady=5)
        
        # Placeholder for custom FSM
        self.custom_fsm = None
    
    def on_tab_change(self, event):
        """Handle tab change events to update the current FSM"""
        tab_id = self.notebook.select()
        tab_name = self.notebook.tab(tab_id, "text")
        
        if tab_name == "DFA (a+b)c*":
            self.current_fsm = self.dfa
        elif tab_name == "NFA (a|b)*abb":
            self.current_fsm = self.nfa
        else:
            self.current_fsm = self.custom_fsm
    
    def test_string(self, fsm, input_string, result_label):
        """Test if a string is accepted by the FSM and display the result"""
        if fsm is None:
            messagebox.showerror("Error", "No FSM defined!")
            return
        
        result = fsm.process_string(input_string)
        if result:
            result_label.config(text=f"String '{input_string}' is ACCEPTED", foreground="green")
        else:
            result_label.config(text=f"String '{input_string}' is REJECTED", foreground="red")
    
    def test_custom_string(self):
        """Test a string against the custom FSM"""
        if self.custom_fsm is None:
            messagebox.showerror("Error", "Please create or load a custom FSM first!")
            return
        
        input_string = self.custom_input_entry.get()
        self.test_string(self.custom_fsm, input_string, self.custom_result_label)
    
    def fill_input(self, entry, example):
        """Fill the input entry with an example string"""
        entry.delete(0, tk.END)
        entry.insert(0, example)
    
    def visualize_processing(self, fsm, input_string):
        """Visualize how the FSM processes a string"""
        if fsm is None:
            messagebox.showerror("Error", "No FSM defined!")
            return
        
        if not input_string:
            messagebox.showerror("Error", "Please enter a string to visualize!")
            return
        
        # Create visualization
        viz_file = f"processing_{id(fsm)}_{input_string}"
        visualize_string_processing(fsm, input_string, viz_file)
        
        # Open the visualization in a new window
        self.open_image_window(f"{viz_file}.png", f"Processing '{input_string}'")
    
    def animate_processing(self, fsm, input_string):
        """Create an animation showing how the FSM processes a string"""
        if fsm is None:
            messagebox.showerror("Error", "No FSM defined!")
            return
        
        if not input_string:
            messagebox.showerror("Error", "Please enter a string to animate!")
            return
        
        # Create animation frames
        frames_dir = f"animation_{id(fsm)}_{input_string}"
        frames = animate_string_processing(fsm, input_string, frames_dir)
        
        # Open animation window
        self.open_animation_window(frames, f"Animating '{input_string}'")
    
    def open_image_window(self, image_path, title):
        """Open a new window to display an image"""
        if not os.path.exists(image_path):
            messagebox.showerror("Error", f"Image file not found: {image_path}")
            return
        
        # Create new window
        window = tk.Toplevel(self)
        window.title(title)
        
        # Load the image
        image = Image.open(image_path)
        
        # Resize if too big
        screen_width = window.winfo_screenwidth() * 0.8
        screen_height = window.winfo_screenheight() * 0.8
        
        img_width, img_height = image.size
        if img_width > screen_width or img_height > screen_height:
            ratio = min(screen_width / img_width, screen_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Display the image
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(window, image=photo)
        label.image = photo  # Keep a reference
        label.pack(padx=10, pady=10)
        
        # Add a close button
        close_button = ttk.Button(window, text="Close", command=window.destroy)
        close_button.pack(pady=10)
    
    def open_animation_window(self, frame_paths, title):
        """Open a window to display an animation"""
        if not frame_paths:
            messagebox.showerror("Error", "No animation frames found")
            return
        
        # Create new window
        window = tk.Toplevel(self)
        window.title(title)
        
        # Create controls frame
        controls = ttk.Frame(window)
        controls.pack(side=tk.BOTTOM, fill="x", padx=10, pady=10)
        
        # Image display label
        image_label = ttk.Label(window)
        image_label.pack(padx=10, pady=10)
        
        # Load all frames
        frames = []
        for path in frame_paths:
            if os.path.exists(path):
                image = Image.open(path)
                
                # Resize if needed
                screen_width = window.winfo_screenwidth() * 0.8
                screen_height = window.winfo_screenheight() * 0.8
                
                img_width, img_height = image.size
                if img_width > screen_width or img_height > screen_height:
                    ratio = min(screen_width / img_width, screen_height / img_height)
                    new_width = int(img_width * ratio)
                    new_height = int(img_height * ratio)
                    image = image.resize((new_width, new_height), Image.LANCZOS)
                
                photo = ImageTk.PhotoImage(image)
                frames.append(photo)
        
        # Variables for animation control
        current_frame = 0
        animation_running = False
        delay = 1000  # ms
        
        # Function to update the displayed frame
        def update_frame():
            nonlocal current_frame
            image_label.config(image=frames[current_frame])
            image_label.image = frames[current_frame]  # Keep a reference
            frame_label.config(text=f"Frame {current_frame + 1} of {len(frames)}")
        
        # Animation control functions
        def play_animation():
            nonlocal animation_running
            animation_running = True
            next_frame()
        
        def stop_animation():
            nonlocal animation_running
            animation_running = False
        
        def next_frame():
            nonlocal current_frame
            if animation_running:
                current_frame = (current_frame + 1) % len(frames)
                update_frame()
                window.after(delay, next_frame)
        
        def prev_frame():
            nonlocal current_frame
            current_frame = (current_frame - 1) % len(frames)
            update_frame()
        
        def next_frame_manual():
            nonlocal current_frame, animation_running
            animation_running = False
            current_frame = (current_frame + 1) % len(frames)
            update_frame()
        
        # Add control buttons
        play_button = ttk.Button(controls, text="Play", command=play_animation)
        play_button.pack(side=tk.LEFT, padx=5)
        
        stop_button = ttk.Button(controls, text="Stop", command=stop_animation)
        stop_button.pack(side=tk.LEFT, padx=5)
        
        prev_button = ttk.Button(controls, text="Previous", command=prev_frame)
        prev_button.pack(side=tk.LEFT, padx=5)
        
        next_button = ttk.Button(controls, text="Next", command=next_frame_manual)
        next_button.pack(side=tk.LEFT, padx=5)
        
        # Frame counter label
        frame_label = ttk.Label(controls, text=f"Frame 1 of {len(frames)}")
        frame_label.pack(side=tk.RIGHT, padx=5)
        
        # Speed control
        def set_speed(val):
            nonlocal delay
            delay = int(1000 / float(val))
        
        speed_frame = ttk.Frame(controls)
        speed_frame.pack(side=tk.LEFT, padx=20)
        
        speed_label = ttk.Label(speed_frame, text="Speed:")
        speed_label.pack(side=tk.LEFT, padx=5)
        
        speed_scale = ttk.Scale(
            speed_frame, 
            from_=0.5, to=5.0, 
            orient=tk.HORIZONTAL, 
            command=set_speed,
            length=100
        )
        speed_scale.set(1.0)
        speed_scale.pack(side=tk.LEFT)
        
        # Close button
        close_button = ttk.Button(controls, text="Close", command=window.destroy)
        close_button.pack(side=tk.BOTTOM, pady=10)
        
        # Display first frame
        update_frame()
    
    def create_fsm_from_definition(self):
        """Create a custom FSM from the JSON definition"""
        try:
            # Get the JSON definition
            json_text = self.definition_text.get("1.0", tk.END)
            fsm_def = json.loads(json_text)
            
            # Convert to proper format for FSM class
            states = set(fsm_def["states"])
            alphabet = set(fsm_def["alphabet"])
            
            # Process transitions
            transitions = {}
            for src_state, state_trans in fsm_def["transitions"].items():
                for symbol, dest_state in state_trans.items():
                    if fsm_def.get("is_deterministic", True):
                        transitions[(src_state, symbol)] = dest_state
                    else:
                        if isinstance(dest_state, list):
                            transitions[(src_state, symbol)] = set(dest_state)
                        else:
                            transitions[(src_state, symbol)] = {dest_state}
            
            start_state = fsm_def["start_state"]
            accept_states = set(fsm_def["accept_states"])
            is_deterministic = fsm_def.get("is_deterministic", True)
            
            # Create the FSM
            self.custom_fsm = FSM(
                states, alphabet, transitions, start_state, accept_states, is_deterministic
            )
            
            # Visualize the FSM
            viz_file = f"custom_fsm_{id(self.custom_fsm)}"
            visualize_fsm(self.custom_fsm, viz_file)
            
            # Open the visualization
            self.open_image_window(f"{viz_file}.png", "Custom FSM")
            
            messagebox.showinfo("Success", "Custom FSM created successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create FSM: {str(e)}")
    
    def load_fsm_from_file(self):
        """Load FSM definition from a JSON file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r') as file:
                fsm_def = json.load(file)
            
            # Update the text widget with the loaded definition
            self.definition_text.delete("1.0", tk.END)
            self.definition_text.insert("1.0", json.dumps(fsm_def, indent=2))
            
            messagebox.showinfo("Success", f"FSM definition loaded from {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load FSM definition: {str(e)}")
    
    def save_fsm_to_file(self):
        """Save current FSM definition to a JSON file"""
        if self.current_fsm is None:
            messagebox.showerror("Error", "No FSM selected!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Convert FSM to JSON-serializable format
            fsm_def = {
                "states": list(self.current_fsm.states),
                "alphabet": list(self.current_fsm.alphabet),
                "transitions": {},
                "start_state": self.current_fsm.start_state,
                "accept_states": list(self.current_fsm.accept_states),
                "is_deterministic": self.current_fsm.is_deterministic
            }
            
            # Process transitions
            for (src_state, symbol), dest_state in self.current_fsm.transitions.items():
                if src_state not in fsm_def["transitions"]:
                    fsm_def["transitions"][src_state] = {}
                
                if self.current_fsm.is_deterministic:
                    fsm_def["transitions"][src_state][symbol] = dest_state
                else:
                    fsm_def["transitions"][src_state][symbol] = list(dest_state)
            
            # Save to file
            with open(file_path, 'w') as file:
                json.dump(fsm_def, file, indent=2)
            
            messagebox.showinfo("Success", f"FSM definition saved to {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save FSM definition: {str(e)}")

# Run the application
if __name__ == "__main__":
    app = FSMApp()
    app.mainloop()
