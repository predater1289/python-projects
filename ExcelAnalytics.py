import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, ttk, messagebox

df = None

# ---------------- FUNCTIONS ---------------- #
def load_excel():
    global df
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )
    if file_path:
        df = pd.read_excel(file_path)
        update_table()
        update_kpi()

def update_kpi():
    rows_var.set(str(df.shape[0]))
    cols_var.set(str(df.shape[1]))
    num_var.set(str(df.select_dtypes(include='number').shape[1]))

def update_table():
    tree.delete(*tree.get_children())
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=140, anchor=CENTER)

    for _, row in df.iterrows():
        tree.insert("", END, values=list(row))

def show_chart():
    if df is None:
        messagebox.showerror("Error", "Please upload an Excel file first")
        return

    chart = chart_type.get()
    num_df = df.select_dtypes(include='number')

    if num_df.empty:
        messagebox.showerror("Error", "No numeric columns found")
        return

    plt.close('all')  # 🔥 FIX: close old figures

    if chart == "Bar Chart":
        num_df.plot(kind='bar', figsize=(8,5))
    elif chart == "Line Chart":
        num_df.plot(kind='line', figsize=(8,5))
    elif chart == "Pie Chart":
        num_df.iloc[0].plot(kind='pie', autopct='%1.1f%%', figsize=(6,6))
    elif chart == "Histogram":
        num_df.plot(kind='hist', figsize=(8,5))
    elif chart == "Scatter Plot":
        if num_df.shape[1] >= 2:
            plt.figure(figsize=(8,5))
            plt.scatter(num_df.iloc[:,0], num_df.iloc[:,1])
            plt.xlabel(num_df.columns[0])
            plt.ylabel(num_df.columns[1])
        else:
            messagebox.showwarning("Warning", "Scatter plot needs 2 numeric columns")
            return
    elif chart == "Area Chart":
        num_df.plot(kind='area', figsize=(8,5))
    elif chart == "Box Plot":
        num_df.plot(kind='box', figsize=(8,5))

    plt.title(chart)
    plt.tight_layout()
    plt.show()

# ---------------- UI SETUP ---------------- #
root = Tk()
root.title("ExcelInsight AI Dashboard")
root.geometry("1300x720")
root.configure(bg="#f1f5f9")

# Header
header = Frame(root, bg="#0f172a", height=70)
header.pack(fill=X)
Label(
    header, text="ExcelInsight AI",
    fg="white", bg="#0f172a",
    font=("Segoe UI", 22, "bold")
).pack(anchor=W, padx=30, pady=5)
Label(
    header, text="Advanced Excel Data Visualization Dashboard",
    fg="#cbd5f5", bg="#0f172a",
    font=("Segoe UI", 11)
).pack(anchor=W, padx=30)

# KPI Section
kpi_frame = Frame(root, bg="#f1f5f9")
kpi_frame.pack(fill=X, padx=30, pady=15)

def kpi_card(parent, title, var):
    card = Frame(parent, bg="white", width=200, height=90)
    card.pack(side=LEFT, padx=15)
    Label(card, text=title, bg="white", fg="#64748b").pack(anchor=W, padx=15, pady=5)
    Label(card, textvariable=var, bg="white", fg="#1e40af",
          font=("Segoe UI", 22, "bold")).pack(anchor=W, padx=15)

rows_var = StringVar(value="0")
cols_var = StringVar(value="0")
num_var  = StringVar(value="0")

kpi_card(kpi_frame, "Total Rows", rows_var)
kpi_card(kpi_frame, "Total Columns", cols_var)
kpi_card(kpi_frame, "Numeric Columns", num_var)

# Main Content
content = Frame(root, bg="#f1f5f9")
content.pack(fill=BOTH, expand=True, padx=20)

# Sidebar
sidebar = Frame(content, bg="#1e293b", width=220)
sidebar.pack(side=LEFT, fill=Y)

Button(
    sidebar, text="📂 Upload Excel",
    font=("Segoe UI", 12),
    bg="#1e40af", fg="white",
    bd=0, command=load_excel
).pack(pady=30, padx=20, fill=X)

# Table Area
table_frame = Frame(content, bg="white")
table_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=20)

tree = ttk.Treeview(table_frame)
tree.pack(side=LEFT, fill=BOTH, expand=True)

scroll = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
scroll.pack(side=RIGHT, fill=Y)
tree.configure(yscrollcommand=scroll.set)

# Chart Controls
control = Frame(root, bg="#f1f5f9")
control.pack(fill=X, padx=40, pady=10)

chart_type = StringVar(value="Bar Chart")
ttk.Combobox(
    control, textvariable=chart_type,
    values=[
        "Bar Chart", "Line Chart", "Pie Chart",
        "Histogram", "Scatter Plot",
        "Area Chart", "Box Plot"
    ],
    state="readonly", width=22
).pack(side=LEFT, padx=10)

Button(
    control, text="📊 Generate Chart",
    bg="#10b981", fg="white",
    font=("Segoe UI", 11),
    bd=0, command=show_chart
).pack(side=LEFT)

root.mainloop()
