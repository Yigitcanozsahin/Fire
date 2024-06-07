import api
import tkinter as tk
from tkinter import messagebox, Menu
from datetime import datetime
import os

conversation_history = []

def copy_text(event):
    if response_area.tag_ranges(tk.SEL):
        selected_text = response_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        root.clipboard_clear()
        root.clipboard_append(selected_text)

def show_context_menu(event):
    if event.buttons == 1:  # Check if left mouse button is clicked
        context_menu.post(event.x_root, event.y_root)

def copy_text_entry_box():
    selected_text = entry_box.get()
    root.clipboard_clear()
    root.clipboard_append(selected_text)

def paste_text_entry_box():
    entry_box.delete(0, tk.END)
    entry_box.insert(0, root.clipboard_get())

def on_entry_click(event):
    if entry_box.get() == "Enter your question...":
        entry_box.delete(0, tk.END)
        entry_box.insert(0, '')
        entry_box.config(fg='black')

def on_focusout(event):
    if entry_box.get() == '':
        entry_box.insert(0, "Enter your question...")
        entry_box.config(fg='grey')

def clear_response_area():
    response_area.config(state=tk.NORMAL)
    response_area.delete(1.0, tk.END)
    response_area.config(state=tk.DISABLED)

def send_question(event=None):
    question = entry_box.get()
    if question == "Enter your question...":
        messagebox.showwarning("Warning", "Please enter a question.")
        return

    entry_box.delete(0, tk.END)

    if conversation_history:
        last_question = conversation_history[-1]["question"]
        last_response = conversation_history[-1]["response"]

        prompt_parts = [f"{last_response}\n\nUser: {question}"]
        response = api.model.generate_content(prompt_parts)

        response_area.config(state=tk.NORMAL)  # Make response_area editable

        # Add the user question to the response area
        response_area.insert(tk.END, f"You: {question}\n\n", "default")

        # Add AI's response to the response area
        in_code_block = False
        response_lines = response.text.split('\n')

        for line in response_lines:
            if line.startswith("```") and line.endswith("```"):
                response_area.insert(tk.END, f"{line}\n", "code")
                in_code_block = not in_code_block
            elif in_code_block:
                response_area.insert(tk.END, f"{line}\n", "code")
            else:
                response_area.insert(tk.END, f"{line}\n", "default")  # Default tag for non-code lines

        response_area.insert(tk.END, "▬"*116 + "\n")

        response_area.config(state=tk.DISABLED)  # Disable editing after inserting text
        response_area.yview(tk.END)

        # Save the conversation to a file
        save_to_file(f"You: {question}\n\n{response.text}")

        # Add the question and response to the conversation history
        conversation_history.append({"question": question, "response": response.text})

# Conversation save file
def save_to_file(content):
    today_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today_date}_conversation.txt"
    os.makedirs("conversations", exist_ok=True)

    with open(os.path.join("conversations", filename), "a") as f:
        f.write(content)
        f.write("\n"*3)

root = tk.Tk()
root.title("AI Assistant")

entry_box = tk.Entry(root, width=60, bg='grey', fg='black', font=('Helvetica', 14))
entry_box.pack(padx=10, pady=10)
entry_box.insert(0, "Enter your question...")
entry_box.bind("<Return>", send_question)
entry_box.bind("<Button-1>", on_entry_click)
entry_box.bind("<FocusOut>", on_focusout)

response_area = tk.Text(root, wrap=tk.WORD, width=60, height=20, bg='lightgrey', fg='black', font=('Helvetica', 14))
response_area.pack(padx=10, pady=10)
response_area.config(state=tk.DISABLED)

clear_button = tk.Button(root, text="Clear", width=10, command=clear_response_area)
clear_button.pack(side=tk.RIGHT, padx=10, pady=10)

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Copy", command=copy_text)
context_menu.add_command(label="Paste", command=paste_text_entry_box)
context_menu.add_command(label="Delete", command=lambda: entry_box.delete(0, tk.END))
context_menu.bind("<Leave>", lambda event: context_menu.unpost())

root.bind("<Control-c>", copy_text)
root.bind("<Control-v>", paste_text_entry_box)
root.bind("<Button-3>", show_context_menu)  # Change to right mouse button

root.mainloop()