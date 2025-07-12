import tkinter as tk
import re
from tkinter import messagebox



# Function to remove Arabic diacritics
def remove_tashkeel(text):
    tashkeel_pattern = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    return tashkeel_pattern.sub('', text)

# Paste from clipboard
def paste_from_clipboard():
    try:
        clipboard_text = root.clipboard_get()
        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, clipboard_text)
    except tk.TclError:
        pass  # Clipboard is empty

# Process the text
def process_text():
    input_text = text_input.get("1.0", tk.END)
    result = remove_tashkeel(input_text)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, result)
    
def paste_from_clipboard():
    try:
        clipboard_text = root.clipboard_get()
        if re.search(r'[a-zA-Z]', clipboard_text):
            messagebox.showwarning("Invalid Input", "This tool supports Arabic text only.\nEnglish characters are not allowed.")
        else:
            text_input.delete("1.0", tk.END)
            text_input.insert(tk.END, clipboard_text)
    except tk.TclError:
        pass  # Clipboard is empty or invalid

def process_text():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showinfo("Empty Input", "Please paste or enter Arabic text before removing Tashkeel.")
        return
    result = remove_tashkeel(input_text)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, result)
    
def copy_output_to_clipboard():
    output_text = text_output.get("1.0", tk.END).strip()
    if output_text:
        root.clipboard_clear()
        root.clipboard_append(output_text)
        messagebox.showinfo("Copied", "Output text copied to clipboard.")
    else:
        messagebox.showwarning("Empty Output", "There is no text to copy.")

def clear_fields():
    text_input.delete("1.0", tk.END)
    text_output.delete("1.0", tk.END)
from tkinter import filedialog

def save_output_to_file():
    output_text = text_output.get("1.0", tk.END).strip()
    if not output_text:
        messagebox.showwarning("Empty Output", "There is no text to save.")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        title="Save Output As"
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(output_text)
        messagebox.showinfo("Saved", f"Output saved to:\n{file_path}")

# Window setup
root = tk.Tk()
root.title("Tashkeel Remover")
root.geometry("720x00")
root.configure(bg="#1e1e1e")

font = ("Cairo", 12)
fg_color = "white"
bg_color = "#1e1e1e"
root.iconbitmap("assets/icon.ico")


# Text input
text_input = tk.Text(root, height=5, font=font, fg=fg_color, bg=bg_color, insertbackground="white")
text_input.pack(padx=10, pady=(10, 5), fill=tk.X)

# Prevent typing English letters manually
def on_keypress(event):
    if not event.char:
        return
    if re.match(r'[a-zA-Z]', event.char):
        messagebox.showwarning("Invalid Input", "Only Arabic letters are allowed.")
        return "break"  # Prevent the character from being inserted

text_input.bind("<Key>", on_keypress)


# Button row (paste + remove)
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=5)

# Button row (paste + remove + copy)
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=5)

paste_btn = tk.Button(button_frame, text="📋 Paste", command=paste_from_clipboard, font=font, bg="#555", fg="white")
paste_btn.pack(side=tk.RIGHT, padx=10)

remove_btn = tk.Button(button_frame, text="🧹 Remove Tashkeel", command=process_text, font=font, bg="#444", fg="white")
remove_btn.pack(side=tk.RIGHT)

copy_btn = tk.Button(button_frame, text="📋 Copy Output", command=copy_output_to_clipboard, font=font, bg="#666", fg="white")
copy_btn.pack(side=tk.RIGHT, padx=10)

save_btn = tk.Button(button_frame, text="💾 Save Output", command=save_output_to_file, font=font, bg="#007744", fg="white")
save_btn.pack(side=tk.RIGHT, padx=10)

clear_btn = tk.Button(button_frame, text="🔄 Reset", command=clear_fields, font=font, bg="#880000", fg="white")
clear_btn.pack(side=tk.RIGHT, padx=10)


# Text output
text_output = tk.Text(root, height=5, font=font, fg=fg_color, bg=bg_color, insertbackground="white")
text_output.pack(padx=10, pady=5, fill=tk.X)

# Copyright label
copyright_label = tk.Label(
    root,
    text="2025 © All rights reserved to Sayed Aref",
    font=("Cairo", 9),
    fg="gray",
    bg=bg_color
)
copyright_label.pack(side=tk.LEFT, padx=10)

# Exit button
exit_button = tk.Button(root, text="⛔ Exit", command=root.quit, font=font, bg="#444", fg="white")
exit_button.pack(side=tk.RIGHT, padx=10)

root.mainloop()