import tkinter as tk
import tkinter.font as tkfont
import random
import os
from playsound import playsound # <--- NEW IMPORT

# --- 1. Data Preparation (Keep this section the same) ---
def load_jokes(filename="randomJokes.txt"):
    """Reads jokes from the file and returns a list of (setup, punchline) tuples."""
    jokes_list = []
    # (File creation and reading logic remains the same)
    if not os.path.exists(filename):
        print(f"Creating a sample {filename} file...")
        with open(filename, 'w') as f:
            f.write("Why don't scientists trust atoms?Because they make up everything.\n")
            f.write("What musical instrument is found in the bathroom?A tuba toothpaste.\n")
            f.write("What do you call a fake noodle?An impasta.\n")
            f.write("Why did the bicycle fall over?Because it was two tired.\n")
            f.write("What do you call a factory that makes good products?A satisfactory.\n")
            f.write("Where do you find a replacement dinosaur?In the lost and sound.\n")
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                cleaned_line = line.strip()
                if '?' in cleaned_line:
                    parts = cleaned_line.split('?', 1)
                    setup = parts[0].strip() + '?'
                    punchline = parts[1].strip()
                    if setup and punchline:
                        jokes_list.append((setup, punchline))
        if not jokes_list:
            return [("No jokes found in file.", "Try checking the randomJokes.txt file.")]
        return jokes_list
    except FileNotFoundError:
        return [("File Not Found Error.", "Make sure 'randomJokes.txt' is in the same directory.")]

# --- 2. Main Application Class ---
class JokeApp:
    def __init__(self, master):
        self.master = master
        master.title("Ancient Scroll Jokes")
        master.geometry("600x450")
        master.resizable(False, False)
        
        # --- Theme Colors & Fonts ---
        self.bg_color = "#386641"       
        self.frame_color = "#bc7e5c"    
        self.button_color = "#d9b38c"   
        self.text_color = "#4c3a27"     
        self.punchline_color = "#6a057d" 

        self.font_family = 'Arial Black' 
        self.font_large = (self.font_family, 16, 'bold')
        self.font_medium = (self.font_family, 14, 'bold')
        self.font_small = (self.font_family, 12)
        
        master.configure(bg=self.bg_color)

        self.jokes = load_jokes()
        self.current_joke = None
        
        # --- UI Elements Initialization (Same as before) ---
        
        self.main_frame = tk.Frame(master, bg=self.frame_color, bd=5, relief="groove")
        self.main_frame.pack(pady=30, padx=30, fill="both", expand=True)

        self.title_label = tk.Label(self.main_frame, text="THE SCROLL OF JOKES", 
                                    font=(self.font_family, 20, 'bold'),
                                    bg=self.frame_color, fg=self.text_color)
        self.title_label.pack(pady=(20, 10))

        self.setup_label = tk.Label(self.main_frame, text="Consult the Scroll for Wisdom!", 
                                    font=self.font_medium, wraplength=500, 
                                    bg=self.frame_color, fg=self.text_color, justify=tk.CENTER)
        self.setup_label.pack(pady=(10, 5), padx=20)

        self.punchline_label = tk.Label(self.main_frame, text="", 
                                        font=self.font_large, wraplength=500, 
                                        bg=self.frame_color, fg=self.punchline_color, justify=tk.CENTER)
        self.punchline_label.pack(pady=(5, 20), padx=20)
        
        self.button_frame = tk.Frame(self.main_frame, bg=self.frame_color)
        self.button_frame.pack(pady=10)

        self.new_joke_button = tk.Button(self.button_frame, text="Unfurl a Joke", command=self.tell_joke, 
                                        font=self.font_small, bg=self.button_color, fg=self.text_color, 
                                        activebackground=self.frame_color, relief="raised", bd=3)
        self.new_joke_button.pack(side=tk.LEFT, padx=10)

        self.punchline_button = tk.Button(self.button_frame, text="Reveal Truth", command=self.show_punchline, 
                                          font=self.font_small, bg=self.button_color, fg=self.text_color, 
                                          activebackground=self.frame_color, relief="raised", bd=3, state=tk.DISABLED)
        self.punchline_button.pack(side=tk.LEFT, padx=10)
        
        self.quit_button = tk.Button(self.main_frame, text="Seal the Scroll", command=master.quit, 
                                     font=self.font_small, bg="#a04d4a", fg="white", 
                                     activebackground="#8b3a37", relief="raised", bd=3)
        self.quit_button.pack(pady=20)


    # --- 3. Methods/Logic ---
    def tell_joke(self):
        """Randomly selects a joke, displays the setup, and hides the punchline."""
        if not self.jokes:
            self.setup_label.config(text="Alas, no jokes found in the ancient texts!")
            self.punchline_label.config(text="")
            self.punchline_button.config(state=tk.DISABLED)
            return

        self.current_joke = random.choice(self.jokes)
        setup, _ = self.current_joke

        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        self.punchline_button.config(state=tk.NORMAL)
        self.new_joke_button.config(text="Another Scroll")


    def show_punchline(self):
        """Displays the punchline for the current joke AND plays the laugh track."""
        if self.current_joke:
            _, punchline = self.current_joke
            self.punchline_label.config(text=punchline)
            self.punchline_button.config(state=tk.DISABLED)
            
            # --- NEW AUDIO LOGIC ---
            try:
                # Play the sound file (ensure 'laugh_track.mp3' exists in the same folder)
                playsound('laugh_track.wav', block=False)
            except Exception as e:
                # Catch error if file is missing or playsound fails
                print(f"Error playing sound: {e}. Make sure 'laugh_track.mp3' is present.")


# --- 4. Main Execution (Keep this section the same) ---
if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()