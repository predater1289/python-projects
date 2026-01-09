import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, ttk, messagebox

df = None
file_type = None

# ---------------- FILE LOAD ---------------- #
def load_file():
    global df, file_type
    path = filedialog.askopenfilename(
        filetypes=[
            ("Excel Files", "*.xlsx *.xls"),
            ("CSV Files", "*.csv")
        ]
    )
    if not path:
        return

    if path.endswith(".csv"):
        df = pd.read_csv(path)
        file_type = "csv"
    else:
        df = pd.read_excel(path)
        file_type = "excel"

    update_table()
    update_kpi()

# ---------------- SAVE DATA ---------------- #
def save_file():
    if df is None:
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[
            ("Excel File", "*.xlsx"),
            ("CSV File", "*.csv")
        ]
    )
    if not path:
        return

    if path.endswith(".csv"):
        df.to_csv(path, index=False)
    else:
        df.to_excel(path, index=False)

    messagebox.showinfo("Saved", "File saved successfully")

# ---------------- TABLE ---------------- #
def update_table():
    tree.delete(*tree.get_children())
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor=CENTER)

    for i, row in df.iterrows():
        tree.insert("", END, iid=i, values=list(row))

def on_double_click(event):
    item = tree.selection()[0]
    column = tree.identify_column(event.x)
    col_index = int(column.replace("#", "")) - 1

    x, y, w, h = tree.bbox(item, column)
    value = tree.item(item, "values")[col_index]

    entry = Entry(tree)
    entry.place(x=x, y=y, width=w, height=h)
    entry.insert(0, value)
    entry.focus()

    def save_edit(event):
        df.iat[int(item), col_index] = entry.get()
        update_table()
        entry.destroy()

    entry.bind("<Return>", save_edit)

# ---------------- KPI ---------------- #
def update_kpi():
    rows_var.set(str(df.shape[0]))
    cols_var.set(str(df.shape[1]))
    num_var.set(str(df.select_dtypes(include='number').shape[1]))

# ---------------- CHART ---------------- #
def show_chart():
    if df is None:
        return

    chart = chart_type.get()
    num_df = df.select_dtypes(include='number')

    if num_df.empty:
        messagebox.showerror("Error", "No numeric data")
        return

    plt.close("all")

    if chart == "Bar":
        num_df.plot(kind="bar", figsize=(8,5))
    elif chart == "Line":
        num_df.plot(kind="line", figsize=(8,5))
    elif chart == "Pie":
        num_df.iloc[0].plot(kind="pie", autopct="%1.1f%%", figsize=(6,6))
    elif chart == "Histogram":
        num_df.plot(kind="hist", figsize=(8,5))
    elif chart == "Scatter":
        if num_df.shape[1] >= 2:
            plt.figure(figsize=(8,5))
            plt.scatter(num_df.iloc[:,0], num_df.iloc[:,1])
        else:
            return
    elif chart == "Area":
        num_df.plot(kind="area", figsize=(8,5))
    elif chart == "Box":
        num_df.plot(kind="box", figsize=(8,5))

    plt.title(chart)
    plt.tight_layout()
    plt.show()

def save_chart():
    plt.savefig("dashboard_chart.png")
    messagebox.showinfo("Saved", "Dashboard saved as image")

# ---------------- UI ---------------- #
root = Tk()
root.title("ExcelInsight AI Dashboard")
root.geometry("1300x720")
root.configure(bg="#f1f5f9")

header = Frame(root, bg="#0f172a", height=60)
header.pack(fill=X)
Label(header, text="ExcelInsight AI",
      fg="white", bg="#0f172a",
      font=("Segoe UI", 20, "bold")).pack(padx=20, anchor=W)

kpi = Frame(root, bg="#f1f5f9")
kpi.pack(fill=X, padx=20, pady=10)

rows_var = StringVar(value="0")
cols_var = StringVar(value="0")
num_var = StringVar(value="0")

for t, v in [("Rows", rows_var), ("Columns", cols_var), ("Numeric", num_var)]:
    f = Frame(kpi, bg="white", width=200, height=80)
    f.pack(side=LEFT, padx=10)
    Label(f, text=t, bg="white").pack(anchor=W, padx=10)
    Label(f, textvariable=v, bg="white",
          font=("Segoe UI", 18, "bold")).pack(anchor=W, padx=10)

main = Frame(root, bg="#f1f5f9")
main.pack(fill=BOTH, expand=True)

sidebar = Frame(main, bg="#1e293b", width=200)
sidebar.pack(side=LEFT, fill=Y)

Button(sidebar, text="📂 Load Excel / CSV", command=load_file,
       bg="#2563eb", fg="white", bd=0).pack(padx=15, pady=20, fill=X)

Button(sidebar, text="💾 Save Data", command=save_file,
       bg="#10b981", fg="white", bd=0).pack(padx=15, pady=10, fill=X)

content = Frame(main, bg="white")
content.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

tree = ttk.Treeview(content)
tree.pack(fill=BOTH, expand=True)
tree.bind("<Double-1>", on_double_click)

control = Frame(root, bg="#f1f5f9")
control.pack(fill=X, padx=20, pady=10)

chart_type = StringVar(value="Bar")
ttk.Combobox(
    control, textvariable=chart_type,
    values=["Bar", "Line", "Pie", "Histogram", "Scatter", "Area", "Box"],
    state="readonly", width=15
).pack(side=LEFT, padx=10)

Button(control, text="📊 Show Dashboard", command=show_chart,
       bg="#16a34a", fg="white", bd=0).pack(side=LEFT)

Button(control, text="💾 Save Dashboard", command=save_chart,
       bg="#0ea5e9", fg="white", bd=0).pack(side=LEFT, padx=10)

root.mainloop()

