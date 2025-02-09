from PyQt6.QtWidgets import QApplication, QStackedWidget
from PyQt6.QtGui import QIcon
from dashboard_page import DashboardPage
from review_page import ReviewPage

if __name__ == "__main__":

    app = QApplication([])

    stacked_widget = QStackedWidget()
    stacked_widget.setWindowTitle("Kotoba")
    stacked_widget.setWindowIcon(QIcon("data/icon.png"))
    stacked_widget.setStyleSheet("background-color: #3a4754; color: white;")
    dashboard_page = DashboardPage(stacked_widget)
    review_page = ReviewPage(stacked_widget)

    stacked_widget.addWidget(dashboard_page)
    stacked_widget.addWidget(review_page)

    stacked_widget.resize(800, 600)

    stacked_widget.setCurrentIndex(0)

    stacked_widget.show()

    app.exec()
