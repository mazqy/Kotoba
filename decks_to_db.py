import csv
import sqlite3
from datetime import datetime

conn = sqlite3.connect("cards.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Cards;")

cursor.execute(
    """
CREATE TABLE Cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    front TEXT NOT NULL,
    reading TEXT NOT NULL,
    back TEXT NOT NULL,
    date_next_review DATETIME,
    card_type TEXT DEFAULT 'new',
    card_level TEXT DEFAULT 'level 0'
);
"""
)

csv_file_path = "Dareka no Manazashi.csv"

with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)

    next(reader, None)

    for row in reader:
        front = row[0]
        reading = row[1]
        back = row[2]
        date_next_review = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO Cards (front, reading, back, date_next_review) VALUES (?, ?, ?, ?);",
            (front, reading, back, date_next_review),
        )

conn.commit()
conn.close()
