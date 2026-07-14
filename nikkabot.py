""" Run this command everytime in terminal when you change in modelfile    ollama create nikkabot-custom -f Modelfile"""
import tkinter as tk
from tkinter import scrolledtext, font
import ollama
import threading

def get_ai_response():
    user_input = user_entry.get()
    if not user_input.strip():
        return

    # Show what you said
    chat_display.configure(state='normal')
    chat_display.insert(tk.END, "You: " + user_input + "\n", "user_tag")
    user_entry.delete(0, tk.END)
    chat_display.configure(state='disabled')

    def fetch_ollama():
        try:
            # Note: make sure 'llama3' is what you pulled in step 2
            response = ollama.chat(model='nikkabot-custom', messages=[
                {'role': 'user', 'content': user_input},
            ])
            reply = response['message']['content']
            
            chat_display.configure(state='normal')
            chat_display.insert(tk.END, "NikkaBot: " + reply + "\n\n", "bot_tag")
            chat_display.see(tk.END)
            chat_display.configure(state='disabled')
        except Exception as e:
            chat_display.configure(state='normal')
            chat_display.insert(tk.END, f"System Error: {str(e)}\n")
            chat_display.configure(state='disabled')

    threading.Thread(target=fetch_ollama, daemon=True).start()

# --- UI SETUP ---
root = tk.Tk()
root.title("NikkaBot v1.0")
root.geometry("600x700")
root.configure(bg="#f5f5f7") # Mac-style light grey

# Nice fonts
custom_font = font.Font(family="SF Pro Text", size=13)

chat_display = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD, font=custom_font, bg="white", borderwidth=0)
chat_display.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Colors for the text
chat_display.tag_configure("user_tag", foreground="#007aff", font=(custom_font.actual("family"), 13, "bold"))
chat_display.tag_configure("bot_tag", foreground="#333333")

user_entry = tk.Entry(root, font=custom_font, highlightthickness=1, relief="flat")
user_entry.pack(padx=20, pady=(0, 10), fill=tk.X)
user_entry.bind("<Return>", lambda event: get_ai_response())
user_entry.focus_set()

# Small label for instructions
instructions = tk.Label(root, text="Press Enter to send", font=("SF Pro Text", 10), fg="grey", bg="#f5f5f7")
instructions.pack(pady=(0, 10))

root.mainloop()
