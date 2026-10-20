import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).with_name("spelu_veikals.db")


def izveidot_datubazi():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS "users" (
        "user_id" INTEGER PRIMARY KEY,
        "username" TEXT NOT NULL UNIQUE,
        "email" TEXT NOT NULL UNIQUE,
        "balance" REAL NOT NULL CHECK ("balance" >= 0)
    );

    CREATE TABLE IF NOT EXISTS "developers" (
        "dev_id" INTEGER PRIMARY KEY,
        "name" TEXT NOT NULL,
        "country" TEXT
    );

    CREATE TABLE IF NOT EXISTS "genres" (
        "genre_id" INTEGER PRIMARY KEY,
        "name" TEXT NOT NULL UNIQUE,
        "description" TEXT
    );

    CREATE TABLE IF NOT EXISTS "games" (
        "game_id" INTEGER PRIMARY KEY,
        "dev_id" INTEGER NOT NULL,
        "genre_id" INTEGER NOT NULL,
        "title" TEXT NOT NULL,
        "price" REAL NOT NULL CHECK ("price" >= 0),
        FOREIGN KEY ("dev_id") REFERENCES "developers"("dev_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("genre_id") REFERENCES "genres"("genre_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "orders" (
        "order_id" INTEGER PRIMARY KEY,
        "user_id" INTEGER NOT NULL,
        "total_price" REAL NOT NULL,
        FOREIGN KEY ("user_id") REFERENCES "users"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "orderitems" (
        "item_id" INTEGER PRIMARY KEY,
        "order_id" INTEGER NOT NULL,
        "game_id" INTEGER NOT NULL,
        "price" REAL NOT NULL,
        FOREIGN KEY ("order_id") REFERENCES "orders"("order_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("game_id") REFERENCES "games"("game_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "library" (
        "library_id" INTEGER PRIMARY KEY,
        "user_id" INTEGER NOT NULL,
        "game_id" INTEGER NOT NULL,
        UNIQUE ("user_id", "game_id"),
        FOREIGN KEY ("user_id") REFERENCES "users"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("game_id") REFERENCES "games"("game_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "reviews" (
        "review_id" INTEGER PRIMARY KEY,
        "user_id" INTEGER NOT NULL,
        "game_id" INTEGER NOT NULL,
        "rating" INTEGER NOT NULL CHECK ("rating" BETWEEN 1 AND 5),
        FOREIGN KEY ("user_id") REFERENCES "users"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("game_id") REFERENCES "games"("game_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "discounts" (
        "discount_id" INTEGER PRIMARY KEY,
        "game_id" INTEGER NOT NULL,
        "discount_percent" INTEGER NOT NULL CHECK ("discount_percent" BETWEEN 0 AND 100),
        "end_date" TEXT,
        FOREIGN KEY ("game_id") REFERENCES "games"("game_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "payments" (
        "payment_id" INTEGER PRIMARY KEY,
        "order_id" INTEGER NOT NULL,
        "amount" REAL NOT NULL,
        "payment_method" TEXT NOT NULL,
        FOREIGN KEY ("order_id") REFERENCES "orders"("order_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );
    ''')

    cursor.executescript('''
    INSERT OR IGNORE INTO "users" (user_id, username, email, balance) VALUES
        (1, 'Kirills', 'kirills@mail.com', 100.00),
        (2, 'Aleksandrs', 'aleksandrs@mail.com', 25.01),
        (3, 'Tamir', 'tamir@mail.com', 75.50);

    INSERT OR IGNORE INTO "developers" (dev_id, name, country) VALUES
        (1, 'CD Projekt Red', 'Polija'),
        (2, 'Valve', 'ASV'),
        (3, 'Mojang', 'Zviedrija');

    INSERT OR IGNORE INTO "genres" (genre_id, name, description) VALUES
        (1, 'RPG', 'Lomu spēles'),
        (2, 'Shooter', 'Šaušanas spēles'),
        (3, 'Sandbox', 'Atklātas pasaules spēles');

    INSERT OR IGNORE INTO "games" (game_id, dev_id, genre_id, title, price) VALUES
        (1, 1, 1, 'The Witcher 3', 29.99),
        (2, 2, 2, 'Counter-Strike 2', 14.99),
        (3, 3, 3, 'Minecraft', 24.99);

    INSERT OR IGNORE INTO "orders" (order_id, user_id, total_price) VALUES
        (1, 2, 24.99);

    INSERT OR IGNORE INTO "orderitems" (item_id, order_id, game_id, price) VALUES
        (1, 1, 3, 24.99);

    INSERT OR IGNORE INTO "library" (library_id, user_id, game_id) VALUES
        (1, 2, 3);

    INSERT OR IGNORE INTO "reviews" (review_id, user_id, game_id, rating) VALUES
        (1, 2, 3, 5);

    INSERT OR IGNORE INTO "discounts" (discount_id, game_id, discount_percent, end_date) VALUES
        (1, 1, 50, '2030-12-31');

    INSERT OR IGNORE INTO "payments" (payment_id, order_id, amount, payment_method) VALUES
        (1, 1, 24.99, 'card');
    ''')

    conn.commit()
    conn.close()
    print("Datu bāze un tabulas veiksmīgi izveidotas!")


if __name__ == '__main__':
    izveidot_datubazi()
