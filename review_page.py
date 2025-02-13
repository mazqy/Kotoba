from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QStackedWidget,
    QSizePolicy,
    QHBoxLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
import json

import sqlite3
from datetime import datetime


conn = sqlite3.connect("Kotoba.db")
cursor = conn.cursor()


# Ruta al archivo JSON
file_path = "data/config.json"

# Leer el archivo JSON y cargar los datos
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Acceder al valor de 'curr_deck'
curr_deck_value = data.get("curr_deck")

# Imprimir el valor


class ReviewPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.no_more_cards = False
        font_word = QFont("Arial", 32)
        font_reading = QFont("Arial", 18)
        font_back = QFont("Arial", 24)

        self.stacked_widget = stacked_widget

        self.word_reading = QLabel("Reading")
        self.word_reading.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.word_reading.setFont(font_reading)

        self.word_text = QLabel("Front")
        self.word_text.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.word_text.setFont(font_word)

        self.word_back = QLabel("Back")
        self.word_back.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.word_back.setFont(font_back)
        self.word_back.setWordWrap(True)

        def button_style(color1, color2):
            return f"""QPushButton {{
                        background-color: {color1};
                        color: {color2};
                        font-weight: bold;
                        padding: 10px;
                        border-radius: 10px;
                        font-size: 16px;
                        
                    }}
                    QPushButton:hover {{
                        background-color: {color2};
                        color: {color1};
                    }}
                """

        self.show_answer_button = QPushButton("Show answer")
        self.show_answer_button.setStyleSheet(
            button_style("#0096d6", "rgba(255, 255, 255, 100%)")
        )

        self.show_answer_button.clicked.connect(self.show_answer)

        self.nothing_button = QPushButton("Nothing")
        self.nothing_button.setStyleSheet(
            button_style("#f23030", "rgba(255, 255, 255, 100%)")
        )

        self.hard_button = QPushButton("Hard")
        self.hard_button.setStyleSheet(
            button_style("#f28e30", "rgba(255, 255, 255, 100%)")
        )

        self.good_button = QPushButton("Good")
        self.good_button.setStyleSheet(
            button_style("#6fd62a", "rgba(255, 255, 255, 100%)")
        )

        self.easy_button = QPushButton("Easy")
        self.easy_button.setStyleSheet(
            button_style("#30bef2", "rgba(255, 255, 255, 100%)")
        )

        self.easy_button.clicked.connect(lambda: self.ranking_buttons("2 days"))
        self.good_button.clicked.connect(lambda: self.ranking_buttons("1 day"))
        self.hard_button.clicked.connect(lambda: self.ranking_buttons("10 minutes"))
        self.nothing_button.clicked.connect(lambda: self.ranking_buttons("1 minute"))

        self.word_container_widget = QWidget()
        self.word_container_widget.setStyleSheet(
            """
            background-color: #1d232a;
            color: white;
            border-radius: 10px;
        """
        )

        self.word_reading.setVisible(False)
        self.word_back.setVisible(False)

        self.word_container_layout = QVBoxLayout()
        self.word_back_widget = QWidget()
        self.word_back_widget.setStyleSheet(
            "background-color: #2b353f; border-radius: 10px;"
        )
        self.image_label = QLabel()
        self.word_back_layout = QVBoxLayout()
        self.word_back_layout.setContentsMargins(20, 20, 20, 20)
        self.word_back_widget.setLayout(self.word_back_layout)
        self.word_back_layout.addWidget(self.word_back)
        self.word_back_layout.addWidget(self.image_label)
        self.word_back_widget.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )

        self.word_back_widget.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.word_back_widget)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setStyleSheet(
            """
    QScrollArea {
    border: none;
}

    QScrollBar:vertical {
    border: 2px #3a4754; 
    background: #3a4754;
    width: 12px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #1d232a;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: white;
}

QScrollBar::sub-line, QScrollBar::add-line {
    background: #ddd;
    height: 10px;
}

QScrollBar::sub-line:hover, QScrollBar::add-line:hover {
    background: #bbb;
}

QScrollBar::add-page, QScrollBar::sub-page {
    background: none;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
    }

"""
        )

        self.word_container_widget.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )

        self.word_container_layout.addWidget(self.word_reading)
        self.word_container_layout.addWidget(self.word_text)

        self.word_container_widget.setLayout(self.word_container_layout)

        self.main_Vbox_Label = QVBoxLayout()
        self.buttons_container_widget = QWidget()
        self.buttons_container_layout = QHBoxLayout()
        self.buttons_and_show_answer_stacked_widget = QStackedWidget()

        self.buttons_container_layout.addWidget(self.nothing_button)
        self.buttons_container_layout.addWidget(self.hard_button)
        self.buttons_container_layout.addWidget(self.good_button)
        self.buttons_container_layout.addWidget(self.easy_button)
        self.buttons_container_widget.setLayout(self.buttons_container_layout)
        self.buttons_container_layout.setContentsMargins(0, 0, 0, 0)

        self.buttons_and_show_answer_stacked_widget.addWidget(self.show_answer_button)
        self.buttons_and_show_answer_stacked_widget.addWidget(
            self.buttons_container_widget
        )
        self.buttons_and_show_answer_stacked_widget.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )
        self.buttons_and_show_answer_stacked_widget.setCurrentIndex(0)

        self.main_Vbox_Label.addWidget(self.word_container_widget)
        self.main_Vbox_Label.addWidget(self.scroll_area)

        self.main_Vbox_Label.addWidget(self.buttons_and_show_answer_stacked_widget)

        self.setLayout(self.main_Vbox_Label)

        self.load_card(False)

    def load_card(self, is_in_back):
        self.word_reading.setVisible(False)
        self.word_back.setVisible(False)
        self.buttons_and_show_answer_stacked_widget.setCurrentIndex(0)
        cursor.execute(
            """
            SELECT c.card_id, c.front, c.reading, c.back, c.image_url
            FROM Cards AS c
            JOIN Decks AS d ON c.deck_id = d.deck_id
            WHERE d.deck_id = ?
            AND c.next_review_date < ?
            LIMIT 1;
            """,
            (curr_deck_value, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        reader = cursor.fetchone()
        if reader:
            self.current_card_id, front, reading, back, image_url = reader
            self.word_text.setText(front)
            self.word_reading.setText(reading)
            self.word_back.setText(back)
            if is_in_back:
                pixmap = QPixmap("data/img/" + image_url)
                self.image_label.setPixmap(
                    pixmap.scaledToHeight(
                        300, Qt.TransformationMode.SmoothTransformation
                    )
                )
                self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            else:
                self.image_label.setPixmap(QPixmap())
        else:
            self.no_more_cards = True
            self.word_text.setText("No more cards due!")
            self.word_reading.setText("")
            self.word_back.setText("")

    def show_answer(self):
        if self.no_more_cards == False:
            self.load_card(True)
            self.word_reading.setVisible(True)
            self.word_back.setVisible(True)
            self.buttons_and_show_answer_stacked_widget.setCurrentIndex(1)

    def ranking_buttons(self, time):
        cursor.execute(
            """
            UPDATE Cards
            SET next_review_date = DATETIME(?, ?)
            WHERE card_id = ?;
            """,
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                f"+{time}",
                self.current_card_id,
            ),
        )
        conn.commit()
        self.load_card(False)
