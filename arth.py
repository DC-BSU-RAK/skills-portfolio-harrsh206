import tkinter as tk
import random
from playsound import playsound # play mp3 or wav

# --------------------------
# GLOBAL VARS FOR TIMER
# --------------------------
timer_id = None
time_left = 0

# --------------------------
# QUIZ LOGIC
# --------------------------
def randomInt(level):
    if level == "easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "moderate":
        return random.randint(10, 99), random.randint(10, 99)
    else:
        return random.randint(1000, 9999), random.randint(1000, 9999)

def decideOperation():
    return random.choice(["+", "-"])

def isCorrect(num1, num2, op, ans):
    # Using eval is generally risky, but acceptable here for simple math quiz logic
    return ans == eval(f"{num1}{op}{num2}")

# --------------------------
# SOUND EFFECTS
# --------------------------
def play_correct_sound():
    try:
        playsound("correct.wav", block=False)
    except:
        pass # ignore if file not found or unsupported

def play_fail_sound():
    try:
        playsound("wrong.wav", block=False)
    except:
        pass

def play_finish_sound():
    """Plays a special sound effect when the quiz is completed successfully."""
    try:
        playsound("finish.wav", block=False) # Requires a 'finish.wav' file
    except:
        pass

def play_fail_score_sound():
    """Plays a sound effect when the final score is less than 50."""
    try:
        playsound("low_score.wav", block=False) # Requires a 'low_score.wav' file
    except:
        pass

# --------------------------
# CUSTOM UI COMPONENTS
# --------------------------
def create_bubbly_button(parent, text, command=None, width=16):
    """Creates a cartoon-style orange button."""
    frame = tk.Frame(parent, bg="#ff9248", bd=4, relief="ridge", highlightbackground="#ff4500", highlightthickness=2)
    btn = tk.Label(frame, text=text, bg="#ff9248", fg="white", font=("Comic Sans MS", 16, "bold"), width=width, height=1)
    btn.pack(padx=2, pady=2)

    def on_enter(e):
        btn.config(bg="#ff7a33", cursor="hand2")
        frame.config(bg="#ff7a33")
    def on_leave(e):
        btn.config(bg="#ff9248")
        frame.config(bg="#ff9248")
    def on_click(e):
        if command:
            command()

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<Button-1>", on_click)

    return frame

# --------------------------
# TIMER LOGIC
# --------------------------
def start_timer(seconds, entry_widget, submit_button, feedback_label, timer_label):
    """Starts the countdown timer for the current question."""
    global time_left, timer_id, num1, num2, operation
    time_left = seconds
    
    # Cancel any existing timer
    if timer_id:
        root.after_cancel(timer_id)

    def countdown():
        global time_left, timer_id
        if time_left > 0:
            time_left -= 1
            timer_label.config(text=f"Time: {time_left}s")
            timer_id = root.after(1000, countdown) # Schedule next update
        else:
            # Time's up!
            timer_label.config(text="Time's Up!", fg="red")
            feedback_label.config(text=f"⏰ Time's Up! Ans: {eval(f'{num1}{operation}{num2}')}", fg="red")
            
            # Disable input and submission
            entry_widget.config(state='disabled')
            submit_button.pack_forget() # Hide the submit button
            
            play_fail_sound()
            root.unbind("<Return>") # Unbind the Enter key
            
            root.after(1500, next_question) # Move to next question after delay

    countdown()

# --------------------------
# SCREENS
# --------------------------
def displayMenu():
    # Cancel timer if returning from quiz
    global timer_id
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None
        
    for w in root.winfo_children():
        w.destroy()

    root.configure(bg="#fff1e0")

    tk.Label(root, text="🧮 ARITHMETIC QUIZ 🧮",
             bg="#fff1e0", fg="#ff4500",
             font=("Comic Sans MS", 24, "bold")).place(relx=0.5, rely=0.1, anchor="center")

    frame = tk.Frame(root, bg="#fff1e0")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    create_bubbly_button(frame, "🟢 Easy (10s)", lambda: start_quiz("easy")).pack(pady=10)
    create_bubbly_button(frame, "🟠 Moderate (20s)", lambda: start_quiz("moderate")).pack(pady=10)
    create_bubbly_button(frame, "🔴 Advanced (30s)", lambda: start_quiz("advanced")).pack(pady=10)

