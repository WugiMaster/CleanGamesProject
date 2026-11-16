<img width="1220" height="742" alt="Снимок экрана 2026-10-20 144937" src="https://github.com/user-attachments/assets/23b131b3-1ce1-4e27-ac2a-6fa1ca696e60" />


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
