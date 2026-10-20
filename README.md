# Spēļu veikals — individuālā datubāze

## Projekta mērķis
Interneta spēļu veikala (Steam / Epic Games tipa) datubāze ar Python programmu.
Programma ļauj pievienot, skatīt, meklēt, labot un dzēst ierakstus visās 10 tabulās,
kā arī nopirkt spēli (vienā darījumā tiek izveidots pasūtījums, maksājums un ieraksts bibliotēkā).

## Datubāzes struktūra (SQLite, 10 tabulas)
`users`, `developers`, `genres`, `games`, `orders`, `orderitems`, `library`,
`reviews`, `discounts`, `payments`.

Galvenās saites:
- `games.dev_id` → `developers.dev_id`, `games.genre_id` → `genres.genre_id`
- `orders.user_id` → `users.user_id`
- `orderitems.order_id` → `orders.order_id`, `orderitems.game_id` → `games.game_id`
- `library` (pāris `user_id` + `game_id` ir unikāls), `reviews`, `discounts`, `payments` atsaucas uz `users`, `games`, `orders`

## Nepieciešamais
- Python 3.10+ (sqlite3 un tkinter ir iekļauti Python)
- Papildu pakotnes nav jāinstalē

## Datubāzes sagatavošana un palaišana
1. `python functions.py` — izveido `spelu_veikals.db`, tabulas un testa datus (var palaist atkārtoti, dati nedublējas)
2. `python app.py` — atver grafisko logu (ja datubāzes fails nav izveidots, `app.py` to izveido pats)

## Faili
| Fails | Apraksts |
|---|---|
| `functions.py` | datubāzes un tabulu izveide, testa dati |
| `main.py` | darbības ar datubāzi: pievienot, skatīt, labot, dzēst, meklēt, pirkt spēli |
| `app.py` | grafiskais interfeiss (tkinter) |
| `shema.sql` | tabulu struktūra (SQL) |

## Galvenās funkcijas
- Izvēlas tabulu no saraksta un redz visus ierakstus
- **Pievienot / Labot / Dzēst** ierakstu (ievadītie dati tiek pārbaudīti: tips, tukši lauki)
- **Meklēt** izvēlētajā kolonnā
- **Pirkt spēli** (`buy_game`): pārbauda bilanci un vai spēle jau ir bibliotēkā, piemēro atlaidi no `discounts`, izveido ierakstus `orders`, `orderitems`, `payments`, `library` un samazina bilanci
- **Pārskati** ar JOIN: spēles ar izstrādātāju un žanru, pasūtījumi ar lietotāju un spēli

Visi SQL vaicājumi izmanto parametrus (`?`), tabulu un kolonnu nosaukumi tiek pārbaudīti pēc saraksta `TABLES`.
Dati tiek saglabāti failā `spelu_veikals.db` un paliek pēc programmas restartēšanas.

## Zināmās problēmas
- Ierakstu, uz kuru atsaucas citas tabulas (piemēram, spēli, kas jau nopirkta), nevar izdzēst — `FOREIGN KEY` aizsardzība parāda kļūdas paziņojumu
- Maksājums ir simulēts (reāls maksājumu pakalpojums nav pieslēgts)
- Pasūtījumā ir tikai viena spēle (viens `orderitems` ieraksts)
