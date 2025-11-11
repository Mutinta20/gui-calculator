import tkinter as tk
from tkinter import ttk, messagebox
import math

# -----------------------------
# Global history & memory
# -----------------------------
history = []
memory = 0.0

# -----------------------------
# Arithmetic Functions
# -----------------------------
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        messagebox.showerror("Error", "Division by zero is not allowed.")
        return None
    return a / b
def modulus(a, b):
    if b == 0:
        messagebox.showerror("Error", "Division by zero is not allowed.")
        return None
    return a % b
def power(a, b): return a ** b
def square_root(a):
    if a < 0:
        messagebox.showerror("Error", "Square root of negative number is not allowed.")
        return None
    return math.sqrt(a)

# -----------------------------
# History Functions
# -----------------------------
def update_history(expression, result):
    if result is not None:
        entry = f"{expression} = {result}"
        history.append(entry)
        history_text.insert(tk.END, entry + "\n")

def clear_history():
    history.clear()
    history_text.delete(1.0, tk.END)


# Memory Functions

def memory_add(value):
    global memory
    memory += value
    mem_label.config(text=f"M = {memory}")
    messagebox.showinfo("Memory", f"Added {value} to memory (M = {memory})")

def memory_subtract(value):
    global memory
    memory -= value
    mem_label.config(text=f"M = {memory}")
    messagebox.showinfo("Memory", f"Subtracted {value} from memory (M = {memory})")

def memory_recall():
    global memory
    entry1.delete(0, tk.END)
    entry1.insert(0, str(memory))
    messagebox.showinfo("Memory Recall", f"Recalled M = {memory}")

def memory_clear():
    global memory
    memory = 0.0
    mem_label.config(text=f"M = {memory}")
    messagebox.showinfo("Memory", "Memory cleared (M = 0)")
#CHANGE: safer number retrieval for empty/invalid entries
def safe_get_entry(entry):
    try:
        return float(entry.get())
    except (ValueError, TypeError):
        return 0.0

# -----------------------------
# Calculator Logic
# -----------------------------
def calculate(operator):
    try:
        num1 = float(entry1.get())
        num2 = None
        if operator not in ["√"]:  # square root needs only one input
            num2 = float(entry2.get())

        if operator == "+":
            result = add(num1, num2)
            expression = f"{num1} + {num2}"
        elif operator == "-":
            result = subtract(num1, num2)
            expression = f"{num1} - {num2}"
        elif operator == "*":
            result = multiply(num1, num2)
            expression = f"{num1} * {num2}"
        elif operator == "/":
            result = divide(num1, num2)
            expression = f"{num1} / {num2}"
        elif operator == "%":
            result = modulus(num1, num2)
            expression = f"{num1} % {num2}"
        elif operator == "^":
            result = power(num1, num2)
            expression = f"{num1} ^ {num2}"
        elif operator == "√":
            result = square_root(num1)
            expression = f"√{num1}"
        else:
            result = None
            expression = ""

        if result is not None:
            result_label.config(text=f"Result: {result}")
            update_history(expression, result)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")

# -----------------------------
# GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Python Calculator (Advanced)")
root.geometry("450x600")

# Input fields
tk.Label(root, text="Enter first number:").pack()
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="Enter second number (if needed):").pack()
entry2 = tk.Entry(root)
entry2.pack()

# Operation buttons
ops = ttk.Frame(main_frame)
ops.grid(row=2, column=0, columnspan=2, pady=12, sticky="ew")
for c in range(4):
    ops.columnconfigure(c, weight=1)

tk.Button(frame, text="+", width=15, command=lambda: calculate("+")).grid(row=0, column=0)
tk.Button(frame, text="-", width=15, command=lambda: calculate("-")).grid(row=0, column=1)
tk.Button(frame, text="*", width=15, command=lambda: calculate("*")).grid(row=0, column=2)
tk.Button(frame, text="/", width=15, command=lambda: calculate("/")).grid(row=0, column=3)
tk.Button(frame, text="%", width=15, command=lambda: calculate("%")).grid(row=0, column=4)

tk.Button(frame, text="^", width=15, command=lambda: calculate("^")).grid(row=1, column=0)
tk.Button(frame, text="√", width=15, command=lambda: calculate("√")).grid(row=1, column=1)

# Result display
result_label = tk.Label(root, text="Result: ")
result_label.pack(pady=15)

# History display
tk.Label(root, text="Calculation History:").pack()
history_text = tk.Text(root, height=10, width=50)
history_text.pack()

tk.Button(root, text="Clear History", command=clear_history).pack(pady=5)

#  Memory buttons
# FIX: Changed parent from undefined 'main_frame' to 'root', and changed .grid() to .pack()
mem_frame = ttk.LabelFrame(root, text="Memory Functions", padding=8)
mem_frame.pack(pady=10, fill="x", padx=10) # Use pack and fill to make it look nice

tk.Button(mem_frame, text="M+", width=5, command=lambda: memory_add(float(entry1.get() or 0))).grid(row=0, column=0)
tk.Button(mem_frame, text="M-", width=5, command=lambda: memory_subtract(float(entry1.get() or 0))).grid(row=0, column=1)
tk.Button(mem_frame, text="MR", width=5, command=memory_recall).grid(row=0, column=2)
tk.Button(mem_frame, text="MC", width=5, command=memory_clear).grid(row=0, column=3)

# Exit button (button)
ttk.Button(main_frame, text="Exit", command=root.destroy).grid(row=7, column=0, columnspan=2, pady=10)

entry1.focus_set()

# Run the GUI
root.mainloop()