def displayProblem():
    global num1, num2, operation, attempt, timer_id, time_left
    attempt = 1
    num1, num2 = randomInt(difficulty)
    operation = decideOperation()

    # Determine time limit based on difficulty
    if difficulty == "easy":
        time_limit = 10
    elif difficulty == "moderate":
        time_limit = 20
    else:
        time_limit = 30 # advanced

    # Clear screen
    for w in root.winfo_children():
        w.destroy()

    root.configure(bg="#fff1e0")

    # --- Header Frame (for Back and Difficulty) ---
    header_frame = tk.Frame(root, bg="#fff1e0")
    header_frame.pack(pady=10, fill="x")

    tk.Label(header_frame, text=f"Difficulty: {difficulty.capitalize()}",
             bg="#fff1e0", fg="#ff7043",
             font=("Comic Sans MS", 14, "bold")).pack(side="left", padx=20)

    back_btn = create_bubbly_button(header_frame, "⬅ Back", displayMenu, width=8)
    back_btn.pack(side="right", padx=20)
    
    # --- Timer Label (Placed in the center top) ---
    timer_label = tk.Label(root, text=f"Time: {time_limit}s", 
                           bg="#fff1e0", fg="#004d40", 
                           font=("Comic Sans MS", 16, "bold"), 
                           padx=10, pady=5, 
                           relief="ridge", bd=2)
    timer_label.place(relx=0.5, rely=0.18, anchor="center") # Centered placement

    tk.Label(root, text=f"Question {question_number + 1}/10",
             bg="#fff1e0", fg="#ff4500",
             font=("Comic Sans MS", 16, "bold")).pack(pady=50) # Increased padding to account for timer

    tk.Label(root, text=f"{num1} {operation} {num2} =",
             bg="#fff1e0", fg="#e64a19",
             font=("Impact", 40)).pack(pady=10)

    entry = tk.Entry(root, font=("Comic Sans MS", 22), justify="center", width=6, bd=3, relief="ridge")
    entry.pack(pady=10)
    entry.focus()

    feedback = tk.Label(root, text="", bg="#fff1e0", font=("Comic Sans MS", 16))
    feedback.pack(pady=10)

    submit_btn_frame = create_bubbly_button(root, "✅ Submit", lambda: submit(entry, feedback, submit_btn_frame), width=16)
    submit_btn_frame.pack(pady=20)


    def submit(entry_widget, feedback_label, submit_frame, event=None):
        global score, question_number, attempt, timer_id
        
        # Cancel the timer immediately upon submission
        if timer_id:
            root.after_cancel(timer_id)
            timer_id = None
        
        try:
            ans = int(entry_widget.get())
        except ValueError:
            feedback_label.config(text="⚠️ Enter a number!", fg="red")
            play_fail_sound()
            # Restart the timer since it was a non-scoring attempt
            start_timer(time_left, entry, submit_frame, feedback, timer_label)
            return

        # Disable input and submission while processing
        entry_widget.config(state='disabled')
        submit_frame.pack_forget()
        root.unbind("<Return>")

        if isCorrect(num1, num2, operation, ans):
            feedback_label.config(text="✅ Correct!", fg="green")
            play_correct_sound()
            if attempt == 1:
                score += 10
            elif attempt == 2:
                score += 7
            else:
                score += 5
            root.after(1000, next_question)
        else:
            play_fail_sound()
            if attempt < 3:
                feedback_label.config(text=f"❌ Wrong! Attempt {attempt}/3", fg="red")
                attempt += 1
                entry_widget.delete(0, tk.END)
                # Re-enable input and submission, restart timer
                entry_widget.config(state='normal')
                entry_widget.focus()
                submit_frame.pack(pady=20)
                root.bind("<Return>", lambda e: submit(entry, feedback, submit_frame))
                # Restart timer with remaining time
                start_timer(time_left, entry, submit_frame, feedback, timer_label)
            else:
                feedback_label.config(text=f"❌ Out of tries! Ans: {eval(f'{num1}{operation}{num2}')}", fg="red")
                root.after(1500, next_question)

    # Bind Enter key to the submit function
    root.bind("<Return>", lambda e: submit(entry, feedback, submit_btn_frame))

    # Start the timer!
    start_timer(time_limit, entry, submit_btn_frame, feedback, timer_label)

def next_question():
    global question_number, timer_id
    
    # Ensure any running timer is cancelled before moving on
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None
        
    question_number += 1
    if question_number < 10:
        displayProblem()
    else:
        displayResults()

def displayResults():
    # Final cleanup of the timer
    global timer_id, score
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None
        
    # Decide which sound to play based on the final score
    if score >= 50:
        play_finish_sound()
    else:
        play_fail_score_sound() # New fail sound for low score
        
    for w in root.winfo_children():
        w.destroy()

    root.configure(bg="#fff1e0")

    # Determine message and color based on performance
    result_text = "🎉 QUIZ COMPLETE! WELL DONE! 🎉" if score >= 50 else "😔 QUIZ COMPLETE! TRY HARDER! 😔"
    result_color = "#4CAF50" if score >= 50 else "#F44336"

    tk.Label(root, text=result_text,
             bg="#fff1e0", fg=result_color,
             font=("Comic Sans MS", 24, "bold")).pack(pady=20)

    tk.Label(root, text=f"Score: {score}/100", bg="#fff1e0", fg="#e64a19",
             font=("Comic Sans MS", 18, "bold")).pack(pady=10)

    grade = "A+" if score >= 90 else "A" if score >= 80 else "B" if score >= 70 else "C" if score >= 60 else "F"
    tk.Label(root, text=f"Grade: {grade}", bg="#fff1e0", fg="#ff7043",
             font=("Comic Sans MS", 18, "bold")).pack(pady=10)

    frame = tk.Frame(root, bg="#fff1e0")
    frame.pack(pady=20)

    create_bubbly_button(frame, "🔁 Play Again", displayMenu).pack(pady=5)
    create_bubbly_button(frame, "🚪 Exit", root.destroy).pack(pady=5)

def start_quiz(level):
    global difficulty, score, question_number
    difficulty = level
    score = 0
    question_number = 0
    displayProblem()


# --------------------------
# MAIN APP SETUP
# --------------------------
root = tk.Tk()
root.title("🎮 Arithmetic Quiz Game")
root.geometry("520x520")
root.resizable(False, False)
displayMenu()
root.mainloop()