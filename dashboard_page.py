from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6 import QtCore, QtGui
import sqlite3
import json

ruta_archivo = "data/config.json"


conn = sqlite3.connect("Kotoba.db")
cursor = conn.cursor()

cursor.execute("SELECT deck_id, name FROM Decks;")
decks = []
for deck in cursor.fetchall():
    decks.append((deck[0], deck[1]))


class DashboardPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget

        self.main_Vbox_layout = QVBoxLayout()
        self.decks_Vbox_layout = QVBoxLayout()

        self.top_container = QWidget()
        self.top_container_layout = QHBoxLayout()

        self.top_container.setLayout(self.top_container_layout)

        self.label_title = QLabel("Dashboard")

        self.label_title.setStyleSheet(
            """
    font-size: 28px;
    color: white;
    font-weight: bold;

"""
        )
        self.label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_title.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.label_streak = QLabel("Streak: 0")

        self.label_streak.setStyleSheet(
            """
    font-size: 20px;
    color: white;
    font-weight: bold;

"""
        )
        self.label_streak.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_streak.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.button_start_review = QPushButton("Start review")
        self.button_start_review.setStyleSheet(
            """
    QPushButton {
    background-color: green;
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-size: 16px;
    font-weight: bold;
    }
    QPushButton:hover {
    background-color: white;
    color: green;
    }
                                               
"""
        )

        self.button_start_review.clicked.connect(self.go_to_review_page)

        self.top_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.top_container.setStyleSheet(
            "background-color: #1d232a; border-radius: 10px;"
        )
        self.top_container_layout.addStretch(0)
        self.top_container_layout.addWidget(self.label_title)
        self.top_container_layout.addWidget(self.label_streak)

        for deck in decks:
            self.deck_button = QPushButton(deck[1])
            self.deck_button.clicked.connect(
                lambda _, deck_id=deck[0]: self.select_deck(deck_id)
            )
            self.deck_button.setStyleSheet(
                """
    QPushButton {
        background-color: #2b353f;
        border-radius: 10px;
        font-size: 24px;
        color: white;
    }
    QPushButton:hover {
        color: #2b353f;
        background-color: white;
    }
    """
            )
            self.decks_Vbox_layout.addWidget(self.deck_button)

        self.main_Vbox_layout.addWidget(self.top_container)
        self.main_Vbox_layout.addLayout(self.decks_Vbox_layout)
        self.main_Vbox_layout.addStretch()
        self.main_Vbox_layout.addWidget(self.button_start_review)

        self.setLayout(self.main_Vbox_layout)

    def go_to_review_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def select_deck(self, deck_id):
        print(deck_id)
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)  # Cargar los datos como un diccionario de Python

            datos["curr_deck"] = deck_id

            # Guardar los cambios de vuelta al archivo JSON
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
