import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip
import os  

# Allowed special characters
SPECIAL_CHARACTERS = ["$", "@", "#", "&", "!"]

# Function to generate a strong password while maintaining randomized hint order
def generate_password():
    hint = hint_entry.get().strip()
    length = int(length_entry.get()) if length_entry.get().isdigit() else 12
    use_digits = digits_var.get()
    use_special = special_var.get()

    if not hint:
        messagebox.showerror("Error", "Please enter a hint!")
        return

    # Extract, clean, and randomize hints
    hint_parts = [part.strip() for part in hint.split(",") if part.strip()]
    random.shuffle(hint_parts)  # Randomize the order
    hint_password = "".join(hint_parts)  # Join them in the exact random order

    # Determine remaining length needed
    remaining_length = max(0, length - len(hint_password))

    # Generate extra security elements
    extra_chars = []

    if use_digits:
        extra_chars.append(random.choice(string.digits))
    if use_special:
        extra_chars.append(random.choice(SPECIAL_CHARACTERS))

    # Fill remaining length with random characters if needed
    all_chars = string.ascii_letters
    if use_digits:
        all_chars += string.digits
    if use_special:
        all_chars += "".join(SPECIAL_CHARACTERS)

    extra_chars += [random.choice(all_chars) for _ in range(remaining_length - len(extra_chars))]

    # Combine password with hints in randomized order
    final_password = hint_password + "".join(extra_chars)

    # Display password
    password_entry.delete(0, tk.END)
    password_entry.insert(0, final_password)
    check_strength(final_password)

# Function to check password strength
def check_strength(password):
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in SPECIAL_CHARACTERS for c in password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)

    if len(password) >= 12 and has_digit and has_special and has_upper and has_lower:
        strength = "Strong 💪"
    elif len(password) >= 8 and (has_digit or has_special):
        strength = "Medium ⚡"
    else:
        strength = "Weak ❌"

    strength_label.config(text=f"Strength: {strength}")

# Function to save password
def save_password():
    password = password_entry.get()
    if password:
        file_path = "passwords.txt"
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write("Saved Passwords:\n")

        with open(file_path, "a") as file:
            file.write(password + "\n")
        messagebox.showinfo("Saved", "Password saved successfully!")
    else:
        messagebox.showwarning("Warning", "No password to save!")

# Function to copy password to clipboard
def copy_to_clipboard():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# Setup Main Window
root = tk.Tk()
root.title("🔐 Password Generator")
root.geometry("650x500")  # Broader window size
root.resizable(False, False)
root.configure(bg="#1E1E2E")  # Classy dark background

# Title Label
title_label = tk.Label(root, text="Password Generator", font=("Helvetica", 18, "bold"), fg="white", bg="#1E1E2E")
title_label.pack(pady=10)

# Main Frame
frame = tk.Frame(root, bg="#282A36", padx=20, pady=20)
frame.pack(pady=10)

# Hint Entry
tk.Label(frame, text="Enter Hints (Comma-Separated):", font=("Helvetica", 12, "bold"), bg="#282A36", fg="white").grid(row=0, column=0, pady=5, sticky="w")
hint_entry = tk.Entry(frame, font=("Helvetica", 12), width=30)
hint_entry.grid(row=0, column=1, pady=5)

# Password Length Entry
tk.Label(frame, text="Password Length:", font=("Helvetica", 12, "bold"), bg="#282A36", fg="white").grid(row=1, column=0, pady=5, sticky="w")
length_entry = tk.Entry(frame, font=("Helvetica", 12), width=5)
length_entry.grid(row=1, column=1, pady=5)
length_entry.insert(0, "12")

# Checkboxes for Digits & Special Characters
digits_var = tk.BooleanVar()
special_var = tk.BooleanVar()

digits_check = tk.Checkbutton(frame, text="Include Digits", variable=digits_var, font=("Helvetica", 10, "bold"), bg="#282A36", fg="white", selectcolor="#282A36", activebackground="#282A36", activeforeground="white")
digits_check.grid(row=2, column=0, pady=5, sticky="w")

special_check = tk.Checkbutton(frame, text="Include Special Characters", variable=special_var, font=("Helvetica", 10, "bold"), bg="#282A36", fg="white", selectcolor="#282A36", activebackground="#282A36", activeforeground="white")
special_check.grid(row=3, column=0, pady=5, sticky="w")

# Generate Button
generate_btn = tk.Button(frame, text="Generate Password", command=generate_password, font=("Helvetica", 12, "bold"), bg="#FF5733", fg="white", padx=10, pady=5)
generate_btn.grid(row=4, column=0, columnspan=2, pady=10)

# Password Display
password_entry = tk.Entry(root, font=("Helvetica", 14, "bold"), width=45, justify="center", bd=2)
password_entry.pack(pady=10)

# Strength Label
strength_label = tk.Label(root, text="Strength: ", font=("Helvetica", 12, "bold"), fg="white", bg="#1E1E2E")
strength_label.pack()

# Buttons Frame
btn_frame = tk.Frame(root, bg="#1E1E2E")
btn_frame.pack(pady=10)

# Copy Button
copy_btn = tk.Button(btn_frame, text="📋 Copy", command=copy_to_clipboard, font=("Helvetica", 10, "bold"), bg="#3498DB", fg="white", padx=10, pady=5)
copy_btn.grid(row=0, column=0, padx=10)

# Save Button
save_btn = tk.Button(btn_frame, text="💾 Save", command=save_password, font=("Helvetica", 10, "bold"), bg="#27AE60", fg="white", padx=10, pady=5)
save_btn.grid(row=0, column=1, padx=10)

# Run GUI
root.mainloop()
