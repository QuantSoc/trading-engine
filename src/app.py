import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QCompleter
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stock Ticker Selector")
        self.setGeometry(100, 100, 960, 580)

        self.ticker_list = []  # List to store selected tickers

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Add padding to the layout (margins)
        main_layout.setContentsMargins(20, 20, 20, 20)  # Left, Top, Right, Bottom
        main_layout.setSpacing(10)  # Set the space between widgets in the layout

        # Search bar (QLineEdit)
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search Tickers...")
        self.search_bar.setMaximumWidth(300)  # You can adjust the width here

        # Add an icon action to the left side of QLineEdit
        search_icon = QIcon("src/assets/search-icon.svg")
        self.search_bar.addAction(search_icon, QLineEdit.LeadingPosition)

        # Add the search bar to the top of the layout
        main_layout.addWidget(self.search_bar, alignment=Qt.AlignTop)

        # Load stock data and set up the completer
        self.load_stock_data()

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

    def load_stock_data(self):
        """Load stock data from a JSON file and set up the completer."""
        try:
            with open("src/stocks.json", "r") as file:
                data = json.load(file)

            # Extract tickers and set up completer
            tickers = [f"{stock['ticker']} : {stock['name']}" for stock in data]
            completer = QCompleter(tickers, self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.search_bar.setCompleter(completer)

            self.search_bar.returnPressed.connect(self.add_ticker_to_list)

        except FileNotFoundError:
            self.search_bar.setPlaceholderText("stocks.json not found!")

    def add_ticker_to_list(self):
        """Add the selected ticker to the list."""
        ticker = self.search_bar.text()
        if ticker and ticker not in self.ticker_list:
            self.ticker_list.append(ticker)
        self.search_bar.clear()


def load_stylesheet(file_path: str) -> str:
    """Load QSS stylesheet from the given file path."""
    with open(file_path, "r") as file:
        return file.read()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load the stylesheet
    qss_path = "./src/style.qss"
    try:
        stylesheet = load_stylesheet(qss_path)
        app.setStyleSheet(stylesheet)
    except FileNotFoundError:
        print(f"Stylesheet file not found: {qss_path}")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())