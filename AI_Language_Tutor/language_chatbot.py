import sqlite3
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables to connect Genini API key to chat with AI.
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Using Gemini 1.5 flash model
model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=[])

# Setup Database using SQLite
conn = sqlite3.connect("mistakes.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS mistakes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT,
    correct_text TEXT,
    feedback TEXT
)
""")
conn.commit()

def log_mistake(user_input, correct_text, feedback):
    cursor.execute("INSERT INTO mistakes (user_input, correct_text, feedback) VALUES (?, ?, ?)",
                   (user_input, correct_text, feedback))
    conn.commit()

# Creating a GUI to interact with user
class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Learning Chatbot)")
        self.root.geometry("600x500")

        ttk.Label(root, text="Language Learning Chatbot", font=("Arial", 14, "bold")).pack(pady=5)

        # Language Settings
        frame1 = ttk.Frame(root)
        frame1.pack(pady=5)

        ttk.Label(frame1, text="Learn:").grid(row=0, column=0, padx=5)
        self.learning_lang = ttk.Combobox(frame1, values=["French", "Spanish", "German", "Japanese"])
        self.learning_lang.grid(row=0, column=1)
        self.learning_lang.set("French")

        ttk.Label(frame1, text="Fluent in:").grid(row=0, column=2, padx=5)
        self.known_lang = ttk.Combobox(frame1, values=["English", "Hindi", "Spanish", "German"])
        self.known_lang.grid(row=0, column=3)
        self.known_lang.set("English")

        ttk.Label(frame1, text="Level:").grid(row=0, column=4, padx=5)
        self.level = ttk.Combobox(frame1, values=["Beginner", "Intermediate", "Advanced"])
        self.level.grid(row=0, column=5)
        self.level.set("Beginner")

        self.start_button = ttk.Button(root, text="Start Chat", command=self.start_chat)
        self.start_button.pack(pady=5)

        self.chat_display = scrolledtext.ScrolledText(root, height=15, wrap=tk.WORD)
        self.chat_display.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        frame2 = ttk.Frame(root)
        frame2.pack(pady=5)

        self.user_input = ttk.Entry(frame2, width=50, font=("bold", 12))
        self.user_input.grid(row=0, column=0, padx=5)

        self.send_button = ttk.Button(frame2, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=5)

        self.exit_button = ttk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack(pady=5)

    def start_chat(self):
        try:
            prompt = f"You are a friendly language tutor. Help the user practice {self.learning_lang.get()}. So tell 10-15 commonly used words in the selected languages with meanings then asked 10 questions upon the words you have given. According to the answers given by user provide feedback and rate the answers out of 10."
            response = chat.send_message(prompt)
            self.chat_display.insert(tk.END, f"\nBot: {response.text.strip()}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def send_message(self):
        user_input = self.user_input.get().strip()
        if not user_input:
            return

        self.chat_display.insert(tk.END, f"\nYou: {user_input}")
        self.user_input.delete(0, tk.END)

        if user_input.lower() == "exit":
            self.show_mistakes()
            return

        try:
            response = chat.send_message(user_input)
            self.chat_display.insert(tk.END, f"\nBot: {response.text.strip()}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # Grammar correction
        try:
            correction_prompt = f"The user said: \"{user_input}\" in {self.learning_lang.get()}.\n" \
                                f"Correct any grammar or vocabulary mistakes and provide a brief explanation. " \
                                f"If it's perfect, respond with: No mistakes."
            correction_response = chat.send_message(correction_prompt)
            correction = correction_response.text.strip()

            if "no mistakes" not in correction.lower():
                correct_text, feedback = correction.split("\n", 1) if "\n" in correction else (correction, "")
                log_mistake(user_input, correct_text, feedback)
                self.chat_display.insert(tk.END, f"\n(Correction: {correct_text})\n(Note: {feedback})\n\n")
        except Exception as e:
            self.chat_display.insert(tk.END, f"\n(Error checking grammar: {str(e)})\n")

    def show_mistakes(self):
        cursor.execute("SELECT user_input, correct_text, feedback FROM mistakes")
        mistakes = cursor.fetchall()

        if not mistakes:
            messagebox.showinfo("Mistake Review", "No mistakes recorded!")
            return

        review = "\n### Review of Mistakes ###\n"
        for i, (user_input, correct_text, feedback) in enumerate(mistakes, 1):
            review += f"{i}. You said: {user_input}\n   Correct: {correct_text}\n   Feedback: {feedback}\n\n"

        mistake_window = tk.Toplevel(self.root)
        mistake_window.title("Mistake Review")
        mistake_window.geometry("500x400")

        text_area = scrolledtext.ScrolledText(mistake_window, wrap=tk.WORD)
        text_area.pack(expand=True, fill=tk.BOTH)
        text_area.insert(tk.END, review)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotGUI(root)
    root.mainloop()
