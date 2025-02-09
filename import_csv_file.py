import csv
import sqlite3
from datetime import datetime

date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

conn = sqlite3.connect("cards.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Decks;")
cursor.execute("DROP TABLE IF EXISTS Cards;")
cursor.execute("DROP TABLE IF EXISTS CardReviews;")

cursor.execute(
    """
    CREATE TABLE Decks (
        deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        created_at DATETIME NOT NULL
    );
    """
)

cursor.execute(
    """
    CREATE TABLE Cards (
        card_id INTEGER PRIMARY KEY AUTOINCREMENT,
        deck_id INTEGER NOT NULL,
        front TEXT NOT NULL,
        reading TEXT,
        back TEXT NOT NULL,
        image_url TEXT,
        created_at DATETIME NOT NULL,
        FOREIGN KEY (deck_id) REFERENCES Decks(deck_id) ON DELETE CASCADE
    );
    """
)

cursor.execute(
    """
    CREATE TABLE CardReviews (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_id INTEGER NOT NULL,
        next_review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (card_id) REFERENCES Cards(card_id) ON DELETE CASCADE
    );
    """
)

csv_file_path = "Dareka no Manazashi.csv"

cursor.execute(
    "INSERT INTO Decks (name, description, created_at) VALUES (?, ?, ?)",
    (csv_file_path, "mami", date_now),
)

deck_id = cursor.lastrowid

with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        front, reading, back = row[0], row[1], row[2]

        img_url = row[3] if len(row) > 3 else ""

        cursor.execute(
            "INSERT INTO Cards (deck_id, front, reading, back, image_url, created_at) VALUES (?, ?, ?, ?, ?,?);",
            (deck_id, front, reading, back, img_url, date_now),
        )

        card_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO CardReviews (card_id, next_review_date) VALUES (?, ?);",
            (card_id, date_now),
        )

conn.commit()
conn.close()
