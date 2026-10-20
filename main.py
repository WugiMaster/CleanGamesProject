import sqlite3
from contextlib import closing

from functions import DATABASE_PATH

TABLES = {
    "users": ("user_id", [("username", "text"), ("email", "text"), ("balance", "float")]),
    "developers": ("dev_id", [("name", "text"), ("country", "text?")]),
    "genres": ("genre_id", [("name", "text"), ("description", "text?")]),
    "games": ("game_id", [("dev_id", "int"), ("genre_id", "int"), ("title", "text"), ("price", "float")]),
    "orders": ("order_id", [("user_id", "int"), ("total_price", "float")]),
    "orderitems": ("item_id", [("order_id", "int"), ("game_id", "int"), ("price", "float")]),
    "library": ("library_id", [("user_id", "int"), ("game_id", "int")]),
    "reviews": ("review_id", [("user_id", "int"), ("game_id", "int"), ("rating", "int")]),
    "discounts": ("discount_id", [("game_id", "int"), ("discount_percent", "int"), ("end_date", "text?")]),
    "payments": ("payment_id", [("order_id", "int"), ("amount", "float"), ("payment_method", "text")]),
}


def connect():
    database = sqlite3.connect(DATABASE_PATH)
    database.execute("PRAGMA foreign_keys = ON")
    return database


def check_table(table):
    if table not in TABLES:
        raise ValueError("Nezināma tabula: " + str(table))


def prepare_values(table, values):
    columns = TABLES[table][1]
    if len(values) != len(columns):
        raise ValueError("Nepareizs lauku skaits!")

    result = []
    for (column, kind), value in zip(columns, values):
        value = str(value).strip()
        if value == "" and kind == "text?":
            result.append(None)
        elif value == "":
            raise ValueError("Lauks '" + column + "' nedrīkst būt tukšs!")
        elif kind == "int":
            try:
                result.append(int(value))
            except ValueError:
                raise ValueError("Lauks '" + column + "' jābūt veselam skaitlim!")
        elif kind == "float":
            try:
                result.append(float(value.replace(",", ".")))
            except ValueError:
                raise ValueError("Lauks '" + column + "' jābūt skaitlim!")
        else:
            result.append(value)
    return result


def add_record(table, values):
    check_table(table)
    values = prepare_values(table, values)
    names = [column for column, kind in TABLES[table][1]]
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                f'INSERT INTO "{table}" ({", ".join(names)}) VALUES ({", ".join("?" * len(names))})',
                values,
            )
            return cursor.lastrowid


def get_records(table):
    check_table(table)
    key, columns = TABLES[table]
    names = [key] + [column for column, kind in columns]
    with closing(connect()) as database:
        return database.execute(f'SELECT {", ".join(names)} FROM "{table}" ORDER BY {key}').fetchall()


def update_record(table, values, record_id):
    check_table(table)
    values = prepare_values(table, values)
    key, columns = TABLES[table]
    assignments = ", ".join(f"{column} = ?" for column, kind in columns)
    with closing(connect()) as database:
        with database:
            cursor = database.execute(
                f'UPDATE "{table}" SET {assignments} WHERE {key} = ?',
                (*values, record_id),
            )
            return cursor.rowcount


def delete_record(table, record_id):
    check_table(table)
    key = TABLES[table][0]
    with closing(connect()) as database:
        with database:
            cursor = database.execute(f'DELETE FROM "{table}" WHERE {key} = ?', (record_id,))
            return cursor.rowcount


def search_records(table, column, text):
    check_table(table)
    key, columns = TABLES[table]
    names = [key] + [name for name, kind in columns]
    if column not in names:
        raise ValueError("Nezināma kolonna: " + str(column))
    with closing(connect()) as database:
        return database.execute(
            f'SELECT {", ".join(names)} FROM "{table}" WHERE {column} LIKE ? ORDER BY {key}',
            (f"%{text}%",),
        ).fetchall()


def get_games_overview():
    with closing(connect()) as database:
        return database.execute("""
            SELECT games.game_id, games.title, developers.name, genres.name, games.price
            FROM games
            JOIN developers ON games.dev_id = developers.dev_id
            JOIN genres ON games.genre_id = genres.genre_id
            ORDER BY games.game_id
        """).fetchall()


def get_orders_overview():
    with closing(connect()) as database:
        return database.execute("""
            SELECT orders.order_id, users.username, games.title, orderitems.price, payments.payment_method
            FROM orders
            JOIN users ON orders.user_id = users.user_id
            JOIN orderitems ON orderitems.order_id = orders.order_id
            JOIN games ON orderitems.game_id = games.game_id
            JOIN payments ON payments.order_id = orders.order_id
            ORDER BY orders.order_id
        """).fetchall()


def buy_game(user_id, game_id, method):
    with closing(connect()) as database:
        with database:
            user = database.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
            game = database.execute("SELECT price FROM games WHERE game_id = ?", (game_id,)).fetchone()
            if user is None or game is None:
                raise ValueError("Lietotājs vai spēle nav atrasta!")

            owned = database.execute(
                "SELECT 1 FROM library WHERE user_id = ? AND game_id = ?", (user_id, game_id)
            ).fetchone()
            if owned:
                raise ValueError("Šim lietotājam šī spēle jau ir!")

            percent = database.execute(
                "SELECT MAX(discount_percent) FROM discounts WHERE game_id = ? AND end_date >= date('now')",
                (game_id,),
            ).fetchone()[0] or 0
            price = round(game[0] * (100 - percent) / 100, 2)

            if user[0] < price:
                raise ValueError("Nepietiek līdzekļu! Vajag " + str(price))

            order_id = database.execute(
                "INSERT INTO orders (user_id, total_price) VALUES (?, ?)", (user_id, price)
            ).lastrowid
            database.execute("INSERT INTO orderitems (order_id, game_id, price) VALUES (?, ?, ?)", (order_id, game_id, price))
            database.execute("INSERT INTO payments (order_id, amount, payment_method) VALUES (?, ?, ?)", (order_id, price, method))
            database.execute("INSERT INTO library (user_id, game_id) VALUES (?, ?)", (user_id, game_id))
            database.execute("UPDATE users SET balance = ROUND(balance - ?, 2) WHERE user_id = ?", (price, user_id))
            return order_id, price
