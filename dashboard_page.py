from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6 import QtCore, QtGui


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

        self.label_title.setStyleSheet("""
    font-size: 28px;
    color: white;
    font-weight: bold;

""")
        self.label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.label_streak = QLabel("Streak: 0")

        self.label_streak.setStyleSheet("""
    font-size: 20px;
    color: white;
    font-weight: bold;

""")
        self.label_streak.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_streak.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        
        
        self.button_start_review = QPushButton("Start review")
        self.button_start_review.setStyleSheet("""
    background-color: green;
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-size: 16px;
                                               
""")

        self.button_start_review.clicked.connect(self.go_to_review_page)
        
        self.top_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.top_container_layout.addStretch(0)
        self.top_container_layout.addWidget(self.label_title)
        self.top_container_layout.addWidget(self.label_streak)


        self.decks_Vbox_layout.addWidget(QLabel("Deck 1"))
        self.decks_Vbox_layout.addWidget(QLabel("deck 2"))
        self.decks_Vbox_layout.addWidget(QLabel("Deck 3"))

        self.main_Vbox_layout.addWidget(self.top_container)
        self.main_Vbox_layout.addLayout(self.decks_Vbox_layout)
        self.main_Vbox_layout.addWidget(self.button_start_review)
        
        
        self.setLayout(self.main_Vbox_layout)

    def go_to_review_page(self):
        self.stacked_widget.setCurrentIndex(1)