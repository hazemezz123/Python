import tkinter as tk
from tkinter import scrolledtext, ttk
from atbash import atbash_encrypt

def encrypt_text():
    user_input = text_input.get("1.0", tk.END).strip()
    encrypted_text = atbash_encrypt(user_input)
    result_output.config(state=tk.NORMAL)
    result_output.delete("1.0", tk.END)
    result_output.insert(tk.END, encrypted_text)
    result_output.config(state=tk.DISABLED)

app = tk.Tk()
app.title("Atbash Encryption Tool")
app.geometry("500x400")
app.resizable(False, False)

# Style configuration
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12))

# Input Label
input_label = ttk.Label(app, text="Enter text to encrypt:")
input_label.pack(pady=5)

# Input Text Area
text_input = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=50, height=10, font=("Helvetica", 10))
text_input.pack(pady=10)

# Encrypt Button
encrypt_button = ttk.Button(app, text="Encrypt", command=encrypt_text)
encrypt_button.pack(pady=10)

# Output Label
output_label = ttk.Label(app, text="Encrypted text:")
output_label.pack(pady=5)

# Output Text Area
result_output = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=50, height=10, font=("Helvetica", 10), state=tk.DISABLED)
result_output.pack(pady=10)

app.mainloop()