<img width="1157" height="713" alt="Screenshot 2026-10-16 110855" src="https://github.com/user-attachments/assets/df72e214-1579-4f52-96d1-9bae21cd6dc2" />

CleanGames ir interneta spēļu veikala datubāze (Steam / Epic Games tipa), ko veidoju ar Python un SQLite.
Programma ļauj pievienot lietotājus un spēles, nopirkt spēli, meklēt spēles, mainīt cenu, dzēst spēles un apskatīt pasūtījumus.

-- Kā palaist
Vajag tikai Python 3.

1. python main.py — izveido datubāzi un tabulas
2. python app.py — grafiskais logs

-- Datubāze (10 tabulas)
users, developers, genres, games, orders, orderitems, library, reviews, discounts, payments

-- Zināmās problēmas
Spēli, kas jau ir nopirkta, nevar izdzēst
Maksājums ir tikai imitācija
Atlaides un atsauksmes pagaidām netiek izmantotas programmā
