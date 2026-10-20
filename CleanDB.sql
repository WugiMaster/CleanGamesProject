
CREATE TABLE "users" (
        "user_id" INTEGER PRIMARY KEY,
        "username" TEXT NOT NULL UNIQUE,
        "email" TEXT NOT NULL UNIQUE,
        "balance" REAL NOT NULL CHECK ("balance" >= 0)
    );

CREATE TABLE "developers" (
        "dev_id" INTEGER PRIMARY KEY,
        "name" TEXT NOT NULL,
        "country" TEXT
    );

CREATE TABLE "genres" (
        "genre_id" INTEGER PRIMARY KEY,
        "name" TEXT NOT NULL UNIQUE,
        "description" TEXT
    );

CREATE TABLE "games" (
        "game_id" INTEGER PRIMARY KEY,
        "dev_id" INTEGER NOT NULL,
        "genre_id" INTEGER NOT NULL,
        "title" TEXT NOT NULL,
        "price" REAL NOT NULL CHECK ("price" >= 0),
        FOREIGN KEY ("dev_id") REFERENCES "developers"("dev_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("genre_id") REFERENCES "genres"("genre_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

CREATE TABLE "orders" (
        "order_id" INTEGER PRIMARY KEY,
        "user_id" INTEGER NOT NULL,
        "total_price" REAL NOT NULL,
        FOREIGN KEY ("user_id") REFERENCES "users"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

CREATE TABLE "orderitems" (
        "item_id" INTEGER PRIMARY KEY,
        "order_id" INTEGER NOT NULL,
        "game_id" INTEGER NOT NULL,
        "price" REAL NOT NULL,
        FOREIGN KEY ("order_id") REFERENCES "orders"("order_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("game_id") REFERENCES "games"("game_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

CREATE TABLE "library" (
        "library_id" INTEGER PRIMARY KEY,
        "user_id" INTEGER NOT NULL,
        "game_id" INTEGER NOT NULL,
        UNIQUE ("user_id", "game_id"),
        FOREIGN KEY ("user_id") REFERENCES "users"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("game_id") REFERENCES "games"("game_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

CREATE TABLE "reviews" (
        "review_id" INTEGER PRIMARY KEY,
        "user_id" INTEGER NOT NULL,
        "game_id" INTEGER NOT NULL,
        "rating" INTEGER NOT NULL CHECK ("rating" BETWEEN 1 AND 5),
        FOREIGN KEY ("user_id") REFERENCES "users"("user_id") ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("game_id") REFERENCES "games"("game_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

CREATE TABLE "discounts" (
        "discount_id" INTEGER PRIMARY KEY,
        "game_id" INTEGER NOT NULL,
        "discount_percent" INTEGER NOT NULL CHECK ("discount_percent" BETWEEN 0 AND 100),
        "end_date" TEXT,
        FOREIGN KEY ("game_id") REFERENCES "games"("game_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );

CREATE TABLE "payments" (
        "payment_id" INTEGER PRIMARY KEY,
        "order_id" INTEGER NOT NULL,
        "amount" REAL NOT NULL,
        "payment_method" TEXT NOT NULL,
        FOREIGN KEY ("order_id") REFERENCES "orders"("order_id") ON UPDATE NO ACTION ON DELETE NO ACTION
    );
