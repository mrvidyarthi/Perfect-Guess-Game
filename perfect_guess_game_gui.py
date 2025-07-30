import tkinter as tk
import random
import sys
import threading
import time
import cv2
from playsound import playsound

# Function to play the intro video
def play_intro_video(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("🎬 Game Intro", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

class PerfectGuessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 The Perfect Guess Game")
        self.root.geometry("450x430")
        self.root.configure(bg="#1e1e1e")
        self.setup_game()

    def setup_game(self):
        self.number_to_guess = random.randint(1, 100)
        self.attempts = 0

        for widget in self.root.winfo_children():
            widget.destroy()

        self.label_title = tk.Label(self.root, text="🎯 Welcome to The Perfect Guess Game!",
                                    font=("Helvetica", 16, "bold"), bg="#1e1e1e", fg="#ffffff")
        self.label_title.pack(pady=10)

        self.label_instruction = tk.Label(self.root, text="Enter a number between 1 and 100",
                                          font=("Arial", 12), bg="#1e1e1e", fg="#bbbbbb")
        self.label_instruction.pack(pady=2)

        self.entry_guess = tk.Entry(self.root, font=("Arial", 14), justify='center',
                                    bg="#2d2d2d", fg="#ffffff", insertbackground='white')
        self.entry_guess.pack(pady=8)
        self.entry_guess.focus()

        self.root.bind('<Return>', self.check_guess)

        self.button_submit = tk.Button(self.root, text="Submit Guess", command=self.check_guess,
                                       font=("Arial", 12, "bold"), bg="#4e9af1", fg="white",
                                       padx=10, pady=5, activebackground="#3b82f6")
        self.button_submit.pack(pady=5)

        self.label_result = tk.Label(self.root, text="", font=("Arial", 12),
                                     bg="#1e1e1e", fg="#dddddd")
        self.label_result.pack(pady=10)

        self.label_attempts = tk.Label(self.root, text="Attempts: 0", font=("Arial", 11),
                                       bg="#1e1e1e", fg="#888888")
        self.label_attempts.pack()

    def check_guess(self, event=None):
        guess = self.entry_guess.get()
        self.entry_guess.delete(0, tk.END)

        print(f"🔍 User guessed: {guess}")

        try:
            user_guess = int(guess)
            if user_guess < 1 or user_guess > 100:
                self.label_result.config(text="❗ Please enter a number between 1 and 100.", fg="orange")
                threading.Thread(target=playsound, args=("out_of_range.wav",), daemon=True).start()
                print("⚠️ Number out of valid range.")
                return

            self.attempts += 1
            self.label_attempts.config(text=f"Attempts: {self.attempts}")

            threading.Thread(target=playsound, args=("click.wav",), daemon=True).start()

            if user_guess > self.number_to_guess:
                self.label_result.config(text="⬇️ Lower number please!", fg="#fca5a5")
            elif user_guess < self.number_to_guess:
                self.label_result.config(text="⬆️ Higher number please!", fg="#a5d8fc")
            else:
                self.label_result.config(
                    text=f"🎉 Correct! It was {self.number_to_guess}.\nYou guessed it in {self.attempts} attempts.",
                    fg="#34d399"
                )
                threading.Thread(target=playsound, args=("win.wav",), daemon=True).start()
                self.button_submit.config(state=tk.DISABLED)
                self.entry_guess.config(state=tk.DISABLED)

                self.button_play_again = tk.Button(self.root, text="🔁 Play Again", command=self.play_again,
                                                   font=("Arial", 12, "bold"), bg="#34d399", fg="white",
                                                   padx=10, pady=5, activebackground="#10b981")
                self.button_play_again.pack(pady=10)

                self.button_end = tk.Button(self.root, text="🔚 End Game", command=self.end_game,
                                            font=("Arial", 12, "bold"), bg="#f87171", fg="white",
                                            padx=10, pady=5, activebackground="#ef4444")
                self.button_end.pack(pady=5)

        except ValueError:
            self.label_result.config(text="❌ Please enter a valid number (1–100).", fg="orange")
            threading.Thread(target=playsound, args=("out_of_range.wav",), daemon=True).start()
            print("⚠️ Invalid input.")

    def play_again(self):
        threading.Thread(target=playsound, args=("play_again.wav",), daemon=True).start()
        self.setup_game()

    def end_game(self):
        print("👋 Game Ended by User.")
        self.root.destroy()
        sys.exit()

# -------- Launch sequence --------
if __name__ == "__main__":
    play_intro_video("perfect_guess_intro_final.mp4")
    root = tk.Tk()
    app = PerfectGuessGame(root)
    root.mainloop()
