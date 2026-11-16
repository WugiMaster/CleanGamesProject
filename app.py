import sqlite3
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import main as db
from functions import DATABASE_PATH, izveidot_datubazi

if not DATABASE_PATH.exists():
    izveidot_datubazi()

OVERVIEWS = {
    "Spēles (ar nosaukumiem)": (db.get_games_overview, ["game_id", "title", "developer", "genre", "price"]),
    "Pasūtījumi": (db.get_orders_overview, ["order_id", "username", "title", "price", "payment_method"]),
    "Pasūtījuma preces": (db.get_orderitems_overview, ["item_id", "title", "price"]),
    "Bibliotēka": (db.get_orders_overview, ["library_id", "username", "title"]),\
    "Recenzija": (db.get_reviews_overview, ["review_id", "username", "title", "rating"]),
}

overview_mode = False


class FormDialog(ttk.Toplevel):
    def __init__(self, parent, title, fields, initial_values=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.result = None
        self.entries = []

        container = ttk.Frame(self, padding=20)
        container.pack(fill=BOTH, expand=True)

        for i, field in enumerate(fields):
            ttk.Label(container, text=field.capitalize(), font=("Segoe UI", 10, "bold")).grid(
                row=i, column=0, sticky=W, pady=(0, 8), padx=(0, 15)
            )
            entry = ttk.Entry(container, width=30)
            if initial_values and i < len(initial_values):
                entry.insert(0, str(initial_values[i]))
            entry.grid(row=i, column=1, pady=(0, 8))
            self.entries.append(entry)

        if self.entries:
            self.entries[0].focus_set()

        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=(15, 0), sticky=E)

        ttk.Button(btn_frame, text="Atcelt", bootstyle=SECONDARY, command=self.destroy).pack(side=LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Saglabāt", bootstyle=SUCCESS, command=self.on_save).pack(side=LEFT)

        self.bind("<Return>", lambda e: self.on_save())
        self.bind("<Escape>", lambda e: self.destroy())

        self.transient(parent)
        self.grab_set()
        self.wait_window()

    def on_save(self):
        self.result = [entry.get() for entry in self.entries]
        self.destroy()


def show_rows(rows, columns):
    tree.delete(*tree.get_children())
    tree["columns"] = columns
    for column in columns:
        tree.heading(column, text=column.upper(), anchor=W)
        tree.column(column, width=140, anchor=W)

    for i, row in enumerate(rows):
        tag = "even" if i % 2 == 0 else "odd"
        clean_row = ["" if value is None else value for value in row]
        tree.insert("", END, values=clean_row, tags=(tag,))


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


def search(event=None):
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


def run(action, *args):
    try:
        return action(*args)
    except sqlite3.IntegrityError as error:
        messagebox.showerror(
            "Datubāzes kļūda",
            "Nevar saglabāt/dzēst: ieraksts ir saistīts ar citām tabulām vai atkārtojas.\n" + str(error),
        )
    except (sqlite3.Error, ValueError) as error:
        messagebox.showerror("Kļūda", str(error))


def add_record():
    table = table_var.get()
    fields = [col for col, _ in db.TABLES[table][1]]
    dialog = FormDialog(root, f"Pievienot: {table}", fields)
    if dialog.result is not None:
        run(db.add_record, table, dialog.result)
        load_table()


def edit_record():
    record_id = selected_id()
    if record_id is None:
        return
    table = table_var.get()
    fields = [col for col, _ in db.TABLES[table][1]]
    current_values = tree.item(tree.selection()[0], "values")[1:]
    dialog = FormDialog(root, f"Labot ierakstu #{record_id}", fields, current_values)
    if dialog.result is not None:
        run(db.update_record, table, dialog.result, record_id)
        load_table()


def delete_record():
    record_id = selected_id()
    if record_id is None:
        return
    if messagebox.askyesno("Apstiprināt", f"Vai tiešām dzēst ierakstu #{record_id}?"):
        run(db.delete_record, table_var.get(), record_id)
        load_table()


def buy_game():
    dialog = FormDialog(root, "Pirkt spēli", ["Lietotāja ID", "Spēles ID", "Maksājuma veids"], ["", "", "card"])
    if dialog.result is None:
        return
    try:
        user_id = int(dialog.result[0])
        game_id = int(dialog.result[1])
        method = dialog.result[2].strip()
    except ValueError:
        messagebox.showerror("Kļūda", "ID laukiem jābūt skaitļiem.")
        return

    if not method:
        return
    result = run(db.buy_game, user_id, game_id, method)
    if result:
        messagebox.showinfo("Pirkums veiksmīgs", f"Pasūtījums #{result[0]}, cena: {result[1]}")
        show_overview("Pasūtījumi")


root = ttk.Window(themename="superhero")
root.title("Spēļu veikals")
root.geometry("1150x550")

style = ttk.Style()
style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

top = ttk.Frame(root, padding=15)
top.pack(fill=X)

ttk.Label(top, text="Tabula:", font=("Segoe UI", 10, "bold")).pack(side=LEFT, padx=(0, 6))
table_var = tk.StringVar(value="users")
table_box = ttk.Combobox(top, textvariable=table_var, values=list(db.TABLES), state="readonly", width=16)
table_box.bind("<<ComboboxSelected>>", load_table)
table_box.pack(side=LEFT)

ttk.Label(top, text="Meklēt:", font=("Segoe UI", 10, "bold")).pack(side=LEFT, padx=(24, 6))
search_field_var = tk.StringVar()
search_field_box = ttk.Combobox(top, textvariable=search_field_var, state="readonly", width=15)
search_field_box.pack(side=LEFT)

search_entry = ttk.Entry(top, width=20)
search_entry.pack(side=LEFT, padx=6)
search_entry.bind("<Return>", search)

ttk.Button(top, text="Meklēt", bootstyle=INFO, command=search).pack(side=LEFT, padx=(0, 4))
ttk.Button(
    top,
    text="Notīrīt",
    bootstyle=(SECONDARY, OUTLINE),
    command=lambda: [search_entry.delete(0, END), load_table()],
).pack(side=LEFT)

tree_frame = ttk.Frame(root, padding=(15, 0))
tree_frame.pack(fill=BOTH, expand=True)

tree = ttk.Treeview(tree_frame, show="headings", selectmode="browse", bootstyle=PRIMARY)
scroll = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scroll.set)

tree.tag_configure("odd", background="#2b3e50")
tree.tag_configure("even", background="#32465a")

tree.pack(side=LEFT, fill=BOTH, expand=True)
scroll.pack(side=RIGHT, fill=Y)

tree.bind("<Double-1>", lambda e: edit_record())

buttons = ttk.Frame(root, padding=15)
buttons.pack(fill=X)

ttk.Button(buttons, text="+ Pievienot", bootstyle=SUCCESS, command=add_record).pack(side=LEFT, padx=(0, 8))
ttk.Button(buttons, text="Labot", bootstyle=WARNING, command=edit_record).pack(side=LEFT, padx=(0, 8))
ttk.Button(buttons, text="Dzēst", bootstyle=DANGER, command=delete_record).pack(side=LEFT, padx=(0, 24))

ttk.Button(buttons, text="🛒 Pirkt spēli", bootstyle=PRIMARY, command=buy_game).pack(side=LEFT, padx=(0, 24))

for name in OVERVIEWS:
    ttk.Button(
        buttons,
        text=name,
        bootstyle=(INFO, OUTLINE),
        command=lambda n=name: show_overview(n),
    ).pack(side=LEFT, padx=(0, 8))

load_table()
root.mainloop()
