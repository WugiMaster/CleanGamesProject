import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import main as db
from functions import DATABASE_PATH, izveidot_datubazi

if not DATABASE_PATH.exists():
    izveidot_datubazi()

OVERVIEWS = {
    "Spēles (ar nosaukumiem)": (db.get_games_overview, ["game_id", "title", "developer", "genre", "price"]),
    "Pasūtījumi": (db.get_orders_overview, ["order_id", "username", "title", "price", "payment_method"]),
}

overview_mode = False


def show_rows(rows, columns):
    tree.delete(*tree.get_children())
    tree["columns"] = columns
    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=130)
    for row in rows:
        tree.insert("", "end", values=["" if value is None else value for value in row])


def table_columns(table):
    return [db.TABLES[table][0]] + [column for column, kind in db.TABLES[table][1]]


def load_table(event=None):
    global overview_mode
    overview_mode = False
    table = table_var.get()
    columns = table_columns(table)
    search_field_box["values"] = columns
    search_field_var.set(columns[1])
    show_rows(db.get_records(table), columns)


def show_overview(name):
    global overview_mode
    function, columns = OVERVIEWS[name]
    show_rows(function(), columns)
    overview_mode = True


def search():
    text = search_entry.get().strip()
    if not text or overview_mode:
        load_table()
        return
    table = table_var.get()
    try:
        show_rows(db.search_records(table, search_field_var.get(), text), table_columns(table))
    except ValueError as error:
        messagebox.showerror("Kļūda", str(error))


def selected_id():
    selection = tree.selection()
    if overview_mode or not selection:
        messagebox.showinfo("Nav izvēlēts", "Izvēlies ierakstu no tabulas (nevis no pārskata).")
        return None
    return int(tree.item(selection[0], "values")[0])


def ask_for_values(title, table, current_values=None):
    values = []
    for i, (column, kind) in enumerate(db.TABLES[table][1]):
        start = current_values[i] if current_values else ""
        answer = simpledialog.askstring(title, column, initialvalue=start, parent=root)
        if answer is None:
            return None
        values.append(answer)
    return values


def run(action, *args):
    try:
        return action(*args)
    except sqlite3.IntegrityError as error:
        messagebox.showerror("Datubāzes kļūda", "Nevar saglabāt/dzēst: ieraksts ir saistīts ar citām tabulām vai atkārtojas.\n" + str(error))
    except (sqlite3.Error, ValueError) as error:
        messagebox.showerror("Kļūda", str(error))


def add_record():
    table = table_var.get()
    values = ask_for_values("Pievienot: " + table, table)
    if values is not None:
        run(db.add_record, table, values)
        load_table()


def edit_record():
    record_id = selected_id()
    if record_id is None:
        return
    table = table_var.get()
    current_values = tree.item(tree.selection()[0], "values")[1:]
    values = ask_for_values(f"Labot ierakstu {record_id}", table, current_values)
    if values is not None:
        run(db.update_record, table, values, record_id)
        load_table()


def delete_record():
    record_id = selected_id()
    if record_id is None:
        return
    if messagebox.askyesno("Apstiprināt", f"Dzēst ierakstu {record_id}?"):
        run(db.delete_record, table_var.get(), record_id)
        load_table()


def buy_game():
    user_id = simpledialog.askinteger("Pirkt spēli", "Lietotāja ID:", parent=root)
    if user_id is None:
        return
    game_id = simpledialog.askinteger("Pirkt spēli", "Spēles ID:", parent=root)
    if game_id is None:
        return
    method = simpledialog.askstring("Pirkt spēli", "Maksājuma veids:", initialvalue="card", parent=root)
    if not method:
        return
    result = run(db.buy_game, user_id, game_id, method.strip())
    if result:
        messagebox.showinfo("Pirkums veiksmīgs", f"Pasūtījums {result[0]}, cena: {result[1]}")
        show_overview("Pasūtījumi")


root = tk.Tk()
root.title("Spēļu veikals")

top = ttk.Frame(root, padding=8)
top.pack(fill="x")

table_var = tk.StringVar(value="users")
table_box = ttk.Combobox(top, textvariable=table_var, values=list(db.TABLES), state="readonly")
table_box.bind("<<ComboboxSelected>>", load_table)
table_box.pack(side="left")

ttk.Label(top, text="Meklēt kolonnā").pack(side="left", padx=(16, 4))
search_field_var = tk.StringVar()
search_field_box = ttk.Combobox(top, textvariable=search_field_var, state="readonly", width=16)
search_field_box.pack(side="left")
search_entry = ttk.Entry(top, width=16)
search_entry.pack(side="left", padx=4)
ttk.Button(top, text="Meklēt", command=search).pack(side="left")

tree_frame = ttk.Frame(root)
tree_frame.pack(fill="both", expand=True, padx=8)
tree = ttk.Treeview(tree_frame, show="headings", selectmode="browse")
scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
tree.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

buttons = ttk.Frame(root, padding=8)
buttons.pack(fill="x")
ttk.Button(buttons, text="Pievienot", command=add_record).pack(side="left", padx=(0, 8))
ttk.Button(buttons, text="Labot izvēlēto", command=edit_record).pack(side="left", padx=(0, 8))
ttk.Button(buttons, text="Dzēst izvēlēto", command=delete_record).pack(side="left", padx=(0, 24))
ttk.Button(buttons, text="Pirkt spēli", command=buy_game).pack(side="left", padx=(0, 8))
for name in OVERVIEWS:
    ttk.Button(buttons, text=name, command=lambda n=name: show_overview(n)).pack(side="left", padx=(0, 8))

load_table()
root.mainloop()
