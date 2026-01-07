import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

df = None

# ---------- Functions ----------

def load_excel():
    global df
    path = filedialog.askopenfilename(
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )
    if path:
        df = pd.read_excel(path)
        text.delete("1.0", tk.END)
        text.insert(tk.END, df.to_string())
        messagebox.showinfo("Success", "Excel file loaded successfully")

def update_data():
    try:
        row = int(entry_row.get())
        col = entry_col.get()
        value = entry_value.get()

        if col not in df.columns:
            messagebox.showerror("Error", "Column name not found")
            return

        df.loc[row, col] = value
        text.delete("1.0", tk.END)
        text.insert(tk.END, df.to_string())
        messagebox.showinfo("Updated", "Data updated successfully")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def save_excel():
    if df is not None:
        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")]
        )
        if save_path:
            df.to_excel(save_path, index=False)
            messagebox.showinfo("Saved", "Excel file saved successfully")

# ---------- UI ----------

root = tk.Tk()
root.title("Excel Editor")
root.geometry("1000x650")
root.configure(bg="#f4f6f8")

# Title
title = tk.Label(
    root,
    text="Excel File Editor",
    font=("Segoe UI", 22, "bold"),
    bg="#f4f6f8",
    fg="#2c3e50"
)
title.pack(pady=10)

# Button Frame
btn_frame = tk.Frame(root, bg="#f4f6f8")
btn_frame.pack(pady=5)

tk.Button(
    btn_frame,
    text="Load Excel File",
    command=load_excel,
    bg="#3498db",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    width=18
).grid(row=0, column=0, padx=10)

tk.Button(
    btn_frame,
    text="Save Excel File",
    command=save_excel,
    bg="#27ae60",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    width=18
).grid(row=0, column=1, padx=10)

# Edit Card
card = tk.Frame(root, bg="white", bd=2, relief="groove")
card.pack(pady=15, padx=20, fill="x")

tk.Label(card, text="Edit Cell Data", bg="white",
         font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=6, pady=10)

tk.Label(card, text="Row Index", bg="white").grid(row=1, column=0, padx=10)
entry_row = tk.Entry(card, width=10)
entry_row.grid(row=1, column=1)

tk.Label(card, text="Column Name", bg="white").grid(row=1, column=2, padx=10)
entry_col = tk.Entry(card, width=15)
entry_col.grid(row=1, column=3)

tk.Label(card, text="New Value", bg="white").grid(row=1, column=4, padx=10)
entry_value = tk.Entry(card, width=15)
entry_value.grid(row=1, column=5)

tk.Button(
    card,
    text="Update Cell",
    command=update_data,
    bg="#e67e22",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    width=20
).grid(row=2, column=0, columnspan=6, pady=12)

# Text Area
text_frame = tk.Frame(root, bg="#f4f6f8")
text_frame.pack(expand=True, fill="both", padx=20, pady=10)

text = tk.Text(
    text_frame,
    font=("Consolas", 11),
    bg="white",
    fg="#2c3e50",
    wrap="none"
)
text.pack(expand=True, fill="both")

root.mainloop()
