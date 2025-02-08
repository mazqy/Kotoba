from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QStackedWidget,
    QSizePolicy,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sqlite3
from datetime import datetime

conn = sqlite3.connect("cards.db")
cursor = conn.cursor()


class ReviewPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
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
        self.word_back.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.word_back.setFont(font_back)
        self.word_back.setWordWrap(True)

        self.show_answer_button = QPushButton("Show awnser")
        self.show_answer_button.setStyleSheet(
            """
            QPushButton{
            background-color: rgb(0, 150, 214);
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
            font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(0, 150, 214, 75%);
            }
        """
        )

        self.show_answer_button.clicked.connect(self.show_awnser)

        self.nothing_button = QPushButton("Nothing")
        self.nothing_button.setStyleSheet(
            """
            background-color: #f23030;
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
            font-size: 16px;
        """
        )

        self.hard_button = QPushButton("Hard")
        self.hard_button.setStyleSheet(
            """
            background-color: #f28e30;
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
            font-size: 16px;
        """
        )

        self.good_button = QPushButton("Good")
        self.good_button.setStyleSheet(
            """
            background-color: #6fd62a;
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
            font-size: 16px;
        """
        )

        self.easy_button = QPushButton("Easy")
        self.easy_button.setStyleSheet(
            """
            background-color: #30bef2;
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
            font-size: 16px;
        """
        )

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
        self.word_back_layout = QVBoxLayout()
        self.word_back_layout.setContentsMargins(0, 0, 0, 0)
        self.word_back_widget.setLayout(self.word_back_layout)
        self.word_back_layout.addWidget(self.word_back)
        self.word_back_widget.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
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
        self.buttons_and_show_awnser_stacked_widget = QStackedWidget()

        self.buttons_container_layout.addWidget(self.nothing_button)
        self.buttons_container_layout.addWidget(self.hard_button)
        self.buttons_container_layout.addWidget(self.good_button)
        self.buttons_container_layout.addWidget(self.easy_button)
        self.buttons_container_widget.setLayout(self.buttons_container_layout)
        self.buttons_container_layout.setContentsMargins(0, 0, 0, 0)

        self.buttons_and_show_awnser_stacked_widget.addWidget(self.show_answer_button)
        self.buttons_and_show_awnser_stacked_widget.addWidget(
            self.buttons_container_widget
        )
        self.buttons_and_show_awnser_stacked_widget.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )
        self.buttons_and_show_awnser_stacked_widget.setCurrentIndex(0)

        self.main_Vbox_Label.addWidget(self.word_container_widget)
        self.main_Vbox_Label.addWidget(self.word_back_widget)
        self.main_Vbox_Label.addWidget(self.buttons_and_show_awnser_stacked_widget)

        self.setLayout(self.main_Vbox_Label)

        self.load_card()

    def load_card(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            """
            SELECT front, reading, back
            FROM Cards
            WHERE date_next_review = (
                SELECT MIN(date_next_review)
                FROM Cards
                WHERE date_next_review < ?
            )
            """,
            (current_time,),
        )

        reader = cursor.fetchone()
        if reader:
            front, reading, back = reader
            self.word_text.setText(front)
            self.word_reading.setText(reading)
            self.word_back.setText(back)
        else:
            self.word_text.setText("No more cards due!")
            self.word_reading.setText("")
            self.word_back.setText("")

    def show_awnser(self):
        self.load_card()
        self.word_reading.setVisible(True)
        self.word_back.setVisible(True)
        self.buttons_and_show_awnser_stacked_widget.setCurrentIndex(1)

    def show_awnser(self):
        self.load_card()
        self.word_reading.setVisible(True)
        self.word_back.setVisible(True)
        self.buttons_and_show_awnser_stacked_widget.setCurrentIndex(1)

    def ranking_buttons(self, button):
        if button == self.easy_button:
            cursor.execute
