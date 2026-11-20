<img width="1220" height="742" alt="Снимок экрана 2026-10-20 144937" src="https://github.com/user-attachments/assets/23b131b3-1ce1-4e27-ac2a-6fa1ca696e60" />

# CleanGamesProject

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite" alt="SQLite" />
  <img src="https://img.shields.io/badge/Tkinter-GUI-00A86B?style=for-the-badge" alt="Tkinter" />
  <img src="https://img.shields.io/badge/ttkbootstrap-Modern-5E5CE6?style=for-the-badge" alt="ttkbootstrap" />
</p>

A lightweight game store management application built with Python, SQLite, and a Tkinter desktop interface. The project simulates a small digital storefront where users can manage games, developers, genres, orders, reviews, discounts, and purchases.

## About the Project

CleanGamesProject is a database-driven storefront app designed to model a simplified online game shop similar to Steam or Epic Games. It demonstrates how to combine relational database design with a graphical interface and business logic such as:

- user management
- game catalog administration
- buying and purchasing flow
- order tracking
- library management
- discounts and reviews
- basic search and filtering

This repository is a practical example of a clean, compact Python project with structured database logic and a GUI dashboard.

## Features

| Feature | Description |
| --- | --- |
| User management | Add, update, and view customers and their balances |
| Game catalog | Manage developers, genres, titles, and prices |
| Purchase flow | Buy games with a simulated payment method |
| Order history | Review orders, payments, and purchased items |
| Library tracking | See which games each user owns |
| Reviews | Add ratings for games |
| Discounts | Apply active discounts to game prices |
| Search | Filter records by table and field |
| GUI dashboard | Manage all data from a desktop app |

## Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python |
| Database | SQLite |
| GUI | Tkinter |
| Styling | ttkbootstrap |
| Schema definition | SQL script + Python initialization |

## Project Structure

```text
CleanGamesProject/
├── app.py                 # Desktop GUI application
├── main.py                # Database logic and CRUD operations
├── functions.py           # SQLite DB creation, seed data, and helper functions
├── CleanDB.sql            # Database schema definition
├── spelu_veikals.db       # SQLite database file generated at runtime
├── README.md              # Project documentation
└── __pycache__/           # Python cache files
```

## Database Schema

The app uses a relational SQLite database with these main tables:

| Table | Purpose |
| --- | --- |
| users | Store user profiles and balances |
| developers | Store game developer information |
| genres | Store genres such as RPG, Shooter, Sandbox |
| games | Main game catalog |
| orders | Store customer orders |
| orderitems | Items included in each order |
| library | Games owned by users |
| reviews | User ratings for games |
| discounts | Game discounts and expiration dates |
| payments | Payment records for orders |

## Requirements

Before running the project, make sure you have:

- Python 3.10 or newer
- `pip` installed

Install the required GUI dependency:

```bash
pip install ttkbootstrap
```

## Getting Started

### 1) Clone the repository

```bash
git clone https://github.com/WugiMaster/CleanGamesProject.git
cd CleanGamesProject
```

### 2) Initialize the database

You can create the SQLite database and insert sample data with:

```bash
python functions.py
```

This will generate `spelu_veikals.db` and populate it with example records.

### 3) Run the application

```bash
python app.py
```

The desktop app will open and you can interact with the game store interface.

## Usage

Once the app is running, you can:

- choose a table from the dropdown
- search records by field
- add a new record
- edit an existing record
- delete a selected row
- purchase a game through the checkout dialog
- view purchase and review summaries

### Example actions

| Action | Description |
| --- | --- |
| Add user | Create a user with username, email, and balance |
| Add game | Associate a game with a developer and genre |
| Buy game | Purchase a game using a payment method |
| Review | Add a rating for a title |
| Search | Filter rows in the active table |

## Key Logic

The project includes core logic for:

- SQLite connection management
- table validation
- data sanitization
- inserts, updates, deletions, and searches
- order processing and inventory ownership checks
- automatic price calculation with discounts

### Purchase flow

When a user buys a game, the system:

1. verifies the user and game exist
2. checks whether the user already owns the title
3. calculates the discounted price
4. validates the user balance
5. creates an order
6. creates an order item
7. records payment info
8. adds the game to the user library
9. reduces the user's balance

## Screenshots

The repo includes a desktop UI styled with ttkbootstrap. The interface allows users to browse records in a table layout and perform common store actions from a clean dashboard.

## Notes

Current project behavior includes:

- a simulated payment system rather than a real payment processor
- discount logic that is implemented but still simple
- some UI labels and strings in Latvian
- demo data seeded into the database for testing

## Roadmap

Possible future improvements:

- better validation and confirmation dialogs
- export/import of database data
- admin authentication
- more advanced discount rules
- sales analytics and charts
- improved UI polish and responsiveness

## Contributing

Contributions are welcome. If you want to improve the project:

1. fork the repository
2. create a feature branch
3. make your changes
4. run the app and validate the flow
5. submit a pull request

## License

This project does not currently include a license file. If you intend to publish or share it publicly, consider adding an appropriate open-source license such as MIT.

## Contact

For questions or collaboration, contact the project owner on GitHub:

- GitHub: [WugiMaster](https://github.com/WugiMaster)

---

<p align="center">
  <strong>Built with Python, SQLite, and a clean desktop storefront workflow.</strong>
</p>
